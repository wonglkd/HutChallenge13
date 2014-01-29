import common
import customer
import splitxy
import features
import json
import argparse
import numpy as np
import probas
import yaml
import datetime
from pprint import pprint
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.externals import joblib
from sklearn.preprocessing import LabelBinarizer
import pylab as pl

def train(features_filename, y_filename, use_only_feat=None, save_clf=None, use_clf='rf', params_filename=None):
    """ Returns a pair of (classifier, feature_names, y_labels) """
    X_train_, X_train_feat_names = features.load(features_filename)
    # to be continued - to apply the two functions
    if use_only_feat:
        feats_to_use = get_feat_from_logfile(use_only_feat)
        if frozenset(X_train_feat_names) != frozenset(feats_to_use):
            common.print_err("Filtering out features based on those supplied (orig: {n})...".format(n=len(X_train_feat_names)))
            X_train_, X_train_feat_names = filter_feat(X_train_, X_train_feat_names, feats_to_use)
            common.print_err("{n} features remaining.".format(n=len(X_train_feat_names)))

    Y_list = list(splitxy.load_y(y_filename))

    lb = LabelBinarizer()
    Y_train_ = lb.fit_transform(Y_list)

    X_train = np.asarray(X_train_)
    Y_train = np.asarray(Y_train_)

    params_grid = {
        'n_estimators': [100]
    }
    params_fixed = {
        'rf': {
            # 'n_estimators': 80,
            'n_estimators': 20,
            # 'n_estimators': 50,
            # 'n_estimators': 20,
            # 'n_estimators': 2,
            # 'n_jobs': 2,
            'max_features': 20,
            'oob_score': True,
            'verbose': 2,
            'random_state': 101
        },
        'gbm': {
            'learning_rate': 0.10,
            # 'learning_rate': 0.05,
            'n_estimators': 5,
            # 'n_estimators': 100,
            'max_depth': 3,
            # 'subsample': 0.5,
            'verbose': 2,
            'random_state': 101
        },
        'sgd': {
            'loss': 'log', # 'modified_huber'
            'penalty': 'l2', # 'elasticnet'
            'alpha': 0.00001, # 0.00001, 0.000001
            'n_iter': 8, # 10, 50, 80
            'verbose': 2,
        }
    }

    if use_clf == 'rf':
        clf = RandomForestClassifier(**params_fixed['rf'])
    elif use_clf == 'gbm':
        clf = OneVsRestClassifier(GradientBoostingClassifier(**params_fixed['gbm']))
    elif use_clf == 'sgd':
        clf = OneVsRestClassifier(SGDClassifier(**params_fixed['sgd']))
    else:
        raise Exception("Classifier {} not found".format(use_clf))


    # Handle config file
    # Behaviour:
    # - if present, load from it.
    # - if not present, create it and dump current values there.

    try:
        with open(params_filename, 'rb') as f:
            loaded_params = yaml.load(f)
            if use_clf in loaded_params:
                clf.set_params(**loaded_params[use_clf])
                common.print_err("Params loaded from file.")
                pprint(loaded_params[use_clf])
    except IOError:
        # file does not exist
        common.print_err("Params file does not exist; creating it ({}).".format(params_filename))
        to_save = {
            use_clf: clf.get_params(),
            '_timestamp_saved': datetime.datetime.now().isoformat()
        }
        with open(params_filename, 'wb') as f:
            yaml.dump(to_save, f, default_flow_style=False)
            # pprint(to_save, stream=f)
    
    common.print_err("Parameters used:")
    pprint({use_clf: clf.get_params()})

    clf.fit(X_train, Y_train)
    
    return clf, X_train_feat_names, lb.classes_

def analyse(clf, feature_names, feat_impt_logfile):
    impts = clf.feature_importances_
    sorted_indices = np.argsort(impts)[::-1]

    with open(feat_impt_logfile, 'wb') as f_logfile:
        common.print_err("OOB Score:", clf.oob_score_)
        f_logfile.write("OOB Score:{}\n".format(clf.oob_score_))
        common.print_err("Feature Ranking:")
        for i, fid in enumerate(sorted_indices):
            feat_line = "{feat_name} {i}. #{id} ({impt})".format(
                i=i+1, id=fid, feat_name=feature_names[fid], impt=impts[fid])
            common.print_err(feat_line)
            f_logfile.write(feat_line + "\n")

    # Plot feature importance graph
    std = np.std([tree.feature_importances_ for tree in clf.estimators_],
                 axis=0)
    pl.figure()
    pl.title("Feature importances")
    pl.bar(range(len(sorted_indices)), impts[sorted_indices],
             color="r", yerr=std[sorted_indices], align="center")
    pl.xticks(range(len(sorted_indices)),
              [feature_names[v] for v in sorted_indices],
              rotation=45, horizontalalignment='right')
    pl.xlim([-1, len(sorted_indices)])
    fig = pl.gcf()
    fig.subplots_adjust(bottom=0.2)
    # pl.show()
    # if args.output == '-':
    #         pl.show()
    # else:
    #         pl.savefig(args.output)

def get_feat_from_logfile(feat_impt_logfile):
    return [line[0] for line in common.load_csv_i(feat_impt_logfile, delimiter=' ')]

def filter_feat(X, X_feat_names, feats_to_use):
    feats_to_use = frozenset(feats_to_use)
    X_feat_ind = [i for i, f in enumerate(X_feat_names) if f in feats_to_use]
    X, X_feat_names = np.asarray(X), np.asarray(X_feat_names)
    return X[:, X_feat_ind], X_feat_names[X_feat_ind]

def predict(clf, X_train_feat_names, y_labels, customer_ids, test_features_filename, preds_filename, top_k=20):
    """ Save top-K probabilities and labels """
    X_test, X_test_feat_names = features.load(test_features_filename)
    if frozenset(X_test_feat_names) != frozenset(X_train_feat_names):
        common.print_err("Filtering features to those used in training (orig: {n}...".format(n=len(X_test_feat_names)))
        X_test, X_test_feat_names = filter_feat(X_test, X_test_feat_names, X_train_feat_names)
        common.print_err("{n} features remaining.".format(n=len(X_test_feat_names)))

    Y_test_probas = clf.predict_proba(np.asarray(X_test))

    if clf.__class__.__name__ == 'RandomForestClassifier':
        Y_test_probas = [[pred[1] for pred in label_probs] for label_probs in Y_test_probas]
        Y_test_probas = np.asarray(Y_test_probas).T

    if len(Y_test_probas) != len(customer_ids):
        raise Exception("len(Y_test_probas) != len(customer_ids)")

    # Y_predicted: a list of lists of tuples (label, prob)
    Y_predicted = []
    for row in Y_test_probas:
        pred = np.argsort(row)[-top_k:][::-1]
        nz = row.nonzero()[0]
        if len(nz) <= top_k:
            pred = [i for i in pred if i in nz]
        row_probas = [(y_labels[i], row[i]) for i in pred]
        Y_predicted.append(row_probas)

    probas.save(Y_predicted, customer_ids, preds_filename)

    # lb.inverse_transform(Y_test_probas, threshold=0.5)
    # a = np.array([
    #   [0, 0, 0, 0, 0, 0, 6, 7, 8, 9, 0, 0, 0],
    #   [0, 0, 4, 0, 0, 0, 0, 0, 5, 6, 7, 8, 9]])
    # N = 6

def main():
    """
    Possible defaults:
    -t, --train: x-features.pkl
    -o, --output-model: model.pkl

    -p, --predict-feat: all-features.pkl
    -l, --load-model: model.pkl
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train')
    parser.add_argument('-y', '--y-list', default='y-list.csv')
    parser.add_argument('-o', '--output-model')

    parser.add_argument('-a', '--analyse-model', action='store_true')

    parser.add_argument('--clf', default='rf')
    parser.add_argument('--feature-select', action='store_true')
    parser.add_argument('--use-only-feat', default='rf-feature-importances.out')
    parser.add_argument('-p', '--predict-feat')
    parser.add_argument('-l', '--load-model')
    parser.add_argument('-c', '--customer-ids', default='all-customers-used.out')
    parser.add_argument('-s', '--save-probas', default='rf.probas')
    parser.add_argument('-f', '--save-feats-impt', default='rf-feature-importances.out')
    parser.add_argument('-P', '--params-filename', default='params-clf.yaml')

    # parser.add_argument('--cv', action='store_true')
    # parser.add_argument('--folds', default=3)
    # parser.add_argument('--gridsearch', action='store_true')
    # parser.add_argument('--usegrid', action='store_true')
    args = parser.parse_args()

    if args.train and args.load_model:
        raise Exception("--train and --load-model both specified")
    elif args.train:
        common.print_err("Training model...")
        use_feat = None if not args.feature_select else args.use_only_feat
        clf, x_feat_names, y_labels = train(args.train, args.y_list, use_feat, args.output_model, args.clf, args.params_filename)
        if args.output_model:
            common.print_err("Saving model...")
            # joblib.dump((clf, x_feat_names, y_labels), args.output_model)
            common.save_pickle(args.output_model, (clf, x_feat_names, y_labels))
    elif args.load_model:
        common.print_err("Loading model...")
        clf, x_feat_names, y_labels = joblib.load(args.load_model)
    else:
        raise Exception("--train and --load-model both not specified")

    if args.analyse_model:
        common.print_err("Analysing model...")
        analyse(clf, x_feat_names, args.save_feats_impt)

    if args.predict_feat:
        common.print_err("Making predictions...")
        customer_ids = customer.load_ids(args.customer_ids)
        predict(clf, x_feat_names, y_labels, customer_ids, args.predict_feat, args.save_probas)

if __name__ == "__main__":
    main()
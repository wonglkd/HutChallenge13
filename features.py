import argparse
import common
import customer
import splitxy
from pprint import pprint
from collections import Counter
import dateutil.parser
import datetime
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.externals import joblib
from sklearn.base import BaseEstimator

class Feature(BaseEstimator):
    def generate_feat(self, orders):
        raise NotImplementedError

    def transform(self, X):
        # lazy (generator)
        # for orders in X:
        #     yield [self.generate_feat(orders)]

        # non-lazy
        return [[self.generate_feat(orders)] for orders in X]

    def fit(self, X, y=None):
        return

    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X)

    def get_feature_names(self):
        return ['x']

class FeatureFindClasses(Feature):
    def __init__(self, classes_to_count=None):
        self.classes = classes_to_count
        self._classes_fixed = classes_to_count is not None
 
    def get_feature_names(self):
        return ["C({pid})".format(pid=p) for p in self.classes]

class FeatCountry(FeatureFindClasses):
    def fit(self, X, y=None):
        if self._classes_fixed:
            return
        seen = set()
        for orders in X:
            for row in orders:
                seen.add(row[3])
        self.classes = list(seen)

    def transform(self, X, y=None):
        return [[int(c == customer.get_most_common_country(orders))
                for c in self.classes]
                for orders in X]

class FeatNOrders(Feature):
    """ No. of order entries """

    def generate_feat(self, orders):
        return len(orders)

class FeatNTransactions(Feature):
    """ No. of distinct order times """

    def generate_feat(self, orders):
        return len(customer.get_unique_times(orders))

class FeatAvgOrdersPerTransaction(Feature):
    "Average Size of Transaction = FeatNOrders / FeatNTransactions"
    def generate_feat(self, orders):
        return len(orders) / len(customer.get_unique_times(orders))

class FeatNProducts(Feature):
    """ No. of distinct products """

    def generate_feat(self, orders):
        return len(set([a[customer.ORDER_INDEX_PRODUCT] for a in orders]))

class FeatTimeSinceLastOrder(Feature):
    def generate_feat(self, orders):
        maxtime = dateutil.parser.parse(max(a[customer.ORDER_INDEX_TIME] for a in orders))
        return (maxtime-datetime.datetime(1970,1,1)).total_seconds()

class FeatAvgIntervalBetweenTransactions(Feature):
    """ Average interval between transactions """
    def generate_feat(self, orders):
        #print orders
        times = customer.get_unique_times(orders)

        return (dateutil.parser.parse(times[-1]) - 
                dateutil.parser.parse(times[0])).total_seconds() / len(times)


class FeatIndividualProductCount(FeatureFindClasses):
    def fit(self, X, y=None):
        """ Find out the breadth of the product space """
        if self._classes_fixed:
            return
        seen = set()
        for orders in X:
            for row in orders:
                seen.add(row[1])
        self.classes = list(seen)
    
    def transform(self, X):
        newX = []
        for orders in X:
            product_count = Counter(row[1] for row in orders)
            newX.append([product_count[p] for p in self.classes])
        return newX

class FeatIndividualProductBinary(FeatIndividualProductCount):
    """ Whether product X was bought by customer, for multiple X """

    def transform(self, X):
        newX = []
        for orders in X:
            products_ordered = frozenset(row[1] for row in orders)
            newX.append([int(p in products_ordered) for p in self.classes])
        return newX


def get_combined():
    feature_generators = [
        ('fg_NOrders', FeatNOrders()),
        ('fg_NTransactions', FeatNTransactions()),
        ('fg_AvgOrdersPerTransaction', FeatAvgOrdersPerTransaction()),
        ('fg_NProducts', FeatNProducts()),
        ('fg_TimeSinceLastOrder', FeatTimeSinceLastOrder()),
        ('fg_AvgIntervalBetweenTransactions', FeatAvgIntervalBetweenTransactions()),
        ('fg_Country', FeatCountry()),

        # ('fg_IndividualProductBinary', FeatIndividualProductBinary()),
        ('fg_IndividualProductCount', FeatIndividualProductCount())
    ]
    # Disabled for the moment, lb/get_feature_names() does not play well with parallelisation
    # return FeatureUnion(feature_generators, n_jobs=-1)
    return FeatureUnion(feature_generators)

def load(features_filename):
    """ Returns a tuple of (features, feature_names) """
    return joblib.load(features_filename)

def save(X, feat_names, features_filename):
    joblib.dump((X, feat_names), features_filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("x_orders_files", nargs='*', default=["x-orders.pkl"])
    parser.add_argument("-o", "--output-features-files", nargs='*', default=["x-features.pkl"])
    args = parser.parse_args()

    # customers = [1,2,100,270074,270081]
    # customers = [1,2,5]
    
    #pprint(splitter.split(customer.get_records(270074)))
    #pprint(splitter.split(customer.get_records(100)))
    # pprint((customer.get_records(3)))
    #pprint(splitter.split(customer.get_records(270081)))
    # cr = [customer.get_records(i) for i in customers]

    if len(args.x_orders_files) != len(args.output_features_files):
        raise Exception("len(x_orders_files) != len(output_features_files)")

    crs = [list(splitxy.load_x(o_filename)) for o_filename in args.x_orders_files]

    combined = get_combined()

    combined.fit(common.flatten_lists(crs))
    feat_names = combined.get_feature_names()

    for cr, output_feat_file in zip(crs, args.output_features_files):
        X = combined.transform(cr)
        common.print_err("{} examples by {} features".format(*X.shape))
        save(X, feat_names, output_feat_file)

    # ft = FeatCountry()
#     ft = FeatNOrders()
#     ft = FeatNTransactions()
    # ft = FeatTimeSinceLastOrder()
    # print(FeatCountry().fit_transform(cr))
    # ft = FeatIndividualProductBinary()
    # pprint(list(ft.fit_transform(cr)))
    # ft2 = FeatIndividualProductCount()
    # pprint(list(ft2.fit_transform(cr)))

if __name__ == "__main__":
    main()
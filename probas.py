import common
import customer
import argparse
import json
import scipy.stats
from itertools import izip

def load(probas_filename):
    cust_probas = {}
    for line in common.load_file(probas_filename):
        if line.strip() == "":
            continue
        line = line.split("|")
        customer, probas = line
        probas = json.loads(probas)
        cust_probas[customer] = probas
    return cust_probas

def save(probas, customer_ids, probas_filename):
    with open(probas_filename, 'wb') as f_preds:
        for customer_id, row_probas in izip(customer_ids, probas):
            row_probas = ['"{}":{:g}'.format(label, val) for label, val in row_probas]
            f_preds.write(customer_id + "|{" + ",".join(row_probas) + "}\n")


def merge_dicts(dcts, combine_func=sum):
    all_keys = set()
    result = {}
    for dct in dcts:
        all_keys |= set(dct.keys())
    for k in all_keys:
        result[k] = combine_func(dct.get(k, 0) for dct in dcts)
    return result

def combine(list_of_probas, combine_func=sum):
    # simple summation
    all_customers = set()
    for pr in list_of_probas:
        all_customers |= set(pr.keys())

    combined_probas = {}
    for c in all_customers:
        combined_for_cust = {}
        all_probas_for_cust = []
        for probas in list_of_probas:
            if c in probas:
                all_probas_for_cust.append(probas[c])
        if len(all_probas_for_cust) > 1:
            combined_for_cust = merge_dicts(all_probas_for_cust, combine_func)
        elif len(all_probas_for_cust) == 1:
            combined_for_cust = all_probas_for_cust[0]
        combined_probas[c] = combined_for_cust
    return combined_probas

def reweigh_dict(dct_of_dcts, factor):
    """ Multiply all values inside a dict of dicts by a factor """
    factor = float(factor)
    reweighted = {}
    for c, dct in dct_of_dcts.iteritems():
        reweighted[c] = { k: v * factor for k, v in dct.iteritems() }
    return reweighted

def get_predictions(probas, N=6, to_pad=None):
    """ Takes top 6 non-zero probabilities as labels.
        If < 6 items, pad with items from to_pad. """
    result = {}
    for customer, prob in probas.iteritems():
        ans = sorted(prob.iteritems(), key=lambda x:x[1], reverse=True)[:N]
        ans = [int(x[0]) for x in ans]
        for item in to_pad:
            if len(ans) >= N:
                break
            if item not in ans:
                ans.append(item)
        result[customer] = ans
    return result

def save_submission(result, submission_filename, customers_filename):
    with open(submission_filename, 'wb') as f:
        for c in customer.load_ids(customers_filename):
            f.write(','.join(map(str, result[c])) + '\n')

def load_submission_i(submission_filename, customers_filename):
    for customer_id, row in izip(customer.load_ids(customers_filename),
                                 common.load_csv_i(submission_filename)):
        yield customer_id, map(int, row)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('probas_filenames', nargs='+')
    parser.add_argument('-c', '--customers_filename')
    parser.add_argument('-w', '--weights', nargs='*', type=float)
    parser.add_argument('-o', '--output', default='combined.sol')
    parser.add_argument('-p', '--to-pad', nargs='*', type=int, default=[200,441,177,392,50,11])
    args = parser.parse_args()

    combine_func = sum
    # doesn't work just yet
    # combine_func = scipy.stats.hmean
    # combine_func = scipy.stats.gmean


    all_probas = [load(f) for f in args.probas_filenames]
    if args.weights:
        if len(all_probas) != len(args.weights):
            raise Exception("len(all_probas) != len(arg.weights)")
        all_probas = [reweigh_dict(p, factor) for p, factor in zip(all_probas, args.weights)]
    flattened_probas = combine(all_probas, combine_func)

    result = get_predictions(flattened_probas, to_pad=args.to_pad)
    save_submission(result, args.output, args.customers_filename)

if __name__ == "__main__":
    main()
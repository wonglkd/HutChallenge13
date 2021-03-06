import common
import customer
import argparse
import json
import scipy.stats
from collections import defaultdict
from itertools import izip
from functools import partial
import numpy as np

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
    """
    probas: iterable of tuples of (label, val:float)
    customer_ids: an iterable of customer ids (strings expected)
    """
    with open(probas_filename, 'wb') as f_preds:
        for customer_id, row_probas in izip(customer_ids, probas):
            row_probas = ['"{}":{:g}'.format(label, val) for label, val in row_probas]
            f_preds.write(customer_id + "|{" + ",".join(row_probas) + "}\n")


def merge_dicts(dcts, combine_func=sum):
    """
    For instance, given a list of dicts (one for each method)
    and we want to combine the probas given by different methods
    """
    all_keys = set()
    result = {}
    for dct in dcts:
        all_keys |= set(dct.keys())
    for k in all_keys:
        result[k] = combine_func(dct.get(k, 0) for dct in dcts)
    return result

def merge_ranklists(dcts):
    """
    Similar to merge_dicts, but this version combines ranking lists
    """
    result = defaultdict(float)
    for dct in dcts:
        curr_len = float(len(dct))
        for i, (k, _) in enumerate(sorted(dct.iteritems(), reverse=True, key=lambda x:x[1])):
            result[k] += 1. - (i / curr_len)
    return dict(result)

def combine(list_of_probas, merge_func, customers_filename='data/publicChallenge.csv'):
    # simple summation
    all_customers = set()
    for pr in list_of_probas:
        all_customers |= set(pr.keys())

    all_customers |= set(map(str, customer.load_ids(customers_filename)))

    combined_probas = {}
    for c in all_customers:
        combined_for_cust = {}
        all_probas_for_cust = []
        for probas in list_of_probas:
            if c in probas:
                all_probas_for_cust.append(probas[c])
        if len(all_probas_for_cust) > 1:
            combined_for_cust = merge_func(all_probas_for_cust)
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

def get_predictions(probas, N=6, to_pad=None, cold_start=None):
    """ Takes top 6 non-zero probabilities as labels.
        If < 6 items, pad with items from to_pad. """
    result = {}
    for customer, prob in probas.iteritems():
        ans = sorted(prob.iteritems(), key=lambda x:x[1], reverse=True)[:N]
        ans = [int(x[0]) for x in ans]
        if not ans:
            ans = list(cold_start)
        else:
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

def harmonic_mean_n(vals, N=2):
    vals = list(vals)
    pad_with = min(vals) / 2.
    while len(vals) < N:
        vals.append(pad_with)
    vals = [1. / max(v, 0.001) for v in vals]
    return N / np.sum(vals)

def geometric_product(vals):
    p = 1.
    for v in vals:
        p *= max(v, 0.03)
    return p

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('probas_filenames', nargs='+')
    parser.add_argument('-c', '--customers_filename')
    parser.add_argument('-w', '--weights', nargs='*', type=float)
    parser.add_argument('-o', '--output', default='combined.sol')
    # parser.add_argument('-p', '--to-pad', nargs='*', type=int, default=[200,441,177,392,50,11])
    # parser.add_argument('-p', '--to-pad', nargs='*', type=int, default=[200,392,500,328,404])
    # parser.add_argument('-s', '--cold-start', nargs='*', type=int, default=[200,316,500,392,135])
    parser.add_argument('-p', '--to-pad', nargs='*', type=int, default=[200,392,500,316,47])
    parser.add_argument('-s', '--cold-start', nargs='*', type=int, default=[200,392,500,316,47])
    parser.add_argument('--merge-func', choices=['dicts','ranklists'], default='dicts')
    parser.add_argument('--combine-func', choices=['sum','harmonic','geometric'], default='sum')
    args = parser.parse_args()

    if args.combine_func == "sum":
        combine_func = sum
    elif args.combine_func == "harmonic":
        combine_func = partial(harmonic_mean_n, N=len(args.probas_filenames))
    elif args.combine_func == "geometric":
        combine_func = geometric_product
    # doesn't work just yet
    # combine_func = scipy.stats.hmean
    # combine_func = scipy.stats.gmean
    if args.merge_func == "dicts":
        merge_func = partial(merge_dicts, combine_func=combine_func)
    elif args.merge_func == "ranklists":
        merge_func = merge_ranklists

    all_probas = [load(f) for f in args.probas_filenames]
    if args.weights:
        if len(all_probas) != len(args.weights):
            raise Exception("len(all_probas) != len(arg.weights)")
        all_probas = [reweigh_dict(p, factor) for p, factor in zip(all_probas, args.weights)]
    flattened_probas = combine(all_probas, merge_func, args.customers_filename)

    result = get_predictions(flattened_probas, to_pad=args.to_pad, cold_start=args.cold_start)
    save_submission(result, args.output, args.customers_filename)

if __name__ == "__main__":
    main()

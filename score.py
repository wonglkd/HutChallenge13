import common
import argparse
import customer
import numpy as np
import splitxy
import probas

def align_preds_actuals(preds, actuals):
    """
    preds: an iterable of tuples,
           each in the form (customer_id, [product1, product2, ...]
    actuals: a dict of form { customerid: [product1, product2, ...] }
    """
    skipped_customers = []
    for customer_id, preds_row in preds:
        if customer_id in actuals:
            yield preds_row, actuals[customer_id]
        else:
            pass
            # skipped_customers.append(customer_id)
            # common.print_err("Skipped customer ({c}), no actuals".format(c=customer_id))

def main():
    parser = argparse.ArgumentParser(description='Calculate @MAP score')
    parser.add_argument('actuals_filename',
                        help='actuals (gold standard) csv filename (y-list.csv)')
    parser.add_argument('preds_filename',  
                        help='predicted csv filename (sol.csv)')
    parser.add_argument('-c', '--customers-file', default='data/publicChallenge.csv')
    parser.add_argument('-k', type=int, default=6)
    args = parser.parse_args();

    actuals = splitxy.load_y_with_cust(args.actuals_filename)
    preds = probas.load_submission_i(args.preds_filename, args.customers_file)

    customers = customer.load_ids(args.customers_file)
    common.print_err("No. of total customers = {}".format(len(customers)))
    # if len(actuals) != len(customers):
    #     common.print_err("No. of predictions != customers.")

    actuals_preds = align_preds_actuals(preds, actuals)

    print "MAP@{K} = {mapk}".format(K=args.k, mapk=map_k(actuals_preds, args.k))

def apk(actuals, preds, k):
    """ Average Precision @ K """
    if len(preds) > k:
        preds = preds[:k]
    
    actuals = frozenset(actuals)

    score = 0.0
    cnt_hits = 0.0

    for i, p in enumerate(preds):
        # second condition checks that item was not already predicted
        if p in actuals and p not in preds[:i]:
            cnt_hits += 1.0
            score += cnt_hits / (i + 1.0)

    if not actuals:
        return 1.0

    return score / min(len(actuals), k)

def map_k(actuals_preds_iter, k):
    """ Mean Average Precision @ K """
    aps = [apk(a,p,k) for a, p in actuals_preds_iter]
    common.print_err("No. of predictions evaluated = {}".format(len(aps)))
    return np.mean(aps)

if __name__ == '__main__':
    main()

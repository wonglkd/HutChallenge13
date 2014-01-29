import common
import customer
from collections import defaultdict
from itertools import combinations
import probas
import argparse
import math

def load_customer_product_counts(filename):
    # Here we only consider whether a product is bought by a customer,
    # and not the specific counts. This could be adapted (and possibly improved)
    # to take into account the actual counts.
    customers_who_bought_product = defaultdict(set)
    products_bought_by_customer = defaultdict(set)
    for row in common.load_csv_i(filename):
        # do some sanity checks - there are weird rows in the file of the form x,, -- skip those rows
        # need to do some sanity checks
        if not row or not row[0] or not row[1] or not row[2]:
            continue
        customer_id, product_id, cnt = map(int, row)
        customers_who_bought_product[product_id].add(customer_id)
        products_bought_by_customer[customer_id].add(product_id) 
    return customers_who_bought_product, products_bought_by_customer

def sim_cos(A, B):
    return float(len(A & B)) / math.sqrt(len(A) * len(B))

def sim_cos_log(A, B):
    return math.log(1. + float(len(A & B)) / math.sqrt(len(A) * len(B)))

def sim_jaccard(A, B):
    return float(len(A & B)) / (len(A | B))

def main():
    parser = argparse.ArgumentParser(description='Calculate item-based CF probas')
    parser.add_argument('customer_product_counts', default='interim/products_by_test_customers_cnts.csv')
    parser.add_argument('-o', '--preds-filename')
    parser.add_argument('-c', '--customer-ids-filename', default='data/publicChallenge.csv')
    parser.add_argument('-s', '--similarity-func', default='jaccard', choices=['jaccard', 'cos', 'cos_log'])
    # parser.add_argument('-K', '--take-top-products-in-p-matrix', default=250, type=int)
    parser.add_argument('-N', '--take-top-products-for-user', default=80, type=int)
    args = parser.parse_args()
   
    common.print_err("Loading data...")
    customers_who_bought_product, products_bought_by_customer = load_customer_product_counts(args.customer_product_counts)
    
    products = customers_who_bought_product.keys()
    # customer_ids = products_bought_by_customer.keys()
    customer_ids = customer.load_ids(args.customer_ids_filename)
    nscore = defaultdict(dict)

    func_sim = globals()["sim_"+args.similarity_func]

    common.print_err("Calculating product-similarity scores...")
    for p1, p2 in combinations(products, 2):
        score = func_sim(customers_who_bought_product[p1], customers_who_bought_product[p2])
        if score > 0.:
            nscore[p1][p2] = score
            nscore[p2][p1] = score
    
    common.print_err("Generating predictions by summing scores...")
    Y_predicted, customer_ids_used = [], []
    # for customer_id, products_bought in products_bought_by_customer.iteritems():
    for customer_id in customer_ids:
        if int(customer_id) not in products_bought_by_customer:
            continue
        products_bought = products_bought_by_customer[int(customer_id)]
        # cos ( dot product ) / | no of customers 1 |
        # for product_id in products_bought:
            # nscore[product_id]
            # find top N recommended products
            # nscore[product_id].sort()
        nscore_dcts = [nscore[product_id] for product_id in products_bought]
        # we probably should refactor merge_dicts from probas into common
        preds = probas.merge_dicts(nscore_dcts, combine_func=sum).items()
        preds = sorted(preds, key=lambda x:x[1], reverse=True)[:args.take_top_products_for_user]
        preds_total = sum(x[1] for x in preds)
        preds = [(p, v / preds_total) for p, v in preds]
        customer_ids_used.append(customer_id)
        Y_predicted.append(preds)
        # c_probas[product_id] = score / probability
    probas.save(Y_predicted, customer_ids, args.preds_filename)

if __name__ == "__main__":
    main()
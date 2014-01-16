import common
import argparse
import sys
from collections import Counter

_db = common.DBWrapper()

def get_records(customer_id):
    return list(_db.select('SELECT * FROM rec WHERE customer = ?', [customer_id]))

def get_mult_records_i(customer_ids, yield_customer_id=True):
    if yield_customer_id:
        for c_id in customer_ids:
            yield c_id, get_records(c_id)
    else:
        for c_id in customer_ids:
            yield get_records(c_id)


def get_mult_records(customer_ids):
    return list(get_mult_records_i(customer_ids))

def save_records(X, X_filename):
    common.save_pickle(X_filename, X)

def get_unique_times(orders):
    return sorted(set([row[2] for row in orders]))

def get_most_common_country(orders):
    return Counter([row[3] for row in orders]).most_common(1)[0][0]

def save_ids(c_ids, c_ids_filename):
    common.save_csv_i(c_ids_filename, ([r] for r in c_ids))

def load_ids(c_ids_filename, add_prefix=''):
    with open(c_ids_filename, 'rb') as f:
        return [add_prefix+cid.strip() for cid in f if cid.strip() != ""]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("customers_file", nargs='?', default="gen/customers-100.txt")
    parser.add_argument("-o", "--orders-out", default='all-orders.pkl')
    parser.add_argument("-c", "--customers-out", nargs='?', default="customers-all-used.out")
    args = parser.parse_args()
    cst = (int(customer_id)
           for customer_id
           in common.load_file(args.customers_file))

    X = []
    c_ids_used = []

    for c_id in cst:
        cr = get_records(c_id)
        if cr:
            X.append(cr)
            c_ids_used.append(c_id)

    save_records(X, args.orders_out)
    common.save_csv_i(args.customers_out, ([c] for c in c_ids_used))

if __name__ == '__main__':
    main()

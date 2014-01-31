import argparse
import common
import math
import customer
import csv
import json
from collections import Counter
from pprint import pprint

class SplitXY:
    def get_y_from_orders(self, orders):
        products_Y = [row[1] for row in orders]
        return list(set(products_Y))
        # return dict(Counter(products_Y))

class SplitXYByTime(SplitXY):
    def __init__(self, split_time = '2013-06-00'):
        self._split_time = split_time

    def split(self, customer_records, t = None):
        """ Everything before time is used for X, everything >= time for Y """
        if t == None:
            t = self._split_time
        customer_records_train = []
        cr_X, cr_Y = common.partition(lambda r: r[2] < t, customer_records)
        return cr_X, self.get_y_from_orders(cr_Y)

class SplitXYByPer(SplitXYByTime):
    def __init__(self, per = 0.25):
        self._per = per

    def split(self, customer_records, per = None):
        """ Splits by percentage of orders (defined here as distinct times).
            Assumes at least 2 distinct times given. """
        if per == None:
            per = self._per
        times = customer.get_unique_times(customer_records)
        times_to_take = max(1, int(len(times) * per))
        splitting_time = times[len(times) - times_to_take]
        return SplitXYByTime.split(self, customer_records, splitting_time)

def get_split_i(splitter, customer_ids, min_x, min_y):
    for customer_id, customer_records in customer.get_mult_records_i(customer_ids):
        if len(customer.get_unique_times(customer_records)) < 2:
            common.print_err("Skipped:", customer_id)
            continue
        x_orders_set, y_row = splitter.split(customer_records)
        if len(x_orders_set) < min_x:
            common.print_err("Skipped due to x too small: {} ({})".format(customer_id, len(x_orders_set)))
            continue
        if len(y_row) < min_y:
            common.print_err("Skipped due to y too small: {} ({})".format(customer_id, len(y_row)))
            continue
            
        yield customer_id, x_orders_set, y_row
        # print customer_id
        # pprint(customer_records)
        # pprint(x_orders_set)
        # pprint(y_row)

def get_split(*args, **kwargs):
    """ Input:
            splitter: a sub-class of SplitXY),
            customer_ids: a list of customer IDs to retrieve data for
        Output:
            X: a list of lists, with each internal list corresponding to
               one customer and showing the orders available to mine data
            Y: a list of lists, with each internal list corresponding to
               one customer and listing the products that the customer
               bought within the second split of the data
            c_ids: a list of customer ids that correspond to X and Y """
    c_ids, X, Y = [], [], []
    for c_id, x_orders_set_i, y_row_i in get_split_i(*args, **kwargs):
        X.append(x_orders_set_i)
        Y.append((c_id, y_row_i))
        c_ids.append(c_id)
    return X, Y, c_ids

def save(X, X_filename, Y, Y_filename, c_ids, c_ids_filename):
    customer.save_records(X, X_filename)
    common.save_csv_i(Y_filename, Y)
    customer.save_ids(c_ids, c_ids_filename)

def load_x(filename):
    return common.load_pickle(filename)

def load_y(filename):
    for _, row in common.load_csv_i(filename):
        yield json.loads(row)

def load_y_with_cust(filename):
    """ returns a dict of form { customerid: [product1, product2, ...] } """
    return { customer_id : json.loads(row)
             for customer_id, row in common.load_csv_i(filename) }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("customers_file", nargs='?', default="interim/customers-100.txt")
    parser.add_argument("-x", "--x-orders-out", nargs='?', default="x-orders.pkl")
    parser.add_argument("-y", "--y-out", nargs='?', default="y-list.csv")
    parser.add_argument("-c", "--customers-out", nargs='?', default="customers-split-used.out")
    parser.add_argument("-s", "--splitter", choices=['time','percent'], default='time')
    
    args = parser.parse_args()

    cst = (int(customer_id)
           for customer_id
           in common.load_file(args.customers_file))
    # cst = [1,2,100,270074,270081]
    # cst = [1,5]

    #splitter = SplitXYByTime('2013-03-00')
    #pprint(splitter.split(customer.get_records(270074)))
    #pprint(splitter.split(customer.get_records(100)))
    # pprint(splitter.split(customer.get_records(1)))
    #pprint(splitter.split(customer.get_records(270081)))

    if args.splitter == 'percent':
        splitter = SplitXYByPer()
        min_x = 1
        min_y = 1
    elif args.spitter == 'time':
        splitter = SplitXYByTime('2013-06-00')
        min_x = 1
        min_y = 4

    X, Y, c_ids = get_split(splitter, cst, min_x, min_y)
    save(X, args.x_orders_out, Y, args.y_out, c_ids, args.customers_out)

if __name__ == '__main__':
    main()

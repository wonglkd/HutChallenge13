import argparse
import common
import math
import customer
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

    """ Everything before time is used for X, everything >= time for Y """
    def split(self, customer_records, t = None):
        if t == None:
            t = self._split_time
        customer_records_train = []
        cr_X, cr_Y = common.partition(lambda r: r[2] < t, customer_records)
        return cr_X, self.get_y_from_orders(cr_Y)

class SplitXYByPer(SplitXYByTime):
    def __init__(self, per = 0.25):
        self._per = per

    """ Splits by percentage of orders (defined here as distinct times).
        Assumes at least 2 distinct times given. """
    def split(self, customer_records, per = None):
        if per == None:
            per = self._per
        times = customer.get_unique_times(customer_records)
        times_to_take = max(1, int(len(times) * per))
        splitting_time = times[len(times) - times_to_take]
        return SplitXYByTime.split(self, customer_records, splitting_time)

def get_split(splitter, customer_ids):
    X, Y = [], []
    for customer_id in customer_ids:
        customer_records = customer.get_records(customer_id)
        if len(customer.get_unique_times(customer_records)) < 2:
            common.print_err("Skipped:", customer_id)
            continue
        # pprint(customer_records)
        # print customer_id
        # print(splitter.split(customer_records))
        x_orders_set, y_row = splitter.split(customer_records)
        X.append(x_orders_set)
        Y.append(y_row)
    return X, Y

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("customers_file", nargs='?', default="gen/customers-100.txt")
    args = parser.parse_args()

    #customers = [1,2,100,270074,270081]
    
    splitter = SplitXYByPer()
    #splitter = SplitXYByTime('2013-03-00')
    
    #pprint(splitter.split(customer.get_records(270074)))
    #pprint(splitter.split(customer.get_records(100)))
    # pprint(splitter.split(customer.get_records(1)))
    #pprint(splitter.split(customer.get_records(270081)))

    cst = (int(customer_id)
           for customer_id
           in common.load_file(args.customers_file))
    # cst = [322273,198150]

    get_split(splitter, cst)

if __name__ == '__main__':
    main()
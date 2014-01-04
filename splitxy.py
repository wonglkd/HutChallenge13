import common
import math
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

    """ Splits by percentage of orders (defined here as distinct times) """
    def split(self, customer_records, per = None):
        if per == None:
            per = self._per
        times = sorted(set([a[2] for a in customer_records]))
        times_to_take = max(1, int(len(times) * per))
        splitting_time = times[len(times) - times_to_take]
        return SplitXYByTime.split(self, customer_records, splitting_time)

def get_customer_records(customer_id):
    db = common.DBWrapper()
    return list(db.select('SELECT * FROM rec WHERE customer = ?', [customer_id]))

def main():
    customers = [1,2,100,270074,270081]
    
    splitter = SplitXYByPer()
    #splitter = SplitXYByTime('2013-03-00')
    
    #pprint(splitter.split(get_customer_records(270074)))
    #pprint(splitter.split(get_customer_records(100)))
    pprint(splitter.split(get_customer_records(1)))
    #pprint(splitter.split(get_customer_records(270081)))
    
    # SELECT * FROM rec WHERE time < 

if __name__ == '__main__':
    main()
import common
import customer
from pprint import pprint
from collections import Counter
import dateutil.parser
import datetime
from sklearn import preprocessing
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import FeatureUnion
from sklearn.externals import joblib

class Feature:
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
    
class FeatCountry(Feature):
    def __init__(self):
        self.vectorizer = DictVectorizer()

    def fit_transform(self, X, y=None):
        newX = []
        for orders in X:
            newX.append({'country':
                Counter([row[3] for row in orders]).most_common(1)[0][0]})
        return self.vectorizer.fit_transform(newX)

class FeatNOrders(Feature):
    """ No. of order entries """

    def generate_feat(self, orders):
        return len(orders)

class FeatNTransactions(Feature):
    """ No. of distinct order times """

    def generate_feat(self, orders):
        return len(set([a[2] for a in orders]))

class FeatNProducts(Feature):
    """ No. of distinct products """

    def generate_feat(self, orders):
        return len(set([a[1] for a in orders]))

class FeatTimeSinceLastOrder(Feature):
    def generate_feat(self, orders):
        maxtime = dateutil.parser.parse(max(a[2] for a in orders))
        return (maxtime-datetime.datetime(1970,1,1)).total_seconds()

class FeatIndividualProductBinary(Feature):
    """ Whether product X was bought by customer, for multiple X """

    def __init__(self):
        self.lb = preprocessing.LabelBinarizer()

    def fit(self, X, y=None):
        raise NotImplementedError

    def fit_transform(self, X, y=None):
        self._newX = []
        for orders in X:
            self._newX.append(list(set(row[1] for row in orders)))
        return self.lb.fit_transform(self._newX)

class FeatIndividualProductCount(Feature):
    def __init__(self, products_to_count = []):
        self.products = products_to_count

    def fit(self, X, y=None):
        """ Find out the breadth of the product space """
        seen = set()
        for orders in X:
            for row in orders:
                seen.add(row[1])
        self.products = list(seen)
    
    def transform(self, X):
        newX = []
        for orders in X:
            productCount = Counter(row[1] for row in orders)
            newX.append([productCount[p] for p in self.products])
        return newX

def get_combined():
    feature_generators = [
        ('fg_NOrders', FeatNOrders()),
        ('fg_NTransactions', FeatNTransactions()),
        ('fg_NProducts', FeatNProducts()),
        ('fg_Country', FeatCountry()),
        ('fg_TimeSinceLastOrder', FeatTimeSinceLastOrder()),
        ('fg_IndividualProductBinary', FeatIndividualProductBinary()),
        ('fg_IndividualProductCount', FeatIndividualProductCount())
    ]
    return FeatureUnion(feature_generators, n_jobs=-1)

def main():
    customers = [1,2,100,270074,270081]
    customers = [1,2,5]
    
    #pprint(splitter.split(customer.get_records(270074)))
    #pprint(splitter.split(customer.get_records(100)))
    # pprint((customer.get_records(3)))
    #pprint(splitter.split(customer.get_records(270081)))
    cr = [customer.get_records(i) for i in customers]
    combined = get_combined()
    features_file = 'gen/features.pkl'
    X = combined.fit_transform(cr)
    joblib.dump(X, features_file)
#     ft = FeatCountry()
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
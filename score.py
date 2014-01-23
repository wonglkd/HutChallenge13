import common
import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Calculate @MAP score')
    parser.add_argument('preds_filename', metavar='preds_filename',  
                        help='predicted csv filename')
    parser.add_argument('goldstd_filename', metavar='goldstd_filename',
                        default='', help='gold standard csv filename')
    
    parser.add_argument('k', metavar='k', nargs='?', default='6')

    args = parser.parse_args();
    
    predicted = [map(int, row) for row in common.load_csv_i(preds_filename)]
    actual = [map(int, row) for row in common.load_csv_i(goldstd_filename)] 
    
    print "@MAP" + k
    print mapk(actual, predicted, k)

def apk(actual, predicted, k):
    if len(predicted)>k:
        predicted = predicted[:k]
    
    actual = frozenset(actual)

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 1.0

    return score / min(len(actual), k)

# actual is all the examples ...
# predicted is all the examples
def mapk(actual, predicted, k):
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])

if __name__ == '__main__':
    main()

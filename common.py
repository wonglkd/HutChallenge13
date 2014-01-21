import sys
import cPickle as pickle
import csv
import os.path

try:
    import apsw
    db_interface = 'apsw'
except ImportError:
    import sqlite3
    db_interface = 'sqlite'

class DBWrapper:
    def __init__(self, id='origdata'):
        DBs = {
            'origdata': os.path.join(os.path.dirname(__file__), "db/db.sqlite3")
        }
        db_filename = DBs[id]
        if db_interface == 'apsw':
             self._conn = apsw.Connection(db_filename)
        else:
             self._conn = sqlite3.connect(db_filename)
    
    def select(self, query, para = None):
        cur = self._conn.cursor()
        if db_interface == 'apsw':
            for row in cur.execute(query, para):
                yield row
        else:
            if para == None:
                para = []
            cur.execute(query, para)
            for row in cur.fetchall():
                yield row

def print_err(*args):
    sys.stderr.write(' '.join(map(str,args)) + '\n')

def verbose_iter(iter, n=10000):
    for i, line in enumerate(iter):
        yield i, line
        if (i+1) % n == 0:
            print_err(i+1, 'lines done')

def load_file(filename):
    with open(filename, 'rb') as f:
        for line in f:
            yield line

def flatten_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

def partition(pred, iter):
    t = []
    f = []
    for row in iter:
        if pred(row):
            t.append(row)
        else:
            f.append(row)
    return t, f

def save_pickle(filename, obj):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def save_csv_i(filename, obj_iter, delimiter=','):
    with open(filename, 'wb') as f:
        writer = csv.writer(f, delimiter=delimiter)
        for line in obj_iter:
            writer.writerow(line)

def load_csv_i(filename, delimiter=','):
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=delimiter)
        for line in reader:
            yield line

import sys

try:
    import apsw
    db_interface = 'apsw'
except ImportError:
    import sqlite3
    db_interface = 'sqlite'

class DBWrapper:
    def __init__(self, id='origdata'):
        DBs = {
            'origdata': "db/db.sqlite3"
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

def load_customers(filename, prefix=''):
    with open(filename, 'rb') as f:
        return [prefix+cid.strip() for cid in f if cid.strip() != ""]

def partition(pred, iter):
    t = []
    f = []
    for row in iter:
        if pred(row):
            t.append(row)
        else:
            f.append(row)
    return t, f

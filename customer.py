import common

def get_records(customer_id):
    db = common.DBWrapper()
    return list(db.select('SELECT * FROM rec WHERE customer = ?', [customer_id]))

def get_unique_times(orders):
    return sorted(set([row[2] for row in orders]))
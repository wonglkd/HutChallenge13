import splitxy
import argparse
import common
import customer

def get_customers(records, N):
  """ filter the customer_id with at least N purchases"""
  for row in records:
    if len(records[row]) >= N:
      yield row
    else:
      pass

def main():
  parser = argparse.ArgumentParser(description = 'Add more customers to training data');
  parser.add_argument('y_list_all_customers', nargs='?', default='interim/y-list-all-customers.csv')
  parser.add_argument('least_N_products', nargs='?', type=int, default=6)
  args = parser.parse_args()

  """records: a dict of form { customerid: [product1, product2, ...] }"""
  y_list_records = splitxy.load_y_with_cust(args.y_list_all_customers)
  y_records = get_customers(y_list_records, args.least_N_products)
  common.save_csv_i('interim/customers_with_6_products.csv', ([r] for r in y_records))

  """ union with publicChallenge.csv """
  public_challenge_records = customer.load_ids('data/publicChallenge.csv')
  union_records = set(y_records) | set(public_challenge_records)
  common.save_csv_i('interim/union_customers.csv', ([r] for r in union_records))
 
if __name__ == '__main__':
  main()
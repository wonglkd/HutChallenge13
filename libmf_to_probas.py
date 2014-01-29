from collections import defaultdict
import probas
import argparse

# A simple utilty to convert to probas
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('libmf_output_filename')
    parser.add_argument('-o', '--probas_filename')
    parser.add_argument('-c', '--customers_filename')
    parser.add_argument('-N', '--max-n', help='Max N for each customer that we will take', type=int, default=100)
    args = parser.parse_args()

    cust_probas = defaultdict(list)

    with open(args.libmf_output_filename, 'rb') as f:
        for line in f:
            customer_id, product, score = line.split()
            cust_probas[customer_id].append((product, float(score)))

    for k, tup in cust_probas.iteritems():
        cust_probas[k] = sorted(tup, key=lambda x:x[1], reverse=True)[:args.max_n]

    probas.save(cust_probas.values(), cust_probas.keys(), args.probas_filename)

if __name__ == "__main__":
    main()
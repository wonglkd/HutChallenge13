import common
import customer
import argparse
import csv
from pprint import pprint
from collections import Counter
from collections import defaultdict
import random
import bisect
# import networkx as nx
# from numpy.random import choice as np_choice
# from numpy import cumsum
# from numpy.random import rand
# import numpy as np

def nx_ppr(G, customers_to_predict, products, customers):
    per_template = { node: 0 for node in G }
    for c in customers_to_predict:
        per = per_template.copy()
        per[c] = 1
        # up to 1e-02 seemed to be okay
        pr = nx.pagerank_scipy(G, alpha=0.85 ,personalization=per,
            weight='weight', max_iter=100, tol=1e-03)
        ppr = sorted([(pr[product_id], product_id) for product_id in products], reverse=True)
        print c, ','.join(p[1:] for v, p in ppr[:6])
        #pprint(ppr[:20])

def weighted_choice(items, cumsums):
    rnd = random.random() * cumsums[-1]
    return items[bisect.bisect_right(cumsums, rnd)]

# def weighted_choice(items, probas):
#   return np_choice(items, p=probas)


# def weighted_choice(adj, total):
#   # choices = [(k, adj_dict['weight']) for k, adj_dict in adj.iteritems()]
#   # choices = adj.iteritems()
#   # total = sum(w for _, w in choices)

#   return np_choice(adj, p=adj.values())


#   r = random.uniform(0, total)
#   up_to = 0
#   for k, w in adj.iteritems():
#       if up_to + w >= r:
#           return k
#       up_to += w
#   assert False, "Problem"

def nx_load_data(edges_filename):
    G = nx.read_weighted_edgelist(edges_filename, delimiter=',', encoding='ascii')
    print G.size()

    products = set()
    customers = set()
    for node in G:
        if node.startswith('p'):
            products.add(node)
        else:
            customers.add(node)
    return customers, products, G

def load_adj_list(edges_filename):
    products = set()
    customers = set()
    G = defaultdict(list)
    G_w = defaultdict(list)
    with open(edges_filename, 'rb') as f:
        reader = csv.reader(f)
        for c, p, w in reader:
            customers.add(c)
            products.add(p)
            w = int(w)
            G[c].append(p)
            G_w[c].append(w)
            G[p].append(c)
            G_w[p].append(w)
    return customers, products, G, G_w

def predict(customers_to_predict, customers, G, G_w, walk_length, no_of_walks, N, output_filename):
    cumtotals = {}
    for v1, dt in G_w.iteritems():
        cum_sum = 0
        cum_sums = []
        for w in dt:
            cum_sum += w
            cum_sums.append(cum_sum)
        cumtotals[v1] = cum_sums

    with open(output_filename, "wb") as f:
        for start in customers_to_predict:
            if start not in customers:
                # common.print_err("Skipped, no data:", start)
                # print start[1:] + '|{}'
                f.write(start[1:] + '|{}\n')
                continue
            visited_counts = Counter()
            for _ in xrange(no_of_walks):
                curr = weighted_choice(G[start], cumtotals[start])
                for _ in xrange(walk_length):
                    visited_counts[curr] += 1
                    curr = weighted_choice(G[curr], cumtotals[curr])
                    curr = weighted_choice(G[curr], cumtotals[curr])
            total_cnts = sum(visited_counts.values())
            most_visited = ['"'+k[1:]+'":'+'{}'.format(v/float(total_cnts)) for k, v in visited_counts.most_common(N)]
            row_str = start[1:] + '|' + '{' + ','.join(most_visited) + '}'
            # print row_str
            f.write(row_str + "\n")
            # visited_counts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('edges_filename', default='interim/customer_product_counts.csv')
    parser.add_argument('customers_filename', default='data/publicChallenge.csv')
    parser.add_argument('-o', '--output', default='rwalks.probas')
    parser.add_argument('-l', '--walk-length', default=2, type=int)
    parser.add_argument('-w', '--no-walks', default=20, type=int)
    parser.add_argument('-N', '--top-n', default=20, type=int)
    args = parser.parse_args()

    # customers, products, G = nx_load_data(edges_filename)
    common.print_err("Loading...")
    customers, products, G, G_w = load_adj_list(args.edges_filename)
    common.print_err("Loaded")

    # customers_to_predict = customers

    # with open(customers_to_predict_filename, 'rb') as f:
    #   customers_to_predict = ['c'+cid.strip() for cid in f if cid.strip() != ""]
    customers_to_predict = customer.load_ids(args.customers_filename, add_prefix='c')

    # walk_length = 2
    # no_of_walks = 20 # 100

    predict(customers_to_predict, customers, G, G_w, args.walk_length, args.no_walks, args.top_n, args.output)

    # N = 6
    # N = 20

    # totals = { k : sum(x[1] for x in nadj) for k, nadj in G.iteritems() }
    # for v1, dt in G_w.iteritems():
    #   total = float(sum(dt))
    #   G_w[v1] = np.array([w/total for w in dt])


    # nx_ppr(G, customers_to_predict, products, customers)


if __name__ == "__main__":
    main()
import common
import json

def load(probas_filename):
	cust_probas = {}
	for line in common.load_file(probas_filename):
		if line.strip() == "":
			continue
		line = line.split("|")
		customer, probas = line
		probas = json.loads(probas)
		cust_probas[customer] = probas
	return cust_probas

def merge_dicts(dcts):
	all_keys = set()
	result = {}
	for dct in dcts:
		all_keys |= set(dct.keys())
	for k in all_keys:
		result[k] = sum(dct.get(k, 0) for dct in dcts)
	return result

def combine(list_of_probas):
	# simple summation
	all_customers = set()
	for pr in list_of_probas:
		all_customers |= set(pr.keys())

	combined_probas = {}
	for c in all_customers:
		combined_for_cust = {}
		all_probas_for_cust = []
		for probas in list_of_probas:
			if c in probas:
				all_probas_for_cust.append(probas[c])
		if len(all_probas_for_cust) > 1:
			combined_for_cust = merge_dicts(all_probas_for_cust)
		elif len(all_probas_for_cust) == 1:
			combined_for_cust = all_probas_for_cust[0]
		combined_probas[c] = combined_for_cust
	return combined_probas

def reweigh_dict(dct_of_dcts, factor):
	""" Multiply all values inside a dict of dicts by a factor """
	factor = float(factor)
	reweighted = {}
	for c, dct in dct_of_dcts.iteritems():
		reweighted[c] = { k: v * factor for k, v in dct.iteritems() }
	return reweighted

def get_predictions(probas, N=6, to_pad=None):
	""" Takes top 6 non-zero probabilities as labels.
		If < 6 items, pad with items from to_pad. """
	result = {}
	for customer, prob in probas.iteritems():
		ans = sorted(prob.iteritems(), key=lambda x:x[1], reverse=True)[:N]
		ans = [int(x[0]) for x in ans]
		for item in to_pad:
			if len(ans) >= N:
				break
			if item not in ans:
				ans.append(item)
		result[customer] = ans
	return result

def print_submission(result, customers_filename):
	for c in common.load_customers(customers_filename):
		print ','.join(map(str, result[c]))

def main():
	to_pad = [200,441,177,392,50,11]
	probas = load("gen/randomwalks.out")
	result = get_predictions(probas, to_pad=to_pad)
	print_submission(result, "data/publicChallenge.csv")

if __name__ == "__main__":
	main()
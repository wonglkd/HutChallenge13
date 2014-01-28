# should be fixed
CUSTOMERS_FILE = data/publicChallenge.csv
ACTUALS_FOR_SCORING = ../../interim/y-list.csv
SOL_TO_SCORE = sol.csv
# PRODUCT_CUSTOMER_EDGES_FILE = interim/customer_product_counts.csv
CUSTOMER_PRODUCT_COUNTS_FILE ?= $(ROOT_DIR)interim/products_by_test_customers_cnts.csv

## TO BE MODIFIED!
EXPERIMENT_NAME = walklen_1__nwalks_500
# RWALKS_PARAMS = --walk-length 1 --no-walks 500



# to be fixed
# PROBAS_TO_COMBINE = rwalks_$(EXPERIMENT_NAME).probas
# uncomment if you want to mix in probabilities from somewhere else
# PROBAS_TO_COMBINE += ../2014-01-21-rf-all/rf.probas


itembasedcf: itembasedcf_test.probas

include ../../Makefile
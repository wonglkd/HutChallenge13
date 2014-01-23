# should be fixed
CUSTOMERS_FILE = data/publicChallenge.csv
ACTUALS_FOR_SCORING = ../../interim/y-list.csv
SOL_TO_SCORE = sol.csv
PRODUCT_CUSTOMER_EDGES_FILE = interim/customer_product_counts.csv

## TO BE MODIFIED!
EXPERIMENT_NAME = nwalks_20__walklen_2
RWALKS_PARAMS = --walk-length 2 --no-walks 20

# to be fixed
PROBAS_TO_COMBINE = rwalks_$(EXPERIMENT_NAME).probas
# uncomment if you want to mix in probabilities from somewhere else
# PROBAS_TO_COMBINE += ../2014-01-19-newfeat-0.02/rf.probas
score:
sol: sol.csv
include ../../Makefile
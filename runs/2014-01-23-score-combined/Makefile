# should be fixed
CUSTOMERS_FILE = data/publicChallenge.csv
ACTUALS_FOR_SCORING = ../../interim/y-list.csv
PRODUCT_CUSTOMER_EDGES_FILE = interim/customer_product_counts.csv

## TO BE MODIFIED!
# EXPERIMENT_NAME = nwalks_20__walklen_2
# RWALKS_PARAMS = --walk-length 2 --no-walks 20

# EXPERIMENT_NAME = w_0.50__0.50
# PROBAS_PARAMS = -w 0.50 0.50

EXPERIMENT_NAME = hmean
# to be fixe
PROBAS_TO_COMBINE = rwalks.probas
# PROBAS_TO_COMBINE = rwalks_$(EXPERIMENT_NAME).probas
# uncomment if you want to mix in probabilities from somewhere else
PROBAS_TO_COMBINE += ../2014-01-21-rf-all/rf.probas
SOL_TO_SCORE = sol_$(EXPERIMENT_NAME).csv
score:
include ../../Makefile
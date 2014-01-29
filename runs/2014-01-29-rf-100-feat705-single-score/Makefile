# to be constant
CUSTOMERS_FILE = data/publicChallenge.csv
ACTUALS_FOR_SCORING = ../../interim/y-list.csv
PRODUCT_CUSTOMER_EDGES_FILE = interim/customer_product_counts.csv

## TO BE MODIFIED!
RWALKS_EXPERIMENT_NAME = walklen_1__nwalks_500
RWALKS_PARAMS = --walk-length 1 --no-walks 500

PROBAS_EXPERIMENT_NAME = w_0.55__0.45
PROBAS_PARAMS = -w 0.55 0.45

# to be held constant
# PROBAS_TO_COMBINE = rwalks_$(RWALKS_EXPERIMENT_NAME).probas
PROBAS_TO_COMBINE = ../2014-01-23-score-rw/rwalks_$(RWALKS_EXPERIMENT_NAME).probas
# uncomment if you want to mix in probabilities from somewhere else
# PROBAS_TO_COMBINE += ../2014-01-21-rf-all/rf.probas
PROBAS_TO_COMBINE += ../2014-01-29-rf-100-feat705-single/rf_direct.probas
SOL_TO_SCORE = sol_$(PROBAS_EXPERIMENT_NAME).csv

score:
include ../../Makefile
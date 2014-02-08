# should be fixed
CUSTOMERS_FILE = data/publicChallenge.csv
ACTUALS_FOR_SCORING = ../../interim/y-list.csv
SOL_TO_SCORE = sol.csv
PRODUCT_CUSTOMER_EDGES_FILE = interim/customer_product_counts.csv

## TO BE MODIFIED!
EXPERIMENT_NAME = walklen_1__nwalks_500
RWALKS_PARAMS = --walk-length 1 --no-walks 500

rw: rwalks_$(EXPERIMENT_NAME).probas
include ../../Makefile
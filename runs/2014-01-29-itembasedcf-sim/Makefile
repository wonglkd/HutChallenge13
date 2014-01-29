# should be fixed
CUSTOMERS_FILE = data/publicChallenge.csv
# CUSTOMER_PRODUCT_COUNTS_FILE ?= $(ROOT_DIR)interim/products_by_test_customers_cnts.csv
CUSTOMER_PRODUCT_COUNTS_FILE ?= $(ROOT_DIR)interim/products_by_all_customers_cnts.csv

## TO BE MODIFIED!
# ITEMBASEDCF_PARAMS = --similarity-func jaccard
# ITEMBASEDCF_EXPERIMENT_NAME = jaccard

# ITEMBASEDCF_PARAMS = --similarity-func cos
# ITEMBASEDCF_EXPERIMENT_NAME = cos

ITEMBASEDCF_PARAMS = --similarity-func cos_log
ITEMBASEDCF_EXPERIMENT_NAME = cos_log


itembasedcf: itembasedcf_$(ITEMBASEDCF_EXPERIMENT_NAME).probas

include ../../Makefile

ROOT_DIR ?= ../../

PRODUCT_CUSTOMER_EDGES_FILE ?= interim/customer_product_counts.csv

CUSTOMERS_TRAIN_FILE ?= $(CUSTOMERS_FILE)
# CUSTOMERS_TRAIN_FILE ?= data/all_customers.csv
CUSTOMERS_TEST_FILE ?= $(CUSTOMERS_FILE)
SOL_TO_SCORE ?= sol.csv
ACTUALS_FOR_SCORING ?= $(ROOT_DIR)interim/y-list.csv
CUSTOMER_PRODUCT_COUNTS_FILE ?= $(ROOT_DIR)interim/products_by_test_customers_cnts.csv
# CUSTOMER_PRODUCT_COUNTS_FILE ?= $(ROOT_DIR)interim/products_by_all_customers_cnts.csv

EXEC_PREFIX = time python

rf: rf.probas
gbm: gbm.probas
sgd: sgd.probas

.SECONDARY: rf-model.pkl gbm-model.pkl

x-orders.pkl y-list.csv x-customers-used.out x-skipped.out: $(ROOT_DIR)splitxy.py $(ROOT_DIR)$(CUSTOMERS_TRAIN_FILE)
	$(EXEC_PREFIX) $^ -x x-orders.pkl -y y-list.csv -c x-customers-used.out 2> x-skipped.out

all-orders.pkl all-customers-used.out: $(ROOT_DIR)customer.py $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)
	$(EXEC_PREFIX) $^ -o all-orders.pkl -c all-customers-used.out

all-features.pkl x-features.pkl: $(ROOT_DIR)features.py all-orders.pkl x-orders.pkl
	$(EXEC_PREFIX) $^ -o all-features.pkl x-features.pkl

# where % = {rf, gbm, sgd}
sgd-model.pkl rf-model.pkl gbm-model.pkl: %-model.pkl: $(ROOT_DIR)train.py x-features.pkl y-list.csv
	$(EXEC_PREFIX) $< -t x-features.pkl -y y-list.csv -o $@ --clf $* $(TRAIN_PARAMS) --params-filename params-clf.yaml

sgd.probas rf.probas gbm.probas: %.probas: $(ROOT_DIR)train.py all-features.pkl %-model.pkl
	$(EXEC_PREFIX) $< -p all-features.pkl -l $*-model.pkl -s $@

%-analyse: $(ROOT_DIR)train.py %-model.pkl
	$(EXEC_PREFIX) $< -l $*-model.pkl -a -f "feature-importances"`date "+_%Y%m%d-%H%M.txt"`

rwalks%.probas: $(ROOT_DIR)randomwalks.py $(ROOT_DIR)$(PRODUCT_CUSTOMER_EDGES_FILE) $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)
	$(EXEC_PREFIX) $^ $(RWALKS_PARAMS) -o $@

itembasedcf%.probas: $(ROOT_DIR)itembasedcf.py $(CUSTOMER_PRODUCT_COUNTS_FILE)
	$(EXEC_PREFIX) $^ -o $@

sol%.csv: $(ROOT_DIR)probas.py $(PROBAS_TO_COMBINE) $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)
	$(EXEC_PREFIX) $< $(PROBAS_TO_COMBINE) -c $(ROOT_DIR)$(CUSTOMERS_TEST_FILE) $(PROBAS_PARAMS) -o $@

score: $(ROOT_DIR)score.py $(ACTUALS_FOR_SCORING) $(SOL_TO_SCORE) $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)
	$(EXEC_PREFIX) $< $(ACTUALS_FOR_SCORING) $(SOL_TO_SCORE) -c $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)

clean:
	find . -name "*.npy" -maxdepth 1 -print0 | xargs -0 rm
	rm *.pkl *.npy *.out y-list.csv sol*.csv
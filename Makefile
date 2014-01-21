
ROOT_DIR ?= ../../

PRODUCT_CUSTOMER_EDGES_FILE ?= interim/customer_product_counts.csv

CUSTOMERS_TRAIN_FILE ?= $(CUSTOMERS_FILE)
# CUSTOMERS_TRAIN_FILE ?= data/all_customers.csv
CUSTOMERS_TEST_FILE ?= $(CUSTOMERS_FILE)

rf: rf.probas
gbm: gbm.probas

.SECONDARY: rf-model.pkl gbm-model.pkl

x-orders.pkl y-list.csv x-customers-used.out x-skipped.out: $(ROOT_DIR)splitxy.py $(ROOT_DIR)$(CUSTOMERS_TRAIN_FILE)
	python $^ -x x-orders.pkl -y y-list.csv -c x-customers-used.out 2> x-skipped.out

all-orders.pkl all-customers-used.out: $(ROOT_DIR)customer.py $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)
	python $^ -o all-orders.pkl -c all-customers-used.out

all-features.pkl x-features.pkl: $(ROOT_DIR)features.py all-orders.pkl x-orders.pkl
	python $^ -o all-features.pkl x-features.pkl

# where % = {rf, gbm}
rf-model.pkl gbm-model.pkl: %-model.pkl: $(ROOT_DIR)train.py x-features.pkl y-list.csv
	python $< -t x-features.pkl -y y-list.csv -o $@ --clf $* $(TRAIN_PARAMS)

%.probas: $(ROOT_DIR)train.py all-features.pkl %-model.pkl
	python $< -p all-features.pkl -l $*-model.pkl -s $@

%-analyse: $(ROOT_DIR)train.py %-model.pkl
	python $< -l $*-model.pkl -a -f "feature-importances"`date "+_%Y%m%d-%H%M.txt"`

rwalks.probas: $(ROOT_DIR)randomwalks.py $(ROOT_DIR)$(PRODUCT_CUSTOMER_EDGES_FILE) $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)
	python $^ > $@

sol.csv: $(ROOT_DIR)probas.py $(PROBAS_TO_COMBINE) $(ROOT_DIR)$(CUSTOMERS_TEST_FILE)
	python $< $(PROBAS_TO_COMBINE) -c $(ROOT_DIR)$(CUSTOMERS_TEST_FILE) $(PROBAS_PARAMS) -o $@

clean:
	find . -name "*.npy" -maxdepth 1 -print0 | xargs -0 rm
	rm *.pkl *.npy *.out y-list.csv
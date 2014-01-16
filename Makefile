
ROOT_DIR = ../../

all: rf.probas

x-orders.pkl y-list.csv x-customers-used.out x-skipped.out: $(ROOT_DIR)splitxy.py $(ROOT_DIR)$(CUSTOMERS_FILE)
	python $^ -x x-orders.pkl -y y-list.csv -c x-customers-used.out 2> x-skipped.out

all-orders.pkl all-customers-used.out: $(ROOT_DIR)customer.py $(ROOT_DIR)$(CUSTOMERS_FILE)
	python $^ -o all-orders.pkl -c all-customers-used.out

all-features.pkl x-features.pkl: $(ROOT_DIR)features.py all-orders.pkl x-orders.pkl
	python $^ -o all-features.pkl x-features.pkl

# %-features.pkl: $(ROOT_DIR)features.py %-orders.pkl
# 	python $^ -o $@

model.pkl: $(ROOT_DIR)train.py x-features.pkl y-list.csv
	python $< -t x-features.pkl -y y-list.csv -o $@

analyse: $(ROOT_DIR)train.py model.pkl
	python $< -l model.pkl -a

rf.probas: $(ROOT_DIR)train.py all-features.pkl model.pkl
	python $< -p all-features.pkl -l model.pkl -s $@

clean:
	find . -name "*.npy" -maxdepth 1 -print0 | xargs -0 rm
	rm *.pkl *.npy *.out y-list.csv
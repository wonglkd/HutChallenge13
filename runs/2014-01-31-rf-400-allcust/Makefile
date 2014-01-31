CUSTOMERS_FILE = data/publicChallenge.csv
TRAIN_PARAMS = --feature-select --use-only-feat ../../interim/feature-importances_20140129-2106_top705.txt
SPLIT_PARAMS = --splitter percent
all: rf_direct.probas rf.probas
rf:
include ../../Makefile

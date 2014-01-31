# to be constant
CUSTOMERS_FILE = data/publicChallenge.csv
ACTUALS_FOR_SCORING = ../../interim/timesplit_limited-ylist.csv
PRODUCT_CUSTOMER_EDGES_FILE = interim/customer_product_counts.csv

## TO BE MODIFIED!
RWALKS_EXPERIMENT_NAME = walklen_1__nwalks_500
RWALKS_PARAMS = --walk-length 1 --no-walks 500

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__without
# PROBAS_PARAMS = -w 0.55 0.45
# 0.399175551988

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.0
# PROBAS_PARAMS = -w 0.55 0.45 0.0
# MAP@6 = 0.399471203326

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.1
# PROBAS_PARAMS = -w 0.55 0.45 0.1
# 0.399471203326

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.2
# PROBAS_PARAMS = -w 0.55 0.45 0.2
# MAP@6 = 0.399471203326

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.3
# PROBAS_PARAMS = -w 0.55 0.45 0.3
# MAP@6 = 0.399458853073

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.4
# PROBAS_PARAMS = -w 0.55 0.45 0.4
# MAP@6 = 0.399433535054

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.5
# PROBAS_PARAMS = -w 0.55 0.45 0.5
# MAP@6 = 0.399324715601

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.6
# PROBAS_PARAMS = -w 0.55 0.45 0.6
# MAP@6 = 0.399176306725

# without
# MAP@6 = 0.399175551988

# PROBAS_EXPERIMENT_NAME = w_0.55__0.45__0.7
# PROBAS_PARAMS = -w 0.55 0.45 0.7
# MAP@6 = 0.398919695909

PROBA_PARAMS += --merge-func dicts
# PROBA_PARAMS += --merge-func ranklists

# to be held constant
# PROBAS_TO_COMBINE = rwalks_$(RWALKS_EXPERIMENT_NAME).probas
PROBAS_TO_COMBINE = ../2014-01-23-score-rw/rwalks_$(RWALKS_EXPERIMENT_NAME).probas
# PROBAS_TO_COMBINE = ../2014-01-23-score-rw/rwalks_$(RWALKS_EXPERIMENT_NAME).probas
# PROBAS_TO_COMBINE = ../2014-01-23-score-rw/rwalks_$(RWALKS_EXPERIMENT_NAME).probas
PROBAS_PARAMS = -w 4.0
# uncomment if you want to mix in probabilities from somewhere else
PROBAS_TO_COMBINE += ../2014-01-29-rf-100-feat705-single/rf_direct.probas
# PROBAS_TO_COMBINE += ../2014-01-30-rf-200-feat705/rf.probas
PROBAS_PARAMS += 4.0
PROBAS_TO_COMBINE += ../2014-01-30-rf-200-feat705/rf.probas
PROBAS_PARAMS += 4.0
# PROBAS_TO_COMBINE += ../2014-01-29-itembasedcf-sim/itembasedcf_jaccard.probas
# PROBAS_PARAMS += 0.4
# PROBAS_TO_COMBINE += ../2014-01-29-itembasedcf-sim/itembasedcf_cos_log.probas
# PROBAS_PARAMS += 0.01
# PROBAS_TO_COMBINE += ../../interim/libmf.probas
# PROBAS_PARAMS += 0.01
# SOL_TO_SCORE = sol_allmf_ranklists_dbl.csv

sol: sol_submit_ibcf.csv
	#sol_allmf_dicts_dbl.csv
score:
include ../../Makefile
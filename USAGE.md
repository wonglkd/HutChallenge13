USAGE
=======

INSTALL
-------
Download `db.sqlite3` and place it in the directory `db`:
- http://fi-de.net/ext/HutChallenge/db.sqlite3 OR
- https://dl.dropboxusercontent.com/s/lyunl683dhnzemo/db.sqlite3

Please also ensure that you have the scikit-learn library (>= 0.14.1) installed.


Quick start
-----------
Ensure that the db file has been placed in the right directory: see section INSTALL.

You can use the following instructions to generate a solution using
approximately the same parameters as our best submission.

Generate the probabilities from conducting random walks on the product-customer
graph:

```
cd runs/2014-reproduce-rw
make
```

This will generate a file with name in the format of
`feature-importances_{TIMESTAMP}.txt`.

```
cd runs/2014-reproduce-rf-0.02
make rf-analyse
```

Replace {TIMESTAMP} in the below command before running it
to extract the top 500 features.

```
head -n 501 feature-importances_{TIMESTAMP}.txt | tail -n 500 > feature-importances_{TIMESTAMP}-top500.txt
```

Open the file `runs/2014-reproduce-rf-all/Makefile` and modify the second line of the file
to replace it with `../2014-reproduce-rf-0.02/feature-importances_{TIMESTAMP}-top500.txt`.

Subsequently, run the random classifier. Note: classification and prediction
took ~35 mins and ~6 mins respectively on a 2.6 GHz Intel Core i5 with 16 GB of
RAM and SSD. Parallel processing is turned off by default due to instability
issues encountered, due to suspected inefficiencies with joblib's multithreading
function resulting in combination of multiple trees taking an extraordinary
amount of time on the typical laptop. We were however successfully able to
utilise parallel processing on a EC2 server, possibly because of the greater RAM
available.

```
cd runs/2014-reproduce-rf-all
make
```

This command combines the probabilities generated from the two classifiers.

```
cd runs/2014-reproduce-combine
make
```

This should yield you a solution CSV file.


How our best submission was produced
------------------------------------

Our best submission (0.165777) was produced as follows:
```
cd runs/2014-01-24-quick
make
```

This generated the submission file `sol_w_0.55__0.45_2.csv` by combining probabilites from:
1. Random Forest classifier (`2014-01-21-rf-all/rf.probas`)
2. Random walks (`2014-01-23-score-rw/walklen_1__nwalks_500.probas`)


Running existing experiment
---------------------------

```
cd runs/{EXPERIMENT_NAME}
make
```

There are two types of experiment directories, and thus Makefiles, present.

1. Classifier: this generates a `.probas` file (probabilities from a classifier).
2. Ensemble-merging: this generates a `sol.csv` file (predictions based on combining together multiple `.probas` files).

Setting up a new experiment
---------------------------
1. Make a new experiment directory in runs.
2. Create a Makefile for the directory. We recommend copying an existing
Makefile and modifying it to suit your needs.

    Sample Makefiles to copy from:
    - `runs/2014-01-21-rf-0.02/Makefile` (2% of dataset)
    - `runs/2014-01-21-rf-all/Makefile`
    
3. If running a classification-type Makefile, it is possible to specify the
parameters through the file `params-clf.yaml`. If it does not exist, it will
automatically be created with the default settings when you run the classifier.

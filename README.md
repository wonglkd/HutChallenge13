HutChallenge13
==============
* By **Team Cattywampus.**
    * (see bottom of file for team name explanation)
* An entry for the [Hut Challenge], a competition organised by [The Hut Group].
* Timeframe: 01 Dec 2013 - 31 Jan 2014.

About
-----
**An ensemble of multiple machine learning methods, including:**
* a random forest classifier that mines features from the orders.
* performing random walks on the product-customer graph.
* item-based collaborative filtering^
* matrix factorisation using [LIBMF]^
* (planned) SGD / other linear classifiers

^ _not used in highest-scoring submission ([e324d31])._

**Predictions for each customer**
* Cold start
    * For new customers with no order history / < 6 predictions made
        * Padded with the top 6 products bought by customers on their first order. `[200,392,500,316,47]`
* use each method to calculate a probability of each product being purchased by this customer
* combine the probabilities with optimised weightage
* rank the combined probabilities to output the top 6 products

See the more detailed write-up [doc/README.pdf] for more information.

Usage
=====
See [USAGE.md] for more information.

Prerequisites
=============
* Python 2.6+
* scikit-learn 0.14.1+
* yaml (3.10 was used)
* numpy (1.7.1 was used)
* scipy (0.13.2 was used)
* matplotlib (optional, for plotting feature importance graph; 1.3.1 was used)

What's in a name?
=================
See http://www.comp.nus.edu.sg/~leonghw/Courses/cattywampus.html

Team Cattywampus prior work: Top 25% in [KDD Cup 2013] by ACM SIGKDD, Microsoft & Kaggle ([KDD Cup repository]).

[Hut Challenge]:http://www.thehutchallenge.com/
[The Hut Group]:http://www.thehutgroup.com/
[KDD Cup 2013]:http://www.kaggle.com/c/kdd-cup-2013-author-disambiguation
[KDD Cup repository]:https://github.com/wonglkd/KDDCup13Track2/
[LIBMF]:http://www.csie.ntu.edu.tw/~cjlin/libmf/
[e324d31]:https://github.com/wonglkd/HutChallenge13/commit/e324d311a1a31392f319a5ec82036a74fdf3d66d
[USAGE.md]:USAGE.md
[doc/README.pdf]:doc/README.pdf?raw=true

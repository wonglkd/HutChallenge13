sqlite3 db.sqlite3

CREATE TABLE rec (customer INT, product INT, t, country TEXT);
.mode csv
.import ../data/train.noheader.csv rec

CREATE INDEX rec_customer_ind ON rec (customer);
CREATE INDEX rec_product_ind ON rec (product);
CREATE INDEX rec_country_ind ON rec (country);

CREATE TABLE subset (customer INT);
CREATE INDEX subset_ind ON subset (customer);
.mode csv
.import ../data/publicChallenge.csv subset
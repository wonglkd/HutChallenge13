
-- ## Find no. of orders for customers

-- # that are in publicChallenge.csv
-- (Seems inefficient)
-- SELECT COUNT(*) FROM rec NATURAL JOIN subset;  
-- (What I went with in the end)
.mode csv
.output customer_order_counts_test.csv
SELECT
	customer,
	(SELECT COUNT(*) FROM rec r WHERE r.customer = s.customer) as no_of_orders
FROM
	subset s;
.output stdout
-------------
-- # for all customers
.mode csv
.output customer_order_counts_all.csv
SELECT customer, COUNT(*) FROM rec
GROUP BY customer; 
.output stdout
-----------------------------------
-- ## General statistics
SELECT COUNT(DISTINCT customer) FROM rec;
SELECT COUNT(DISTINCT product) FROM rec;
SELECT COUNT(DISTINCT t) FROM rec;
SELECT COUNT(DISTINCT country) FROM rec;
SELECT COUNT(DISTINCT customer) FROM subset;
-----------------------------------
DROP TABLE t_orders_cnts_testcust IF EXISTS;
CREATE table t_orders_cnts_testcust AS
	SELECT
	customer,
	(SELECT COUNT(*) FROM rec r WHERE r.customer = s.customer) as no_of_orders
		FROM
	subset s;
CREATE INDEX t_orders_cnts_testcust_noo_ind ON t_orders_cnts_testcust (no_of_orders);
-----------------
DROP TABLE t_order_cnts_allcust IF EXISTS;
CREATE table t_order_cnts_allcust AS
	SELECT	
		customer,
		COUNT(*) as no_of_orders
	FROM rec
	GROUP BY customer;
CREATE INDEX t_order_cnts_allcust_noo_ind ON t_order_cnts_allcust (no_of_orders);
-----------------
.mode csv
.output orders_of_test_customers_1.csv
SELECT * FROM rec
WHERE customer IN (SELECT customer FROM t_orders_cnts_testcust WHERE no_of_orders = 1);
.output stdout
-------
.mode csv
.output orders_of_all_customers_1.csv
SELECT * FROM rec
WHERE customer IN (SELECT customer FROM t_order_cnts_allcust WHERE no_of_orders = 1);
.output stdout
------------------
CREATE TABLE t_customer_product_cnts AS
	SELECT customer, product, COUNT(*) as cnt FROM rec
	GROUP BY customer, product;
--------
.mode csv
.output products_by_test_customers_cnts.csv
SELECT subset.customer, tcpc.product, tcpc.cnt FROM
	subset LEFT JOIN t_customer_product_cnts tcpc ON subset.customer = tcpc.customer
;
.output stdout
---------
.mode csv
.output products_by_all_customers_cnts.csv
SELECT * FROM t_customer_product_cnts;
.output stdout
------------------
SELECT
	customer,
	(SELECT COUNT(*) FROM rec r WHERE r.customer = s.customer) as no_of_orders
FROM
	subset s;
-----------------------------------	
-- # No. of customers who had not made any orders in the past (new customers)
SELECT COUNT(*) FROM subset WHERE customer NOT IN (SELECT customer FROM rec);


SELECT customer, COUNT(*) FROM rec
WHERE customer IN (10999,75592,208531)
GROUP BY customer; 



SELECT customer, product, COUNT(*) FROM rec
WHERE customer = 270081
GROUP BY product
ORDER BY COUNT(*);

SELECT customer, t, COUNT(*) FROM rec
WHERE customer = 270081
GROUP BY t
ORDER BY t;

SELECT * FROM rec
WHERE customer = 270081
ORDER BY t;


----------
SELECT customer, COUNT(DISTINCT t) as torders FROM rec
NATURAL JOIN subset
GROUP BY customer; 


SELECT customer, COUNT(DISTINCT t) as torders FROM rec
GROUP BY customer; 
-----------
.mode csv
.output customer_product_counts.csv
SELECT 'c' || customer, 'p' || product, COUNT(*) as weight FROM rec
GROUP BY customer, product;
.output stdout
----------
.mode csv
.output first_buys.csv
SELECT * FROM 
rec,
(SELECT customer, MIN(t) as min_time FROM rec GROUP BY customer) a
WHERE a.customer = rec.customer AND t = min_time;
.output stdout
----------
.mode csv
.output product_popularity_in_test.csv
SELECT product, COUNT(*) FROM rec NATURAL JOIN subset GROUP BY product
ORDER BY COUNT(*) DESC;
.output stdout
---------
.mode list
.separator " "
.output customer_product_counts_all_mf.txt
SELECT customer, product, COUNT(*) as no_of_orders FROM rec GROUP BY customer, product;
.output stdout
-----
.mode list
.separator " "
.output customer_product_counts_all_binary_mf.txt
SELECT customer, product, 1 as no_of_orders FROM rec GROUP BY customer, product;
.output stdout
-------
.mode list
.separator " "
.output customer_product_counts_subset_mf.txt
SELECT customer, product, COUNT(*) as no_of_orders FROM rec NATURAL JOIN subset GROUP BY customer, product;
.output stdout
-----------------
.mode list
.separator " "
.output customer_product_template_mf.txt
SELECT testcustomers.customer, allproducts.product, cnts.no_of_orders FROM
((SELECT DISTINCT customer FROM subset) testcustomers
CROSS JOIN
(SELECT DISTINCT product FROM rec) allproducts)
LEFT JOIN
(SELECT customer, product, COUNT(*) as no_of_orders FROM rec NATURAL JOIN subset GROUP BY customer, product) cnts
ON testcustomers.customer = cnts.customer AND allproducts.product = cnts.product;
.output stdout
-----
.mode list
.separator " "
.output customer_product_template_subset_p_mf.txt
SELECT testcustomers.customer, allproducts.product, cnts.no_of_orders FROM
((SELECT DISTINCT customer FROM subset) testcustomers
CROSS JOIN
(SELECT DISTINCT product FROM rec NATURAL JOIN subset) allproducts)
LEFT JOIN
(SELECT customer, product, COUNT(*) as no_of_orders FROM rec NATURAL JOIN subset GROUP BY customer, product) cnts
ON testcustomers.customer = cnts.customer AND allproducts.product = cnts.product;
.output stdout

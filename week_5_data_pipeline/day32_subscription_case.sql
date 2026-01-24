# Retention rate in 7-days
WITH dates AS
(SELECT start_date, date, user_id
FROM (SELECT MIN(time::date) OVER(PARTITION BY user_id) as start_date, time::date as date, user_id
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
GROUP BY user_id, time) t1
WHERE EXTRACT(DOW FROM start_date) = 1)

SELECT date, COUNT(DISTINCT user_id) as count_orders, COUNT(DISTINCT user_id)::decimal / MAX(COUNT(DISTINCT user_id)) OVER(PARTITION BY start_date) as retention_rate
FROM dates
WHERE date BETWEEN '2022-08-29' AND '2022-09-04 23:59:59'
GROUP BY date, start_date

#LTV in 14-days
WITH first_order_date as
(SELECT MIN(time::date) OVER(PARTITION BY user_id) start_date, user_id, order_id
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
GROUP BY user_id, order_id, time),

price_per_ordering AS
(SELECT date, order_id, SUM(price) as price_per_orders
FROM (SELECT order_id, creation_time::date date, unnest(product_ids) as product_id
FROM orders) t1 JOIN products using (product_id)
GROUP BY date, order_id),

in_14d AS
(SELECT *
FROM first_order_date JOIN price_per_ordering using (order_id)
WHERE date <= start_date + INTERVAL '13 days'),

ltv_per_user AS (
SELECT user_id, SUM(price_per_orders) as ltv_in_14days
FROM in_14d
GROUP BY user_id)

SELECT AVG(ltv_in_14days) AS average_ltv
FROM ltv_per_user

#Churn in 14-day (my dataset have 14-days information, so churn rate is all my dataset)

WITH min_max_date AS
(SELECT MIN(time::date) as start_date, MAX(time::date) as last_date, user_id
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
GROUP BY user_id
ORDER BY user_id),

leave_stay_users AS
(SELECT user_id,
CASE WHEN last_date - start_date = 0 THEN 'leave'
ELSE 'retention'
END AS leave_retention_users
FROM min_max_date)

SELECT COUNT(user_id) FILTER(WHERE leave_retention_users = 'leave') as leave_users,
COUNT(user_id) FILTER(WHERE leave_retention_users = 'retention') as stay_users,
COUNT(user_id) FILTER(WHERE leave_retention_users = 'leave')::decimal / COUNT(user_id) FILTER(WHERE leave_retention_users = 'retention') AS churn_rate
FROM leave_stay_users
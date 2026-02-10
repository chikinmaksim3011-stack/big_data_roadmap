# The first sentence
WITH users_c_date as
(SELECT time::date date, user_id
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
GROUP BY time, user_id)

# DAU
SELECT date, COUNT(DISTINCT user_id) as dau
FROM users_c_date
GROUP BY date
# WAU
SELECT DATE_TRUNC('week', date) week_date, COUNT(DISTINCT user_id) as wau
FROM users_c_date
GROUP BY week_date

# The second sentence is retention_rate in Day 1 and Day 7. I'm limited my database because my database very small and start in Wednesday

WITH users_c_date as
(SELECT time::date date, MIN(time::date) OVER(PARTITION BY user_id) as start_date, user_id
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order') and time BETWEEN '2022-08-29' and '2022-09-04 23:59:59'
GROUP BY time, user_id),

users_numbers as(
SELECT date - start_date as day_number, date, start_date, user_id
FROM users_c_date
WHERE start_date = (SELECT MIN(start_date) FROM users_c_date))

SELECT date, COUNT(DISTINCT user_id)::decimal / MAX(COUNT(DISTINCT user_id)) OVER(PARTITION BY start_date) AS retention
FROM users_numbers
WHERE day_number IN (0,1,6)
GROUP BY date, start_date
ORDER BY date

# The third sentence is funnel from orders

WITH users_c_date as
(SELECT time::date date, user_id, COUNT(order_id) OVER(PARTITION BY user_id) as orders
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
GROUP BY time, user_id, order_id)

SELECT DATE_TRUNC('week',date) week, COUNT(DISTINCT user_id) as wau, COUNT(DISTINCT user_id) FILTER(WHERE orders > 1) as wau_with_1_order, COUNT(DISTINCT user_id) FILTER(WHERE orders > 2) as wau_with_2_order
FROM users_c_date
GROUP BY week
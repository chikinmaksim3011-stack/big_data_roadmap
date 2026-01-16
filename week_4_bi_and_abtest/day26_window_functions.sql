-- We find user's first order, last order and summary his orders.

SELECT DISTINCT user_id, MIN(time::date) OVER(PARTITION BY user_id) as first_order,
MAX(time::date) OVER(PARTITION BY user_id) as last_order,
COUNT(order_id) OVER(PARTITION BY user_id) as orders
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
ORDER BY user_id

-- We find how long has it been since the last order.

SELECT user_id, time::date order_dates, LAG(time::date,1) OVER(PARTITION BY  user_id ORDER BY time::date) as next_orders, time::date - LAG(time::date,1) OVER(PARTITION BY  user_id ORDER BY time::date) as how_long_time
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
ORDER BY user_id

-- We find Users with repeat order with in 7 days.

WITH returned_orders AS
(SELECT user_id, time::date order_dates, LAG(time::date,1) OVER(PARTITION BY  user_id ORDER BY time::date) as next_orders, time::date - LAG(time::date,1) OVER(PARTITION BY  user_id ORDER BY time::date) as how_long_time
FROM user_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order'))

SELECT DISTINCT user_id, MIN(how_long_time) OVER(PARTITION BY  user_id) as min_how_long_time
FROM returned_orders
WHERE how_long_time < 8 and how_long_time != 0
ORDER BY user_id
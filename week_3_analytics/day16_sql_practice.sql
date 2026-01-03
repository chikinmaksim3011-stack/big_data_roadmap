# Find summary orders where time more average time
SELECT COUNT(order_id) as count_orders
FROM orders
WHERE creation_time::time > (SELECT AVG(creation_time::time) FROM orders) and order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')

# Find funded amount from our database
WITH datetime AS
(SELECT creation_time::DATE as dt, COUNT(order_id) as count_orders
FROM orders
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
GROUP BY dt)
SELECT dt, SUM(count_orders) OVER(ORDER BY dt) as funded_amount
FROM datetime

# Find couriers, which creating more than 50 orders

WITH couriers AS
(SELECT courier_id, COUNT(order_id) as orders
FROM courier_actions
WHERE order_id NOT IN (SELECT order_id FROM user_actions WHERE action = 'cancel_order')
GROUP BY courier_id
ORDER BY courier_id)
SELECT courier_id, orders
FROM couriers
WHERE orders >= 50
ORDER BY orders DESC
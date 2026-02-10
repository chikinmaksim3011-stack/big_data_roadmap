## We are launching personalize recommendation for every customer.

We are wanting to do idea with frequently purchased items in frequently purchased stores. The buyer will receive a 20 percent discount on his/her products on our website and there will be free shipping when ordering from N amounts.

Our effect, which we want, is increase the number of orders (10%) and increase the average receipt (10%).

## Metrics

We need:

- Revenue per users
- Orders and his name/id
- Retention rate (in 1 and in 7 day)
- Churn rate

## Methodology 

Due to data availability (14-day window only), we cannot perform a true pre/post analysis. Instead, we simulate an A/B test by randomly assigning users to groups and comparing their behavior over the full period. This assumes that randomization balances user activity across groups. 

We analyzed:

- p-value for recommending to launch our innovation.
- z-test for how many our delta high with the random value.
- 95% CI for in what range find our value with correct 95%.

## Our data

Our data is our castle. So, we need data about:
- our orders for how product user buying a lot
- price for revenue
- users for retention and churn rate
- split in A and B group in Redash

The first, we will rely only on data on orders, without stores.

## Our conclusion

If p-value < 0.05 and our primary metrics are growing up 5%, we will launch this innovation.
If not, we won't launch.

## Limitations

- Due to data availability (14-day window only), we cannot perform a true pre/post analysis. Instead, we simulate an A/B test by randomly assigning users to groups and comparing their behavior over the full period.
- So, we don't need special event on our data, and we don't know, it's our innovation works good, or it's event affected by user. 
# Your task is to design a complete analytical pipeline.
We are launching a new feature — personalized recommendations.
We need to evaluate its impact on user behavior.
You have:
- Order information
- The ability to enrich them with external data (currency exchange rate, holidays, etc.)

## Business hypothesis
For example, our company is a delivery company. I can suggest an idea with frequently purchased items in frequently purchased stores. The buyer will receive a 20 percent discount on these stores on our website and there will be free shipping when ordering from N amounts.

Our effect, which we want, is increase the number of orders (10%) and increase the average receipt (10%).

## Data
#### I use data such as:

- Order and user information
- CSV data about which stores users buying his products

Also, I calculate how much unique subjects people uses our delivery app and I will divide the number of all subjects by the number of unique users per day.

## Metrics

We need primary metrics and guardrail metrics.

- In primary metrics we need to track average receipt, number of orders and revenue.

- In guardrail metrics we need to retention

## Methodology

We need an A/B-testing because we don't have an understanding of whether this innovation needs to be introduced or not, maybe everything is fine with us as it is.
Statistics significance we will check from calculations conversion, p-value, relative conversion and z-statistics. If p-value < 0.05, so our delta is statistics significance.

## Limitations
- If we calculate our metrics in Python or different virtual languages, we will encounter inaccurate results. The numbers cannot accurately show the value, so we use calculator on the Internet for calculate our metrics.

## Conclusion

We will introduce our innovation only if our primary metrics will give results, for example, more than 5% and p-value is less 0.05.

If our innovation will give a neutral or negative effect, we need to check our metrics, and we will finalize the project and launch a new A/B test.



import pandas as pd
import math
import plotly.express as px

p_control = 0.08
uplift = 0.15
p_treatment = p_control * (1 + uplift)
alpha = 0.05
power = 0.80

delta = (p_treatment - p_control)**2 # This is our delta convertion, we find an effect that we need more people, or it's enough.
variance_A = p_control * (1 - p_control)
variance_B = p_treatment * (1 - p_treatment)
variance = variance_A + variance_B # This is variance of our testing, how "noisy" our database in groups. If our variance high, our database needs to many people.
significance = 1.96 # How big should the difference be in order to consider it "statistically significant"?
statistic = 0.84 # How assuredly we want to find our effect?
balance = (significance + statistic)**2  # Balance between reliability and sensitivity.

# We need more people in our A/B testing if:
# Our delta and mistake of the first kind (alpha) is small
# Our variance and power is high

people_in_our_database = (balance * variance) / delta
people_in_our_database = math.ceil(people_in_our_database) # It's our conservative estimate (more data – more reliable)
date = people_in_our_database / 500
date = math.ceil(date)
print(f"=== SAMPLE SIZE CALCULATION === \nBaseline conversion: {p_control * 100}% \nTarget conversion: {p_treatment * 100}% \nMinimal detectable uplift: {uplift*100}% \nRequired sample per group: {people_in_our_database} users \nTotal sample needed: 2*{people_in_our_database}={people_in_our_database*2} users \nAt 1000 new users/day → test duration: {date} days")


uplifts = [i for i in range(5, 30, 2)]
sample_sizes = []
for z in uplifts:
    p_treatment = p_control * (1 + (z/100))
    variance_B = p_treatment * (1 - p_treatment)
    people = ((((significance + statistic)**2) * ((p_control * (1 - p_control)) + p_treatment * (1 - p_treatment))) / (p_treatment - p_control)**2)
    people = math.ceil(people)
    sample_sizes.append(people)
df = pd.DataFrame({"Uplifts in %": uplifts, "Sample Sizes": sample_sizes})

fix = px.line(df, x="Sample Sizes", y="Uplifts in %", title='Required Sample Size vs Minimal Detectable Uplift', labels={'uplift': 'Uplift (relative)', 'sample_size_per_group': 'Users per group'})

fix.write_html('sample_size_vs_uplift.html')

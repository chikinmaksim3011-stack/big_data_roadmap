from scipy.stats import norm
import math

n_A = 50000
conversions_A = 4120
n_B = 50000
conversions_B = 4480

p_A = conversions_A / n_A # conversion (%)
p_B = conversions_B / n_B # conversion (%)
uplift_abs = p_B - p_A # delta
uplift_rel = uplift_abs / p_A # in products
p_pooled = (conversions_A + conversions_B) / (n_A + n_B) # It's % when find out if it's random our data grow up, or it's real data.
z_test = (p_B - p_A) / math.sqrt((p_pooled * (1 - p_pooled)) * ((1/n_A) + (1/n_B))) # This is z-statistics.

p_value = 2 * (1 - norm.cdf(abs(z_test)))
diff = p_B - p_A
se = math.sqrt(((p_A * (1 - p_A)) / n_A) + ((p_B * (1 - p_B)) / n_B))
CI_lower = diff - 1.96 * se
CI_upper = diff + 1.96 * se

def p (p_value):
    if p_value < 0.05:
        return '✅ Statistically significant (p < 0.05) → RECOMMEND TO LAUNCH'
    else:
        return '❌ Not statistically significant (p >= 0.05) → DO NOT LAUNCH'

print(f"=== A/B TEST RESULTS ANALYSIS === \nGroup A: {conversions_A} / {n_A} → {p_A*100:.2f}% \nGroup B: {conversions_B} / {n_B} → {p_B*100:.2f}% \nUplift: {uplift_abs*100:.2f}% (abs), {uplift_rel*100:.2f}% (rel) \nZ-statistic: {z_test:.2f} \nP-value: {p_value:.5f} \n95% CI for difference: [{CI_lower*100:.4f}, {CI_upper*100:.4f}] \nConclusion: {p(p_value)}")
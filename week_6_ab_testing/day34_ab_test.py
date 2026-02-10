# Generate synthetic A/B test data for conversion rate analysis
import pandas as pd
import numpy as np

np.random.seed(42)  # for reproducibility

n_users = 10000
group = np.random.choice(['A', 'B'], size=n_users, p=[0.5, 0.5])

# Realistic conversion rates: A = 8%, B = 9.5% (small uplift)
conversion_A = 0.08
conversion_B = 0.095

converted = []
for g in group:
    p = conversion_A if g == 'A' else conversion_B
    converted.append(np.random.binomial(1, p))

df = pd.DataFrame({
    'user_id': range(1, n_users + 1),
    'group': group,
    'converted': converted
})

# Optional: save to disk for transparency
df.to_csv('ab_test_data.csv', index=False)
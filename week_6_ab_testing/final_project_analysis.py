import pandas as pd
import numpy as np
from scipy.stats import norm
df = pd.read_csv('orders.csv')

unique_users = df['user_id'].unique()
np.random.seed(42)
np.random.shuffle(unique_users)
n = len(unique_users)
split_index = n // 2
group_A_users = unique_users[:split_index]
group_B_users = unique_users[split_index:]
user_to_group = {}
for user in group_A_users:
    user_to_group[user] = 'A'
for user in group_B_users:
    user_to_group[user] = 'B'

df['ab_group'] = df['user_id'].map(user_to_group)

# Average orders per users
users_orders = df.groupby(['ab_group', 'user_id'])['order_id'].count().reset_index(name='orders')
count_orders = users_orders.groupby('ab_group')['orders'].agg(mean='mean',
    std='std',
    n='count'
).reset_index()
count_orders_A_mean = count_orders.loc[count_orders['ab_group'] == 'A', 'mean'].iloc[0]
count_orders_B_mean = count_orders.loc[count_orders['ab_group'] == 'B', 'mean'].iloc[0]
count_orders_A_std = count_orders.loc[count_orders['ab_group'] == 'A', 'std'].iloc[0]
count_orders_B_std = count_orders.loc[count_orders['ab_group'] == 'B', 'std'].iloc[0]
count_orders_A_n = count_orders.loc[count_orders['ab_group'] == 'A', 'n'].iloc[0]
count_orders_B_n = count_orders.loc[count_orders['ab_group'] == 'B', 'n'].iloc[0]


# Revenue per user
users_revenue = df.groupby(['ab_group', 'user_id'])['price'].sum().reset_index(name='prices')
revenue_per_user = users_revenue.groupby('ab_group')['prices'].agg(mean='mean',
    std='std',
    n='count'
).reset_index()
revenue_per_user_A_mean = revenue_per_user.loc[revenue_per_user['ab_group'] == 'A', 'mean'].iloc[0]
revenue_per_user_B_mean = revenue_per_user.loc[revenue_per_user['ab_group'] == 'B', 'mean'].iloc[0]
revenue_per_user_A_std = revenue_per_user.loc[revenue_per_user['ab_group'] == 'A', 'std'].iloc[0]
revenue_per_user_B_std = revenue_per_user.loc[revenue_per_user['ab_group'] == 'B', 'std'].iloc[0]
revenue_per_user_A_n = revenue_per_user.loc[revenue_per_user['ab_group'] == 'A', 'n'].iloc[0]
revenue_per_user_B_n = revenue_per_user.loc[revenue_per_user['ab_group'] == 'B', 'n'].iloc[0]

# Retention rate
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')
first_activity = df.groupby('user_id')['date'].min().reset_index()
first_activity.columns = ['user_id', 'first_day']
user_days = df.groupby('user_id')['date'].apply(set).reset_index()
user_days.columns = ['user_id', 'active_days']
retention_data = first_activity.merge(user_days, on='user_id')
max_date = df['date'].max()

# Retention in 1 day
results = []
for group in ['A', 'B']:
    group_users = df[df['ab_group'] == group]['user_id'].unique()
    cohort = retention_data[retention_data['user_id'].isin(group_users)].copy()

    cohort_d1 = retention_data[
        retention_data['first_day'] <= max_date - pd.Timedelta(days=1)
        ].copy()

    cohort_d1['returned_d1'] = cohort_d1.apply(
        lambda row: (row['first_day'] + pd.Timedelta(days=1)) in row['active_days'],
        axis=1
    )
    retention_d1 = cohort_d1['returned_d1'].mean()
# Retention in 7 day
    cohort_d7 = cohort[cohort['first_day'] <= max_date - pd.Timedelta(days=7)].copy()
    cohort_d7['returned_d7'] = cohort_d7.apply(
        lambda row: ((row['first_day'] + pd.Timedelta(days=7)) in row['active_days']
        ),
        axis=1
    )
    retention_d7 = cohort_d7['returned_d7'].mean()
    results.append({
        'ab_group': group,
        'Day_1_Retention': retention_d1,
        'Day_7_Retention': retention_d7,
        'Cohort D1 size': len(cohort_d1),
        'Cohort D7 size': len(cohort_d7)
        })
retention_df = pd.DataFrame(results)
ret_A = retention_df.loc[retention_df['ab_group'] == 'A'].iloc[0]
ret_B = retention_df.loc[retention_df['ab_group'] == 'B'].iloc[0]

# Churn rate
churn_by_group = users_orders[users_orders['orders'] == 1].groupby('ab_group').size()
users_count_with_one_order_A = churn_by_group.get('A', 0)
users_count_with_one_order_B = churn_by_group.get('B', 0)

# Z-test for average orders per users
se = np.sqrt((count_orders_A_std**2 / count_orders_A_n) + (count_orders_B_std**2 / count_orders_B_n))
z = (count_orders_B_mean - count_orders_A_mean) / se
# P-value for average orders per users
p_value = 2 * (1 - norm.cdf(abs(z)))
# CI for average orders per users
CI_min = (count_orders_B_mean - count_orders_A_mean) - 1.96 * se
CI_max = (count_orders_B_mean - count_orders_A_mean) + 1.96 * se

# Z-test for revenue per user
se_rev = np.sqrt((revenue_per_user_A_std**2 / revenue_per_user_A_n) + (revenue_per_user_B_std**2 / revenue_per_user_B_n))
z_rev = (revenue_per_user_B_mean - revenue_per_user_A_mean) / se_rev
# P-value for revenue per user
p_value_rev = 2 * (1 - norm.cdf(abs(z_rev)))
# CI for revenue per user
CI_min_rev = (revenue_per_user_B_mean - revenue_per_user_A_mean) - 1.96 * se_rev
CI_max_rev = (revenue_per_user_B_mean - revenue_per_user_A_mean) + 1.96 * se_rev

def sigh(p_value):
    if p_value < 0.05:
        return 'SIGNIFICANT'
    else:
        return 'NOT SIGNIFICANT'

def sigh_rev(p_value_rev):
    if p_value_rev < 0.05:
        return 'SIGNIFICANT'
    else:
        return 'NOT SIGNIFICANT'

def recommendation(p_value_rev, p_value):
    if p_value_rev < 0.05 and p_value < 0.05:
        return '✅ LAUNCH'
    else:
        return '❌ DO NOT LAUNCH — otherwise'

print(f"=== FINAL PROJECT: PERSONALIZED RECOMMENDATIONS ===\nGroup A (Control): \n- Revenue per user: {revenue_per_user_A_mean:.2f}\n- Orders per user: {count_orders_A_mean:.2f} \n- Retention D1: {ret_A['Day_1_Retention']*100:.2f}%, D7: {ret_A['Day_7_Retention']*100:.2f}% \nGroup B (Test):\n- Revenue per user: {revenue_per_user_B_mean:.2f} \n- Orders per user: {count_orders_B_mean:.2f}\n- Retention D1: {ret_B['Day_1_Retention']*100:.2f}%, D7: {ret_B['Day_7_Retention']*100:.2f}% \nStatistical significance: \n- Revenue per user: p = {p_value_rev:.2f} → {sigh_rev(p_value_rev)} \n Orders per user: p = {p_value:.2f} → {sigh(p_value)} \nRecommendation: \n{recommendation(p_value, p_value_rev)}")


import pandas as pd

df = pd.read_csv('../Our Datasets/orders.csv')
dataframe = pd.read_csv('exchange_rates.csv')
df['creation_time'] = pd.to_datetime(df['creation_time'], format='%d/%m/%y %H:%M').dt.floor('D')
df['creation_time'].sort_values()
dataframe['creation_time'] = pd.to_datetime(dataframe['creation_time'], format='%Y-%m-%d').dt.floor('D')
new_data = pd.merge(df, dataframe, how='left', on='creation_time')
new_data.to_csv('orders_with_exchange.csv', index=True)

mean_USD = dataframe['USD_RUB'].mean()
print(mean_USD)
summary = new_data['order_id'].isnull().sum()
print(summary)

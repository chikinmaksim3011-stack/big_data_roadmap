import pandas as pd
import plotly.express as px

df = pd.read_csv('../Our Datasets/orders.csv')
df['creation_time'] = pd.to_datetime(df['creation_time'],format='%d/%m/%y %H:%M').dt.floor('D')
df['creation_time'] = df['creation_time'].sort_values()
daily_count = df.groupby(df['creation_time']).size().reset_index(name='orders_count')
daily_count['ma_7'] = daily_count['orders_count'].rolling(window=7).mean()

fig = px.line(daily_count, x='creation_time', y='orders_count', labels={'creation_time': 'Date', 'orders_count': 'Number of Orders'}, title='7-day moving average', template='plotly_white')
fig.add_scatter(x=daily_count['creation_time'], y=daily_count['ma_7'], line=dict(color='red'), name='7-Day Moving Average')
fig.write_html('interactive_time_series.html')

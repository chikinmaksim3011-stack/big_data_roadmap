from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px

df = pd.read_csv('../Our Datasets/revenue_and_users.csv')
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')

dau = px.line(df, x='date', y='dau', labels={'dau': 'Number of Unique Active Users'})
revenue_users = px.line(df, x='date', y='revenue_per_users', labels={'revenue_per_users': 'Revenue per User'})

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Our results afterwards 2 weeks ago', style={'textAlign': 'center'}),
    dcc.Graph(figure=dau),
    dcc.Graph(figure=revenue_users),
    html.H2('Our KPI:', style={'textAlign': 'center'}),
    html.H3(f'Average DAU: {df["dau"].mean():.2f}'),
    html.H4(f'Average Revenue per Users: {df["revenue_per_users"].mean():.2f}')
])
if __name__ == '__main__':
    app.run(debug=True)
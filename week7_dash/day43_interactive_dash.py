from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

data_revenue = pd.read_csv('../Our Datasets/revenue_and_users.csv')
data_revenue['date'] = pd.to_datetime(data_revenue['date'], format='%d/%m/%y')

min_date = data_revenue['date'].min()
max_date = data_revenue['date'].max()

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Interactive Dash App', style={'textAlign': 'center'}),
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed = min_date,
        max_date_allowed = max_date,
        start_date=min_date,
        end_date=max_date,
        display_format='DD/MM/YYYY'),
    html.Div(id='kpi-output', style={'textAlign': 'center'}),
    dcc.Graph(id='graph-dau'),
    dcc.Graph(id='graph-revenue-users')
])

@app.callback(
    Output('kpi-output', 'children'),
    Output('graph-dau', 'figure'),
    Output('graph-revenue-users', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))

def update_dashboard(start_date, end_date):
    if not start_date or not end_date:
        return 'Choose date:', {}, {}, {}

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # Filter
    filtered = data_revenue[(data_revenue['date'] >= start) & (data_revenue['date'] <= end)]
    if filtered.empty:
        return 'Not date in this period', {}, {}, {}

    # KPI
    avg_dau = filtered['dau'].mean()
    avg_revenue = filtered['revenue_per_users'].mean()

    kpi_text = [
        html.Div(f'Average DAU in this period: {avg_dau:.0f}'),
        html.Div(f'Average Revenue per users in this period: {avg_revenue:.2f}')
    ]

    # Graphics
    dau = px.line(filtered, x='date', y='dau', title='DAU')
    revenue_per_users = px.line(filtered, x='date', y='revenue_per_users', title='Revenue per Users')
    return kpi_text, dau, revenue_per_users

if __name__ == '__main__':
    app.run(debug=True)








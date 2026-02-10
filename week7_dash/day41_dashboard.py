import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

dataframe_revenue = pd.read_csv('../Our Datasets/revenue_and_users.csv')

dataframe_revenue['date'] = pd.to_datetime(dataframe_revenue['date'], format='%d/%m/%y')


min_date = dataframe_revenue['date'].min()
max_date = dataframe_revenue['date'].max()

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Interactive Dashboard', style={'textAlign': 'center'}),
    html.Div([
    dcc.DatePickerRange(id='date-filter',
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
            display_format='DD/MM/YY'
        )], style={'margin': '20px', 'textAlign': 'center'}),
html.Div(id='kpi-output', style={'margin': '20px', 'textAlign': 'center'}),
dcc.Graph(id='dau-graph'),
dcc.Graph(id='revenue-graph') ])

@app.callback(
    Output('kpi-output', 'children'),
    Output('dau-graph', 'figure'),
    Output('revenue-graph', 'figure'),
    Input('date-filter', 'start_date'),
    Input('date-filter', 'end_date')
)

def update_dashboard(start_date, end_date):
    if not start_date or not end_date:
        return "Выберите период", {}, {}

    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    filtered = dataframe_revenue[(dataframe_revenue['date'] >= start) & (dataframe_revenue['date'] <= end)]

    if filtered.empty:
        return "No data in this range", {}, {}

    # KPI
    avg_dau = filtered['dau'].mean()
    avg_revenue_per_user = filtered['revenue_per_users'].mean()

    kpi_text = [
        html.P(f"Средний DAU: {avg_dau:.0f}"),
        html.P(f"Средняя выручка на пользователя: {avg_revenue_per_user:.2f} ₽")
    ]

    # График DAU
    fig_dau = px.line(
        dataframe_revenue,
        x='date',
        y='dau',
        title='DAU (Daily Active Users)',
        markers=True
    )
    fig_dau.update_xaxes(tickformat='%d/%m')

    # График выручки на пользователя
    fig_rev = px.line(
        dataframe_revenue,
        x='date',
        y='revenue_per_users',
        title='Выручка на пользователя',
        markers=True
    )
    fig_rev.update_xaxes(tickformat='%d/%m')

    return kpi_text, fig_dau, fig_rev


# === 4. Запуск ===
if __name__ == '__main__':
    app.run(debug=True)


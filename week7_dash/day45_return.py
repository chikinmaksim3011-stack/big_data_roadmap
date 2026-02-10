from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('../Our Datasets/revenue_and_users.csv')
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')
df['dau'] = pd.to_numeric(df['dau'], errors='coerce')

min_dau = df['dau'].min()
max_dau = df['dau'].max()

app = Dash(__name__)
app.layout = html.Div([
    html.H1('Interactive DAU with filter in DAU', style={'textAlign': 'center'}),
    dcc.Slider(
        id='dau-slider',
        min=min_dau,
        max=max_dau,
        step=500
    ),
    dcc.Graph(id='dau-graph'),
    html.Div(id='kpi')]
)

@app.callback(
    Output('dau-graph', 'figure'),
    Output('kpi', 'children'),
    Input('dau-slider', 'value')
)
def update_figure(value):

    filtered = df[df['dau'] >= value]
    if filtered.empty:
        return {}, "No data in this period"

    # KPI
    avg_dau = filtered['dau'].mean()
    kpi_text = [
        html.Div(f'Average DAU for {filtered['dau'].count()} days'),
        html.Div(f'Average DAU per User: {avg_dau:.2f}')
                ]
    fig_dau = px.line(filtered, x='date', y='dau', title='DAU')

    return fig_dau, kpi_text
if __name__ == '__main__':
    app.run(debug=True)
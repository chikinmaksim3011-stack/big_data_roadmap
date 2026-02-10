import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc


revenue_users = pd.DataFrame({'group':['A','B'],
                             'revenue_per_user': [1026.85, 1029.21]})

retention_rate = pd.DataFrame({'group': ['A','B','A', 'B'],
                               'day': ['D1 Retention','D1 Retention','D7 Retention','D7 Retention'],
                               'retention_%': [0.1718, 0.1718, 0.1265, 0.1209]})

p_value = 0.83

revenue_plot = px.bar(revenue_users,x='group',y='revenue_per_user', title='Revenue per User')
retention_plot = px.bar(retention_rate, x='day', y='retention_%', title='Retention Rate', color='group', barmode='group', text='retention_%')

retention_plot.update_traces(
    texttemplate='%{text:.1%}',
    textposition='outside' # transformation from float to percent values
)

retention_plot.update_yaxes(tickformat='.0%', range=[0, 0.2])

app = Dash(__name__)
app.layout = html.Div([
    html.H1("A/B Test Results — Personalized Recommendations", style={'textAlign': 'center'}),
    html.Div([
        dcc.Graph(figure=revenue_plot),
        html.B("Revenue per Users:"), # bold font
        html.P("Group A: 1026.85 "),
        html.P("Group B: 1029.21 "),
        html.P("p_value: 0.83 -> not significant")
    ]),
    html.Div([
        dcc.Graph(figure=retention_plot),
        html.H2("Recommendation: Do not launch — no statistically significant effect.", style={'textAlign': 'center'})
    ])
])
if __name__ == '__main__':
    app.run(debug=True)

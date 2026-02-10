import pandas as pd
import plotly.express as px
from jinja2 import Template

data_revenue = pd.read_csv('../Our Datasets/revenue_and_users.csv')
data_revenue['date'] = pd.to_datetime(data_revenue['date'], format='%d/%m/%y')

avg_dau = round(data_revenue['dau'].mean(),2)
avg_revenue = round(data_revenue['revenue_per_users'].mean(),2)

dau = px.line(data_revenue, x='date', y='dau', title='DAU')
revenue_per_users = px.line(data_revenue, x='date', y='revenue_per_users', title='Revenue per Users')

dau_html = dau.to_html(full_html=False, include_plotlyjs='cdn')
revenue_html = revenue_per_users.to_html(full_html=False, include_plotlyjs='cdn')

with open('report_template.html', 'r', encoding='utf-8') as f:
    template_str = f.read()

template = Template(template_str)
data_to_html = template.render(avg_dau=avg_dau,
                               avg_revenue=avg_revenue,
                               dau_graph=dau_html,
                               revenue_graph=revenue_html)

with open('report.html', 'w', encoding='utf-8') as f:
    f.write(data_to_html)

print("✅ Отчёт сохранён как report.html")
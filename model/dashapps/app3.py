from types import new_class
from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from datetime import timedelta

import plotly.express as px


import numpy as np
tab_style = { "padding": "1.3vh","color": '#AEAEAE',"fontSize": '30px',"backgroundColor": 'fuchsia','border-bottom': '1px white solid',}
tab_selected_style = {"fontSize": '30px',"color": '#F4F4F4',"padding": "1.3vh",'fontWeight': 'bold',"backgroundColor": 'pink','border-top': '1px white solid','border-left': '1px white solid','border-right': '1px white solid','border-radius': '0px 0px 0px 0px',}

tabs_styles = {
    'height': '18px'
}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app3=DjangoDash('Segmentandtrimaps', external_stylesheets=external_stylesheets)
colors=['#fae588','#f79d65','#f9dc5c','#e8ac65','#e76f51','#ef233c','#b7094c'] 
def label_rfm_segments(df):
    if df['score'] >= 9:
        return 'Cant Loose Them'
    elif ((df['score'] >= 8) and (df['score'] < 9)):
        return 'Champions'
    elif ((df['score'] >= 7) and (df['score'] < 8)):
        return 'Loyal'
    elif ((df['score'] >= 6) and (df['score'] < 7)):
        return 'Potential'
    elif ((df['score'] >= 5) and (df['score'] < 6)):
        return 'Promising'
    elif ((df['score'] >= 4) and (df['score'] < 5)):
        return 'Needs Attention'
    else:
        return 'Others'
def join_rfm(x): return str(x['R']) + str(x['F']) + str(x['M'])
df1 =pd.read_excel('data/Retail_kaggle.xlsx',parse_dates=['InvoiceDate'])
df=df1.copy()
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df.dropna()
df['Total'] = df['Quantity'] * df['UnitPrice']
day_date = df['InvoiceDate'].max() + timedelta(days=1)
df_process = df.groupby(['CustomerID']).agg({
                'InvoiceDate': lambda x: (day_date - x.max()).days,
                'InvoiceNo': 'count',
                'Total': 'sum'})
df_process.rename(columns={'InvoiceDate': 'Recence',
                                'InvoiceNo': 'Frequence',
                                'Total': 'Monnaie'}, inplace=True)
r_labels = range(4, 0, -1); f_labels = range(1, 5);m_labels = range(1, 5)
r_groups = pd.qcut(df_process['Recence'], q=4, labels=r_labels)
f_groups = pd.qcut(df_process['Frequence'], q=4, labels=f_labels)
df_process = df_process.assign(R = r_groups.values, F = f_groups.values)
m_groups = pd.qcut(df_process['Monnaie'], q=4, labels=m_labels)
df_process = df_process.assign(M = m_groups.values)
df_process['rfm_Concat'] = df_process.apply(join_rfm, axis=1)

rfm_count_unique = df_process.groupby('rfm_Concat')['rfm_Concat'].nunique()
df_process['score'] = df_process[['R','F','M']].sum(axis=1)
df_process['RFM_Level'] = df_process.apply(label_rfm_segments, axis=1)
df_process.reset_index(inplace=True)
rfm_level_agg = df_process.groupby('RFM_Level').agg({'Recence': 'mean','Frequence': 'mean','Monnaie': 'mean'}).round(1)

rfm_level_agg.reset_index(inplace = True)

df_mod = df_process[['CustomerID', 'score', 'RFM_Level','Recence','Frequence','Monnaie']]
df_norm = df[['CustomerID', 'Country']]
df_norm.drop_duplicates(subset = ['CustomerID'], inplace=True)
df_final = pd.merge(df_mod, df_norm, on='CustomerID', how='left')
df_graph = df_final[['Country','RFM_Level']].copy()
df_graph['RFM_Level_cnt'] = df_graph.groupby(['Country','RFM_Level'])['Country'].transform('count')
df_graph.drop_duplicates(['Country', 'RFM_Level','RFM_Level_cnt'], inplace=True)
df_graph.sort_values(by = ['Country'], inplace=True)
df_graph.reset_index()
app3.layout = html.Div([
    html.H3('Segmentation and Treemaps',style={'textAlign': 'center'}),
    dcc.Tabs(id="tabs-example-graph", value='tab1', children=[
        dcc.Tab(label='Segmentation', value='tab1',style=tab_style,selected_style = tab_selected_style),
        dcc.Tab(label='Treemaps', value='tab2',style=tab_style,selected_style = tab_selected_style),
       
    ]),
    html.Div(id='tabs-content-example-graph')
])
@app3.callback(Output('tabs-content-example-graph', 'children'),
              Input('tabs-example-graph', 'value'))
def render_content(tab):
    if tab == 'tab1':
        fig = px.pie(df_graph, values='RFM_Level_cnt', names='RFM_Level', template="ggplot2")
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
        fig.update_layout(legend=dict(
                orientation="h",))
        return html.Div([
            html.H4('Segmentation'),
            dcc.Graph(figure=fig, config={"displayModeBar":False}),
             
            ])
    else:
        fig = px.treemap(df_graph, path=['RFM_Level'],values='RFM_Level_cnt', width=900, height=400)
        fig.update_layout(treemapcolorway = colors, #defines the colors in the treemap
               margin = dict(t=50, l=25, r=25, b=25))
        return html.Div([
            html.H4('Treemaps'),
            dcc.Graph(figure=fig, config={"displayModeBar":False}),
          
            
            ])
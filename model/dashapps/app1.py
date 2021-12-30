from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
import pandas as pd
from dash import dash_table
#import namegenerator
import openpyxl
import numpy as np
import plotly.express as px


##css load
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app1=DjangoDash('Entete', external_stylesheets=external_stylesheets)
##append css
app1.css.append_css({ "external_url" : "/static/model/css/s1.css" })
df1 =pd.read_excel('data/Retail_kaggle.xlsx',engine="openpyxl")
df=df1.copy()
df=df.drop_duplicates()
df = df[(df['Quantity']>0)]
df = df [['CustomerID','Description','InvoiceDate','InvoiceNo','Quantity','UnitPrice', 'Country']]
df['TotalPurchase'] = df['Quantity'] *df['UnitPrice']
df_group = df.groupby(['CustomerID','Country']).agg({'InvoiceDate': lambda date: (date.max() - date.min()).days,
                                        'InvoiceNo': lambda num: len(num),
                                        'Quantity': lambda quant: quant.sum(),
                                        'TotalPurchase': lambda price: price.sum()})
df_group.columns=['num_days','num_transactions','num_units','spent_money']
df_group['avg_order_value'] = df_group['spent_money']/df_group['num_transactions']
purchase_frequency = sum(df_group['num_transactions'])/df_group.shape[0]
repeat_rate = round(df_group[df_group.num_transactions > 1].shape[0]/df_group.shape[0],2)

churn_rate = round(1-repeat_rate,2)
df_group.reset_index()

df_group['profit_margin'] = df_group['spent_money']*0.05
df_group['CLV'] = (df_group['avg_order_value']*purchase_frequency)/churn_rate

# Resetting the index
df_group.reset_index(inplace = True)
df_plot = df.groupby(['Country','Description','UnitPrice','Quantity']).agg({'TotalPurchase': 'sum'},{'Quantity':'sum'}).reset_index()

##########
fig_UnitPriceVsQuantity = px.scatter(df_plot[:25000], x="UnitPrice", y="Quantity", color = 'Country', 
        size='TotalPurchase',  size_max=20, log_y= True, log_x= True, title= "PURCHASE TREND ACROSS COUNTRIES")


var_group = [i for i in df_group.columns if df_group.dtypes[i]=='float64']
for i in var_group:
        df_group[i] = df_group[i].round(2)
        df_group[i].apply(lambda x : "{:,}".format(x))
var_df = [i for i in df.columns if df.dtypes[i]=='float64']
for i in var_df:
        df[i] = df[i].round(2)
        df[i].apply(lambda x : "{:,}".format(x))

#####Layout
app1.layout=html.Div([

    html.Div([html.Div([dcc.Dropdown(id='select_pays',options=[{"label": i, "value": i} for i in list(df.Country.unique())
                        ],multi=False,style={'display': True},placeholder='Select Countries',className='dcc_compon')], className="create_container1 four columns",  style={'margin-bottom': '8px'})], className="row flex-display"),
    html.Div((html.Div(html.Div([html.P('Total  Clients', className='text-primary-p1', style={'textAlign': 'center'}),
    html.Span(id='id_total_clients', className='font-bold text-title',style={'textAlign': 'center'}) ], className="card_inner"),className="create_container two columns"),
    html.Div(html.Div([html.P('Total Transactions', className='text-primary-p1', style={'textAlign': 'center'}),
    html.Span(id='id_total_transactions', className='font-bold text-title',
    style={'textAlign': 'center'}),], className="card_inner"),className="create_container three columns"),
    html.Div(html.Div([html.P('Total Ventes($)', className='text-primary-p1', style={'textAlign': 'center'}),
    html.Span(id='id_total_ventes', className='font-bold text-title',
                              style={'textAlign': 'center'}),], className="card_inner"),className="create_container three columns"),
    
    html.Div(html.Div([html.P('Panier Moyen($)', className='text-primary-p1', style={'textAlign': 'center'}),
    html.Span(id='id_panier_moyen', className='font-bold text-title',
                              style={'textAlign': 'center'}),], className="card_inner"),className="create_container two columns"),
    html.Div(html.Div([html.P('Retention %', className='text-primary-p1', style={'textAlign': 'center'}),
    html.Span(id='id_retention', className='font-bold text-title',style={'textAlign': 'center'}),], className="card_inner"),className="create_container two columns")),className="row flex-display"),
    
    html.Br(),html.Br(),
    

    html.Div([
    html.Div([

                    html.Div([
                        html.Label(id='title_bar'),
                        dcc.Graph(id='fig-ProductPie',config={'displayModeBar':False,}),

                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '50%','padding-right': '15px'}),

                html.Div([
                    html.Div([
                        # html.Label(id='title_bar1'),
                        dcc.Graph(id='fig-UnitPriceVsQuantity',config={'displayModeBar':False,}),

                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '60%'}),

            ], className='row flex-display'),
    



     html.Div([
                html.Div([
                    html.Div([
                            dash_table.DataTable(id='id-results',
                                columns=[{'name': 'CustomerID', 'id': 'CustomerID',
                                        'type': 'numeric'},{'name': 'Pays', 'id': 'Country',
                                        },
                                    {'name': 'Transactions', 'id': 'num_transactions',
                                        'type': 'numeric'},
                                    {'name': 'Monnaie Depensee', 'id': 'spent_money',
                                        'type': 'numeric'},
                                    {'name': 'Panier Moyen', 'id': 'avg_order_value',
                                        'type': 'numeric'},
                                    {'name': 'Profit Marginal', 'id': 'profit_margin',
                                        'type': 'numeric'},
                                    {'name': 'Valeur Vie Client', 'id': 'CLV',
                                        'type': 'numeric'},
                                    
                                ],
                                  style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                },
                                                {
                                                    'if': {
                                                        'row_index': 0,  # number | 'odd' | 'even'
                                                        'column_id': 'Revenue'
                                                    },
                                                    'backgroundColor': 'dodgerblue',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'row_index': 0,  # number | 'odd' | 'even'
                                                        'column_id': 'Price'
                                                    },
                                                    'backgroundColor': 'dodgerblue',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'row_index': 0,  # number | 'odd' | 'even'
                                                        'column_id': 'Quantity'
                                                    },
                                                    'backgroundColor': 'dodgerblue',
                                                    'color': 'white'
                                                },
                                            ],
                                            style_header={
                                                'backgroundColor': 'rgb(230, 230, 230)',
                                                'fontWeight': 'bold',
                                                
                                            },
                                            style_data={
                                                'whiteSpace': 'normal',
                                                'height': 'auto',
                                            },
                                            editable=True,
                                            filter_action="native",
                                            sort_action="native",
                                            page_size=12,
                                ),

                             ]),

                ], style={'width': '100%'}),

            ], className='row'),

])
@app1.callback(
    [
        Output("id_total_clients", 'children'),
        Output("id_total_transactions", 'children'),
        Output("id_total_ventes", 'children'),
        Output("id_panier_moyen", 'children'), 
        # Output("id_churn", 'children'), 
        Output("id-results", 'data'), 
        Output("fig-UnitPriceVsQuantity", 'figure'),
        Output("fig-ProductPie", 'figure'), 
        Output("id_retention",'children')
    ],
    [
        Input("select_pays", "value")
    ]
)
def render_content(country_selected):
    if (country_selected != 'All' and country_selected != None):
        df_selectedCountry = df.loc[df['Country'] == country_selected]
        df_selectedCountry_p = df_group.loc[df_group['Country'] == country_selected]

        cnt_transactions = df_selectedCountry.Country.shape[0]
        cnt_customers = len(df_selectedCountry.CustomerID.unique())
        cnt_sales = round(df_selectedCountry.groupby('Country').agg({'TotalPurchase':'sum'})['TotalPurchase'].sum(),2)
        cnt_avgsales = round(df_selectedCountry_p.groupby('Country').agg({'avg_order_value': 'mean'})['avg_order_value'].mean())
        repeat_rate = round(df_selectedCountry_p[df_selectedCountry_p.num_transactions > 1].shape[0]/df_selectedCountry_p.shape[0],2)
        churn_rate = round(1-repeat_rate,2)
            

            # scatter plot for purchase trend
        df2 = df_plot.loc[df_plot['Country'] == country_selected]
        fig_UnitPriceVsQuantity_country = px.scatter(df2[:25000], x="UnitPrice", y="TotalPurchase", color = 'Quantity', 
                    size='Quantity',  size_max=20, log_y= True, log_x= True, title= "PURCHASE TREND ACROSS COUNTRIES")
            
            # Pie chart listing top products
        df_plot_bar = df_selectedCountry.groupby('Description').agg({'TotalPurchase':'sum'}).sort_values(by = 'TotalPurchase', ascending=False).reset_index().head(5)
        df_plot_bar['percent'] = round((df_plot_bar['TotalPurchase'] / df_plot_bar['TotalPurchase'].sum()) * 100,2)

        fir_plotbar = px.bar(df_plot_bar, y='percent', x='Description', title='Top selling products', 
                    text='percent', color='percent')
        fir_plotbar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
        fir_plotbar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',showlegend=False)                
            
        return [cnt_customers, cnt_transactions, cnt_sales, cnt_avgsales,  df_selectedCountry_p.drop(['num_days','num_units'], axis = 1).to_dict('records'),
                    fig_UnitPriceVsQuantity_country, fir_plotbar,repeat_rate*100]
    else:
            
            cnt_transactions = df.shape[0]
            cnt_customers = len(df.CustomerID.unique())
            cnt_sales = round(df.groupby('Country').agg({'TotalPurchase':'sum'})['TotalPurchase'].sum(),2)
            cnt_avgsales = round(df_group.groupby('Country').agg({'avg_order_value': 'mean'})['avg_order_value'].mean())


            repeat_rate = round(df_group[df_group.num_transactions > 1].shape[0]/df_group.shape[0],2)
            churn_rate = round(1-repeat_rate,2)

            # Bar chart listing top products
            df_plot_bar =df.groupby('Description').agg({'TotalPurchase':'sum'}).sort_values(by = 'TotalPurchase', ascending=False).reset_index().head(5)
            df_plot_bar['percent'] = round((df_plot_bar['TotalPurchase'] / df_plot_bar['TotalPurchase'].sum()) * 100,2).apply(lambda x : "{:,}".format(x))

            fir_plotbar = px.bar(df_plot_bar, y='percent', x='Description', title='TOP SELLING PRODUCTS', text='percent', color='percent',)
            fir_plotbar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
            fir_plotbar.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', showlegend=False)
            
            return [cnt_customers, cnt_transactions, cnt_sales,cnt_avgsales,  df_group.drop(['num_days','num_units'], axis = 1).to_dict('records'),
                    fig_UnitPriceVsQuantity, fir_plotbar,repeat_rate*100]
    



    



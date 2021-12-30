import pandas as pd
import matplotlib.pyplot as plt
import warnings
from operator import attrgetter
import matplotlib.colors as mcolors
from dash import  dcc
from dash import  html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from django_plotly_dash import DjangoDash
from dash import dash_table
import openpyxl
import numpy as np
import plotly.express as px
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff



def get_not_nan(L):
    t=[]
    for i in L:
        if str(i)!='nan':
            t.append(i)
        else:
            t.append(0)
    return t
def replace_nan_with(L):
    t=[]
    for i in L:
        if str(i)!='nan':
            t.append(i)
        else:
            t.append('')
    return t
def get_retention_values_empty(df,cols):
    all_list=[]
    for i,row in df.iterrows():
        temp= row[cols]
      
        temp=list(temp)
        
        temp=[100*a for a in temp]
        temp=[round(a,2) for a in temp]
        temp=replace_nan_with(temp)
        
        
        all_list.append(temp)
    return all_list
    

            
def get_retention_values(df,cols):
    all_list=[]
    for i,row in df.iterrows():
        temp= row[cols]
      
        temp=list(temp)
        temp=get_not_nan(temp)
        temp=[100*a for a in temp]
        temp=[round(a,2) for a in temp]
        
        
        all_list.append(temp)
    return all_list
def get_pivot_values(df,cols):
    all_list=[]
    for i,row in df.iterrows():
        temp= row[cols]
      
        temp=list(temp)
        temp=get_not_nan(temp)
        
        all_list.append(temp)
    return all_list


df = pd.read_excel('data/Retail_kaggle.xlsx',
                   dtype={'CustomerID': str,
                          'InvoiceID': str},
                   parse_dates=['InvoiceDate'], 
                   )
df_copy=df.copy()
df_copy = df_copy[['CustomerID', 'InvoiceNo', 'InvoiceDate']].drop_duplicates()
df_copy['order_month'] = df['InvoiceDate'].dt.to_period('M')
df_copy['cohort'] = df_copy.groupby('CustomerID')['InvoiceDate'].transform('min').dt.to_period('M') 
df_cohort = df_copy.groupby(['cohort', 'order_month']) \
              .agg(n_customers=('CustomerID', 'nunique')) \
              .reset_index(drop=False)

df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(attrgetter('n'))
cohort_pivot = df_cohort.pivot_table(index = 'cohort',
                                     columns = 'period_number',
                                     values = 'n_customers')
cohort_size = cohort_pivot.iloc[:,0]
retention_matrix = cohort_pivot.divide(cohort_size, axis = 0)
cols = x_axis = retention_matrix.columns.values.tolist()
rows1=rows = y_axis = [p.strftime('%b-%Y') for p in list(retention_matrix.index)]
z_axis=get_retention_values(retention_matrix,cols)
annot=get_retention_values_empty(retention_matrix,cols)
totals=get_pivot_values(cohort_pivot,cols)
pourcentages=z_axis
hover=[]
for row in range(len(rows1)):
    
    hovertemplate = (
            '<b>Cohort: {cohort_time}<b> <br>'+
            'Months after first purschase: {month_number}<br>'+
            'Cohort Total Interactions: {cohort_size}<br>' +
            'Retention Percentage: {retention_percentage}%<br>' 
        )

    cohort_hovertext = []
    for a,b in zip(pourcentages,totals):
        
        percentage_total_by_cohort = zip(a, b)
        for i, (percentage, total) in enumerate(percentage_total_by_cohort):
            if percentage and total: 
                total_val=float(total)
                percentage_val=float(percentage)
                hovertext = hovertemplate.format(
                    cohort_time=rows1[row],
                    cohort_size=int(total_val),
                    month_number=int(cols[i]),
                    retention_percentage=percentage_val
                   
                )
            else:
                hovertext=''
            cohort_hovertext.append(hovertext)
    hover.append(cohort_hovertext)
hovertext = hover
y_axis=y_axis[::-1]
fig = ff.create_annotated_heatmap(
        x=x_axis, y=y_axis, z=z_axis,
    text=hovertext,
    hoverinfo='text',
    annotation_text=annot[::-1],
    

        
        colorscale='Plasma'
    )

fig.update_layout(
        xaxis_title= " Months after firt purchase",
        yaxis_title="Cohorts ",
        margin=dict(l=40, r=40),
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app2=DjangoDash('Cohorts', external_stylesheets=external_stylesheets)
app2.layout = html.Div([html.H3('Analyse des Cohortes',style={'textAlign': 'center'}),
    html.Div([
        
                html.Div([

                    html.Div([
                        html.Label(id='title_bar'),
                        dcc.Graph(figure=fig,config={'displayModeBar':False,}),

                    ], className='box', style={'padding-bottom': '15px'}),

                ], style={'width': '100%'})

               

            ], className='row'),
])



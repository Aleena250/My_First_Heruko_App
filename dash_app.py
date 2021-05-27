# -*- coding: utf-8 -*-
"""
Created on Tue May 18 14:53:28 2021

@author: EIG
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df =pd.read_csv('SNGPL Meter Reading New.csv')
print(df.head(20))
# set dat as Index
df.set_index('Date_and_Time', inplace = True)
print(df.head(20))

#Create new datframe with selected column
selected_columns = df["M3_difference"]
df_copy = selected_columns.copy()
print(df_copy.head(20))
df_copy = df_copy.reset_index(drop=False)
print(df_copy.head())

df_copy['Date_and_Time'] = pd.to_datetime(df_copy['Date_and_Time']).dt.date

df_copy['Date_and_Time'] = df_copy['Date_and_Time'].astype('datetime64[ns]')

print(df_copy.head())
#calculate daily gas consumption in m3
df_copy.rename(columns={"Date_and_Time": "days"},inplace=True)
print(df_copy.head())
df_copy_day=df_copy.groupby('days',sort=False).agg(
    # Get sum of the interpolate meter reading in m3 column for each group
    sum_consumption_perDay=('M3_difference', sum))
df_copy_day = df_copy_day.reset_index(drop=False)
print(df_copy_day)
#----------------------------End Daily Gas Usage------------------------------

# calculate monthly gas usage in m3
#-----------------------------------------------------------------------------
df_copy_day = df_copy_day.reset_index(drop=False)
df_copy_month=df_copy_day.copy()
df_copy_month['days'] = pd.to_datetime(df_copy_month['days']).dt.month
df_copy_month.rename(columns={"days": "months"},inplace=True)
print(df_copy_month)
df_copy_month=df_copy_month.groupby(df_copy_month['months']).agg(
    # Get sum of the interpolate meter reading in m3 column for each group
    sum_consumption_perMonth=('sum_consumption_perDay', sum))
#df_copy_month.set_index('months', inplace = True)
df_copy_month = df_copy_month.reset_index(drop=False)
print(df_copy_month)

#-----------------------------End Monthly Gas Usage---------------------------


trace1 = go.Bar(x=df_copy_day['days'], y=df_copy_day['sum_consumption_perDay'],
                name='Daily Total Consumption of gas in m3')
trace2=go.Bar(x=df_copy_month['months'], y=df_copy_month['sum_consumption_perMonth'],
                name='Monthly Total Consumption of gas in m3')



#----------------------------------App Code Starts Here------------------------
external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Gas Consumption Analytics: Understand Your Consumption of Gas!"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Gas Consumption Analysis", className="header-title"
                ),
                html.P(
                    children="Analyze the Consumption of gas"
                    " on the basis of hourly, daily and monthly",
                    className="header-description",
                ),
            ],
            className="header",
        ),
   
    dcc.Graph(
        id='Daily Consumption',
        figure={
            'data': [trace1],
            'layout':
            go.Layout(title='Daily Consumption of gas in m3', barmode='stack')
        }),
    dcc.Graph(
        id='Monthly Consumption',
        figure={
            'data': [trace2],
            'layout':
            go.Layout(title='Monthly Consumption of gas in m3', barmode='stack')
        }),
        
   
        
])
    
if __name__ == '__main__':
  app.run_server(debug=True)
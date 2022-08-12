import dash
from dash import dcc
from dash import html
from dash import dash_table
import plotly.express as px

app = dash.Dash('app')

#from gas import gas 
import pandas as pd
pd.options.plotting.backend = "plotly"

gas() #calls the scraping fn

df = pd.read_csv("ssmgas.csv", sep=",")
df.drop(df.tail(1).index,inplace=True) # drop last row
df['Gas Station '] = df['Station '] + df['Address ']
df = df.astype({'Price ': float}) #convert Price column to float
print(df)

mingas = df[df['Price ']==df['Price '].min()] #station(s) with cheapest gas is stored here
mingas.reset_index(inplace = True, drop = True)
#n = len(mingas) #no of rows/no of stations
#print('Lowest gas price in SSM')
#for i in range(0,n):  
# print(mingas['Price '][i], mingas['Station '][i], mingas['Address '][i], mingas['City'][i]) 
#print()

maxgas = df[df['Price ']==df['Price '].max()] #station(s) with costliest gas is stored here
maxgas.reset_index(inplace = True, drop = True)
#n = len(maxgas) #no of rows/no of stations
#print('Highest gas price in SSM')
#for i in range(0,n):  
#  print(maxgas['Price '][i], maxgas['Station '][i], maxgas['Address '][i], maxgas['City'][i]) 
#print()

#setting up the bar chart
fig = px.bar(df, x="Gas Station ", y="Price ",labels={'Gas Station ':'Gas Station','Price ':'Price (cents/L)'})


#fig['layout'].update(height=600, width=1300, title='Gas Prices in SSM')
fig['layout'].update(title='Gas Prices in SSM')

#to customise bar color and opacity
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.6)

#list of columns to display in datatable
select_columns = ['Price ','Station ',"Address ",'City']

#webapp layout
app.layout = html.Div(children=[
    html.H1(children='Live Gas Prices',style={'color': 'black', "font-family":'sans-serif','textAlign': 'center'}),
    html.P(children='''
        This is a web app developed using Dash and Selenium to show live gas prices for Sault Ste. Marie
    ''',style={'color': 'black', "font-family":'sans-serif','textAlign': 'center'}),
  
     dcc.Graph(
        id='gas-graph',
        figure=fig
    ),

    html.Br(),

    html.P(f"Lowest gas price in SSM: {mingas['Price '][0]} cents/L",style={'color': 'black', "font-family":'sans-serif','font-size': '25px','textAlign': 'center'}),
#"font-"
  
    html.Br(),
    html.Br(),
  
    dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'name': c, 'id': c} for c in select_columns],
    page_size=10,
    style_cell={'fontSize':15, 
                'font-family':'sans-serif',
                'textAlign': 'center' #to center align the text in the cell
               },
    style_table={'padding-left': '0%',
                 'padding-right': '0%',
                 #'marginLeft': '5%', 
                 'margin': 'auto', #to keep table center aligned
                 'width': '70%'
                },
    style_header={
        #'backgroundColor': 'white',
        'backgroundColor':'rgb(158,202,225)',
        'fontWeight': 'bold'
    },  
    #fill_width=False  
),
   
  
   
  
])

#if __name__ == '__main__':
#    app.run_server(debug=True)
app.run_server(host='0.0.0.0',port=8081, debug=True)


import dash
from dash import dcc,html, callback
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import date
from datetime import datetime
import pandas as pd
import dash_bootstrap_components as dbc
data = pd.read_csv(r'C:\Users\USER\Downloads\dash\2023_data.csv')

G=['Incomer G3','Incomer G4','Incomer 1 G2','Incomer 5 G1','Incomer 2 G5']
PV=['PV Gen','PV EDL']
EDL=['EDLTF-1','EDLTF-2','EDLTF-3']
generator_names = G + PV + EDL
all_column_names = data.columns
receiver_options=[name for name in all_column_names if name not in generator_names and name !='Date/time' ]
receivers_data = data.drop(columns=generator_names)

def filter_data(start_date,end_date):
    if start_date is not None and end_date is not None:
        filtered_data = receivers_data[
      (pd.to_datetime(receivers_data['Date/time']) >= start_date) &  
      (pd.to_datetime(receivers_data['Date/time']) <= end_date)
    ]
    else:

        filtered_data=receivers_data[pd.to_datetime(receivers_data['Date/time']).dt.month==1]
    consumption = filtered_data.iloc[:, 1:].diff(axis=0)
    
    return consumption

dash.register_page(__name__, path='/Consumption')
layout = html.Div([
    
   html.Div([
  html.Span("Consumption", style={'font-weight': 'bold', 'font-size': '2rem',  'color': '#5383AD'}),
], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),

    
    html.Div([
        html.Div([
  
  html.Div([
    
    html.Div([
      html.Div([
        
        html.Span("Select receiver: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': '40px'}),
        dcc.Dropdown(
          id='y_axis_dropdown',
          options=[{'label': option, 'value': option} for option in receiver_options],
          value=receiver_options[0],
          multi=False
        ),
      ], style={'width': '70%','margin-top': '40px','margin-left':'10px'}), 
      html.Div([
        
        html.Span("Select date range: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': '40px'}),
        dcc.DatePickerRange(
          id='date-picker-range1',
          min_date_allowed=data['Date/time'].min(),
          max_date_allowed=data['Date/time'].max(),
          initial_visible_month=data['Date/time'].min(),
          start_date=date(2023, 1, 1),
          end_date=date(2023, 1, 2)
        ),
      ], style={'width': '70%', 'margin-top': '30px','margin-left':'10px'}),  
    ],style={'background-color': '#fff'}),

    # Row 2: Graph
    html.Div([
      dcc.Graph(id='the_graph'),
    ], style={'width': '70%'}),  
  ], style={'display': 'flex'}), 
])
,

html.Div(style={'width': '100%','height':'30px'}),

        
        html.Div([
            html.Div([
                html.Span("Select date range: ", style={'font-weight': 'bold', 'color': '#333', 'margin-bottom': 40}),
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=data["Date/time"].min(),
                    max_date_allowed=data["Date/time"].max(),
                    initial_visible_month=data["Date/time"].min(),
                    start_date=date(2023, 1, 1),
                    end_date=date(2023, 1, 31)
                ),
            ],style={'width': '70%', 'margin-top': '30px','margin-left':'10px'}),
            html.Div([
                dcc.Graph(id="consumption-pie-chart"),
                dcc.Graph(id="consumption-bar-chart"),
            ], style={'display': 'flex', 'width': '100%'}), 
        ],style={'background-color': '#fff'}),
    ], style={ 
        'background-color': '#36587c',  
        'font-family': 'sans-serif', 
        'padding': '20px',  
        'border': '1px solid #ddd',  
        'display': 'flex',  
        'flex-direction': 'column' , 
        'color':'#5383AD'
    }),
])  



@callback(
    Output(component_id='the_graph', component_property='figure'),

    [Input(component_id='y_axis_dropdown', component_property='value'),
     Input('date-picker-range1', 'start_date'),
     Input('date-picker-range1', 'end_date')]
)
def update_graph(y_axis_dropdown,start_date, end_date):
    if start_date is not None and end_date is not None:
        filtered_data = data[
      (pd.to_datetime(data['Date/time']) >= start_date) &  
      (pd.to_datetime(data['Date/time']) <= end_date)
    ]
    else:

        filtered_data=data[pd.to_datetime(data['Date/time']).dt.month==1]
    consumption = filtered_data.iloc[:, 1:].diff(axis=0)
    consumption['Date/time']=filtered_data['Date/time']
    figure = px.line(
        consumption,
        x='Date/time',
        y=y_axis_dropdown  
    )
    
    return figure


@callback(
    Output("consumption-pie-chart", "figure"),
    Output("consumption-bar-chart", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_pie_chart(start_date, end_date):
    consumption=filter_data(start_date, end_date)
    consumption=consumption.sum(axis=0)
    names = consumption.index.to_numpy()
    values = consumption.to_numpy()

    fig = px.pie(
        values=values, 
        names=names,   
        hole=0.3,      
        #title="Consumption by Receiver "  
    )
    fig2= px.bar(
        
    consumption,  
    x=names, 
    y=values,  
    #title='Consumption by Receiver ',  
    barmode='group'  
    )
    return fig, fig2





import dash
from dash import dcc,html, callback
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import date
import pandas as pd

data = pd.read_csv(r'C:\Users\USER\Downloads\dash\2023_data.csv')

G=['Incomer G3','Incomer G4','Incomer 1 G2','Incomer 5 G1','Incomer 2 G5']
PV=['PV Gen','PV EDL']
EDL=['EDLTF-1','EDLTF-2','EDLTF-3']
generator_names = G + PV + EDL
all_column_names = data.columns
Generator_options=[name for name in all_column_names if name not in generator_names and name !='Date/time' ]
generators_data = data.drop(columns=Generator_options)

def filter_data(start_date,end_date):
    if start_date is not None and end_date is not None:
        filtered_data = generators_data[
      (pd.to_datetime(generators_data['Date/time']) >= start_date) &  
      (pd.to_datetime(generators_data['Date/time']) <= end_date)
    ]
    else:

        filtered_data=generators_data[pd.to_datetime(generators_data['Date/time']).dt.month==1]
    generation = filtered_data.iloc[:, 1:].diff(axis=0)
    
    return generation


dash.register_page(__name__, path='/Generation')

layout = html.Div([
    
    html.Div([
  html.Span("Generation", style={'font-weight': 'bold', 'font-size': '2rem', 'color': '#5383AD'}),
], style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
,
    
    html.Div([
        html.Div([
  
  html.Div([
    
    html.Div([
      html.Div([
        
        html.Span("Select generator: ", style={'font-weight': 'bold', 'color': '#fff', 'margin-bottom': '40px'}),
        dcc.Dropdown(
          id='y_axis_dropdown',
          options=[{'label': option, 'value': option} for option in generator_names],
          value=generator_names[0],
          multi=False
        ),
      ], style={'width': '70%','margin-top': '40px','margin-left':'10px'}), 
      html.Div([
        
        html.Span("Select date range: ", style={'font-weight': 'bold', 'color': '#fff', 'margin-bottom': '40px'}),
        dcc.DatePickerRange(
          id='date-picker-range1',
          min_date_allowed=data['Date/time'].min(),
          max_date_allowed=data['Date/time'].max(),
          initial_visible_month=data['Date/time'].min(),
          start_date=date(2023, 1, 1),
          end_date=date(2023, 1, 7)
        ),
      ], style={'width': '70%', 'margin-top': '30px','margin-left':'10px'}),  
    ],style={'background-color': '#36587c'}),

    
    html.Div([
      dcc.Graph(id='the_graph1'),
    ], style={'width': '70%','boxShadow': '0px 0px 5px rgba(0, 0, 0, 0.2)'}),  
  ], style={'display': 'flex'}), 
])
,

html.Div(style={'width': '100%','height':'30px'}),

        
        html.Div([
            html.Div([
                html.Span("Select date range: ", style={'font-weight': 'bold', 'color': '#fff', 'margin-bottom': 40}),
                dcc.DatePickerRange(
                    id="date-picker",
                    min_date_allowed=data["Date/time"].min(),
                    max_date_allowed=data["Date/time"].max(),
                    initial_visible_month=data["Date/time"].min(),
                    start_date=date(2023, 1, 1),
                    end_date=date(2023, 1, 31)
                ),
            ],style={'width': '70%', 'margin-top': '30px','margin-left':'10px'}),
            html.Div(style={'width': '100%','height':'10px'}),
            html.Div([
                dcc.Graph(id="generation-pie-chart",style={'boxShadow': '0px 0px 5px rgba(0, 0, 0, 0.2)'}),
                dcc.Graph(id="generation-bar-chart",style={'boxShadow': '0px 0px 5px rgba(0, 0, 0, 0.2)'}),
            ]), 
        ],style={'background-color': '#36587c'}),
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
    Output(component_id='the_graph1', component_property='figure'),

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
    generation = filtered_data.iloc[:, 1:].diff(axis=0)
    generation['Date/time']=filtered_data['Date/time']
    figure = px.line(
        generation,
        x='Date/time',
        y=y_axis_dropdown  
    )
    
    return figure


@callback(
    Output("generation-pie-chart", "figure"),
    Output("generation-bar-chart", "figure"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_pie_chart(start_date, end_date):
    generation=filter_data(start_date, end_date)
    generation=generation.sum(axis=0)
    names = generation.index.to_numpy()
    values = generation.to_numpy()

    fig = px.pie(
        values=values, 
        names=names,   
        hole=0.3,      
        #title="generation by Generator "  
    )
    fig2= px.bar(
        
    generation,  
    x=names, 
    y=values,  
    #title='generation by Generator ',  
    barmode='group'
    )
    fig2.update_xaxes(title_text="Generator")
    fig2.update_yaxes(title_text="kW/hr")
    return fig, fig2






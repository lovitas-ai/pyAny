import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as gp
import numpy as np
#from datetime import datetime
import pandas as pd


#Data

df_01=pd.read_csv('pyramid.csv')

app= dash.Dash((__name__),external_stylesheets=[dbc.themes.FLATLY],
            meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0'}]

)

#Layout

app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Bevölkerung in Bayern Dashboard",
            className='text-center text-primary mb-4'), width=12)


        ]),
        dbc.Row([
            dbc.Col([
            
                dcc.Dropdown(id='bev_check', options=[{'label': x,'value': x} for x in sorted(df_01['J'].unique())], value=2020,className='dropdown'),
                dcc.Dropdown(id='bev_check2', options=[{'label': x,'value': x} for x in sorted(df_01['Kreis'].unique())], value='Ansbach (Lkr)',className='dropdown'),  
                    dcc.Graph(id='bev_graph',figure={}),
                ], width={'size':5,'offset':0,'order':1}),                
        
        ])
    ], fluid=True)


@app.callback(
    Output(component_id='bev_graph', component_property='figure'),
    [Input(component_id='bev_check', component_property='value')],
    [Input(component_id='bev_check2', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph(val_chosen,val_chosen2):
    if val_chosen is not None:
        # print(n)
        print(f"value user chose: {val_chosen}")
        print(type(val_chosen))
        print(f"value user chose: {val_chosen2}")
        print(type(val_chosen2))
        dff_01 = df_01[(df_01["J"]==(val_chosen)) & (df_01["Kreis"] == (val_chosen2))]
        fig = gp.Figure()
        name1='Männer'
        name2='Frauen'
        customdata=np.stack((dff_01['Altersjahre'],dff_01['männlich'],dff_01['weiblich']),axis=-1)
        hovertemp='<br>Gruppe: %{meta[0]}<br>Alter: %{customdata[0]}<br> in dieser Altersklasse <br>Anzahl Männer:%{customdata[1]}<br>Anzahl Frauen :%{customdata[2]}'
        # Adding Male data to the figure
        fig.add_trace(gp.Bar(y= dff_01['A'], x = dff_01['männlich'], 
                        name = name1, 
                            orientation = 'h',
                            meta=[name1,dff_01['männlich']],
                            ))
        # Adding Female data to the figure
        fig.add_trace(gp.Bar(y = dff_01['A'], x = dff_01['weiblich']*-1,
                            name = name2, orientation = 'h',
                            meta=[name2,dff_01['weiblich']],
                            ))
        # Updating the layout for our graph
        fig.update_layout(title = 'Bevölkerungspyramide',
                        title_font_size = 22, barmode = 'relative',
                        bargap = 0.0, bargroupgap = 0,
                        yaxis=gp.layout.YAxis(title='Alter'),
                        xaxis=gp.layout.XAxis(
                            title='Anzahl'),
                        )
        fig.update_traces(customdata=customdata, hovertemplate=hovertemp)
        return fig
    elif val_chosen is None:
        raise dash.exceptions.PreventUpdate    


if __name__=='__main__':
    app.run_server(debug=True, port=7000)

from cgitb import text
import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as gp
import numpy as np
import pandas as pd
import plotly.express as px
import geopandas

#Data
kreis_map=geopandas.read_file('landkreise_s.geojson') 
df_01=pd.read_csv('pyramid.csv')
df_02=pd.read_csv('infobox.csv')
df_02['AGS'] = df_02['AGS'].astype(str)
df_02['AGS'] = df_02['AGS'].str.zfill(5)
app= dash.Dash((__name__),external_stylesheets=[dbc.themes.FLATLY],
            meta_tags=[{'name': 'viewport',
                           'content': 'width=device-width, initial-scale=1.0'}]

)

#Layout

app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Bevölkerung in Bayern Dashboard",
            className='text-center text-primary mb-4 '), width={'size':9,'offset':1,'order':1})
            ], justify = 'start'),
        dbc.Row([
            dbc.Col(
                [html.P("Wählen Sie den Kreis",className='text-left text-secundary mb-4'), 
            dcc.Dropdown(id='kreis', options=[{'label': x,'value': x} for x in sorted(df_01['Kreis'].unique())], value='Ansbach (Lkr)',className='dropdown'),
            html.P("Wählen Sie das Jahr",className='text-left text-secundary mb-4 pt-3 '), 
            dcc.Slider(id='year', min = 2000, max=2020,step =1, value=2020,className='slider',updatemode='drag', marks={
                    2000: '2000',2001:'2001',2002:'2002',2003:'2003',2004:'2004',2005:'2005',2006:'2006',2007:'2007',2008:'2008',2009:'2009',2010:'2010',
                    2011:'2011',2012:'2012',2013:'2013',2014:'2014',2015:'2015',2016:'2016',2017:'2017',2018:'2018',2019:'2019',2020:'2020',})]
                    ,width={'size':9,'offset':1,'order':1}),
        ], justify = 'start'),
        dbc.Row([
            dbc.Col([
                    dcc.Graph(id='bev_graph',figure={},className='divBorder'),
                ], width={'size':4,'offset':1,'order':1}),                
            dbc.Col([  
                dbc.CardHeader("Zusätzliche Informationen:"),
                dbc.CardBody([html.P("Card title", className="card-title",id='cardname'),
                            html.P('Example P', className='card-text', id='cardyear'),
                            html.P('Example P', className='card-text', id='cardeinw'),
                            html.P('Example P', className='card-text', id='cardmänner'),
                            html.P('Example P', className='card-text', id='cardfrauen'),
                            html.P('Example P', className='card-text', id='cardgeschl_v'),
                            html.P('Example P', className='card-text', id='carddalter'),
                                ],className="card border-secondary divBorder")
                ], width={'size':4,'offset':1,'order':1}),
        ], justify = 'start'),
        dbc.Row([
            dbc.Col([
                html.P(" ",className='text-left text-primary mb-4'),
                dcc.Graph(id='einw_graph',figure={},className='divBorder')
            ], width={'size':9,'offset':1,'order':1})
            ], justify = 'start'),
        dbc.Row([
            dbc.Col([ 
                    html.P(" ",className='text-left text-primary mb-4'),
                    html.H2("Kartenanalysen",className='text-left text-primary mb-4'),
                    dcc.Slider(id='year_map', min = 2000, max=2020,step =1, value=2020,className='slider',updatemode='drag', marks={
                    2000: '2000',2001:'2001',2002:'2002',2003:'2003',2004:'2004',2005:'2005',2006:'2006',2007:'2007',2008:'2008',2009:'2009',2010:'2010',
                    2011:'2011',2012:'2012',2013:'2013',2014:'2014',2015:'2015',2016:'2016',2017:'2017',2018:'2018',2019:'2019',2020:'2020',}),
                    dcc.RadioItems(id='radio_map',options=[
                    {'label': 'Durchschnittsalter', 'value': 'D_Alter'},
                    {'label': 'Geschlechterverhältnis', 'value': 'Geschl_v'}],value='D_Alter',inline=True, className='mb-4'),
                    dcc.Graph(id='graph_map',figure={},className='divBorder'),
            ], width={'size':9,'offset':1,'order':1})
        ],justify = 'start')
         ], fluid=True, className='body' )


@app.callback(
    Output(component_id='bev_graph', component_property='figure'),
    [Input(component_id='year', component_property='value')],
    [Input(component_id='kreis', component_property='value')],
    prevent_initial_call=False
)


def update_my_graph(val_chosen,val_chosen2):
    if val_chosen is not None:
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


@app.callback(
    Output(component_id='cardname', component_property='children'),
    Output(component_id='cardyear', component_property='children'),
    Output(component_id='cardeinw', component_property='children'),
    Output(component_id='cardmänner', component_property='children'),
    Output(component_id='cardfrauen', component_property='children'),
    Output(component_id='cardgeschl_v', component_property='children'),
    Output(component_id='carddalter', component_property='children'),
    [Input(component_id='kreis', component_property='value')],
    [Input(component_id='year', component_property='value')],
    prevent_initial_call=False
)

def update_my_text(kreis_val,year_val):
    #,J,Kreis,männlich,weiblich,DAlter_m,DAlter_w,Ein,Geschl_v,D_Alter
    einw=(df_02[(df_02['J']==(year_val)) & (df_02['Kreis'] == (kreis_val))].reset_index()).at[0,'Ein']
    männer=(df_02[(df_02['J']==(year_val)) & (df_02['Kreis'] == (kreis_val))].reset_index()).at[0,'männlich']
    frauen=(df_02[(df_02['J']==(year_val)) & (df_02['Kreis'] == (kreis_val))].reset_index()).at[0,'weiblich']
    geschl_v=round((df_02[(df_02['J']==(year_val)) & (df_02['Kreis'] == (kreis_val))].reset_index()).at[0,'Geschl_v'],2)
    dalter=round((df_02[(df_02['J']==(year_val)) & (df_02['Kreis'] == (kreis_val))].reset_index()).at[0,'D_Alter'],2)
    print('Anzahl des gewählten Kreis '+ str(einw))
    return (f' Kreis: {kreis_val}', f' Jahr : {year_val}' ,f' Anzahl der Einwohner : {einw}',f' Anzahl Männer : {männer}',
            f' Anzahl Frauen : {frauen}',f' Geschlechterverhältnis: Auf 100 Frauen kommen {geschl_v} Männer',f' Durchschnittsalter : {dalter} Jahre' )




@app.callback(
    Output(component_id='einw_graph', component_property='figure'),
    [Input(component_id='kreis', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph2(kreis_val):
    dff_02 = df_02[df_01["Kreis"] == (kreis_val)].reset_index()
    fig = gp.Figure()
    fig.add_trace(gp.Scatter(y= dff_02['Ein'], x = dff_02['J'], mode='lines'))
    fig.update_layout(title=f'Einwohnerentwicklung in {kreis_val}',
                   xaxis_title='Jahr',
                   yaxis_title='Einwohner',
        xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        )),
        yaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
        
    ) )              
    return fig


@app.callback(
    Output(component_id='graph_map', component_property='figure'),
    [Input(component_id='year_map', component_property='value')],
    [Input(component_id='radio_map', component_property='value')],
    prevent_initial_call=False
    )
def update_my_graph2(year_map,radio_map):
    dff_02_01 = df_02[(df_02["J"]==(year_map))]
    fig = px.choropleth(dff_02_01,featureidkey='properties.AGS', geojson=kreis_map, locations='AGS', color=radio_map,
                    projection="mercator",color_continuous_scale="Viridis", hover_name='Kreis')
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title_text = 'Bayern',margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__=='__main__':
    app.run_server(debug=True, port=7000)

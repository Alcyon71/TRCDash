import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from textwrap import dedent as d
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import os

#Import des données
# df = pd.read_excel('test.xls', sheet_name='Données brutes', index_col=None, header=None)
# df.columns = ['Temps', 'Température', 'Dilatation']

#print(df)

app = dash.Dash()

app.config['suppress_callback_exceptions']=True

#CSS offline
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

#Affichage de la page web
app.layout = html.Div(children=[
    html.H4(children='Essai TRC'),
    dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=False
        ),
    dcc.Graph(id='trc-graph'),
    html.Hr(),
    dcc.Graph(id='trc-graph-zoom'),
    html.Hr(),
    dcc.Dropdown(
        id='Drop-Tangente',
        options=[
            {'label': 'Tangente1 x1', 'value': 'T1X1'},
            {'label': 'Tangente1 y2', 'value': 'T1Y1'},
            {'label': 'Tangente1 x2', 'value': 'T1X2'},
            {'label': 'Tangente1 y2', 'value': 'T1Y2'}
        ],
        value='T1X1'
    ),
    html.Div(className='tangente', children=[
            html.Div([
                html.H4('Tangente1'),
                html.Div([
                    dcc.Input(
                        id='T1X1',
                        placeholder='x1',
                        type='text',
                        value='',
                        size='10'
                    ),
                    dcc.Input(
                        id='T1Y1',
                        placeholder='y1',
                        type='text',
                        value='',
                        size='10'
                    )]),
                html.Div([
                    dcc.Input(
                        id='T1X2',
                        placeholder='x2',
                        type='text',
                        value='',
                        size='10'
                    ),
                    dcc.Input(
                        id='T1Y2',
                        placeholder='y2',
                        type='text',
                        value='',
                        size='10'
                    )]),
                ]),
            html.Div([
                html.H4('Tangente2'),
                html.Div([
                    dcc.Input(
                        id='T2X1',
                        placeholder='x1',
                        type='text',
                        value='',
                        size='10'
                    )]),
                html.Div([
                    dcc.Input(
                        id='T2X2',
                        placeholder='x2',
                        type='text',
                        value='',
                        size='10'
                    )]),
            ]),
    ], style={'columnCount': 2}),
    html.Div(id='TestClick')
])



#Traitement des données du fichier et création du graph général
def parse_contents(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(',')
        print(filename)
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df = pd.read_excel(io.BytesIO(decoded), sheet_name='Données brutes', index_col=None, header=None)
                df.columns = ['Temps', 'Température', 'Dilatation']
        except Exception as e:
            print(e)
            return html.Div([
                'There was an error processing this file.'
            ])

        return df

#Callback de l'upload
@app.callback(Output('trc-graph', 'figure'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename')])
def update_output(contents, filename):
    if contents is not None:
        df2 = parse_contents(contents, filename)
        if df2 is not None:
            return {'data': [{'x': df2.Température, "y": df2.Dilatation,'mode': 'markers', 'text': df2.Temps, 'type': 'Scatter', 'name': 'Test'}],
                   'layout': {'title': 'Test Titre'
                              }}
        else:
            return [{}]
    else:
        return [{}]

@app.callback(
    Output('trc-graph-zoom', 'figure'),
    [Input('trc-graph', 'selectedData')])
def graph_selected_data(selectedData):
    if selectedData is not None:
        dfselectdata = pd.DataFrame.from_dict(selectedData['points'], orient='columns')
        return {'data': [
            {'x': dfselectdata.x, "y": dfselectdata.y, 'mode': 'markers', 'type': 'Scatter',
             'name': 'Selection'}],
                'layout': {'title': 'Selection'
                           }}
    else:
        return [{}]

#Todo : Sélection des points pour tracer tangente, voir layout 'shapes' documentation plotly
@app.callback(
    Output('TestClick', 'children'),
    [Input('trc-graph-zoom', 'clickData')],
    [State('Drop-Tangente', 'value')])
def display_click_data(clickData,value):
    #return json.dumps(clickData, indent=2)
    return html.Div([
        html.Pre(json.dumps(clickData, indent=2), style=styles['pre']),
        html.Div([value])
            ])

if __name__ == '__main__':
    app.run_server(debug=True)
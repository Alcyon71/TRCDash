import base64
import datetime
import io
import logging, sys

import dash
from dash.dependencies import Input, Output, State
from textwrap import dedent as d
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
from scipy import signal
import numpy as np
import plotly
import os

#Debug
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

#Import des données
# df = pd.read_excel('test.xls', sheet_name='Données brutes', index_col=None, header=None)
# df.columns = ['Temps', 'Température', 'Dilatation']

#print(df)

app = dash.Dash()

#app.config['suppress_callback_exceptions']=True

#CSS offline
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

#Affichage de la page web
app.layout = html.Div([
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
            {'label': 'Tangente1 x1/y1', 'value': 'T1-X1-Y1'},
            {'label': 'Tangente1 x2/y2', 'value': 'T1-X2-Y2'},
            {'label': 'Tangente2 x1/y1', 'value': 'T2-X1-Y1'},
            {'label': 'Tangente2 x2/y2', 'value': 'T2-X2-Y2'}
        ],
        value='T1-X1-Y1'
    ),
    html.Div(id='InputTangente', children=[
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
                    ),
                    dcc.Input(
                        id='T2Y1',
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
                    ),
                    dcc.Input(
                        id='T2Y2',
                        placeholder='x2',
                        type='text',
                        value='',
                        size='10'
                    )]),
                ]),
    ], style={'columnCount': 2}),
    html.Div(id='CalculTangente', children=[
        html.Button('Calculer Tangente', id='btnTangente'),
        html.Button('Essai', id='btnEssai', n_clicks=0),
        html.Button('EssaiCalculdérive', id='btnEssai2', n_clicks=0)
    ]),
    html.Div([
        dt.DataTable(
            rows=[{}], # initialise the rows
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable'
        )
    ])
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
    logging.debug(filename)
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
    [Input('trc-graph', 'selectedData'),
     Input('btnEssai', 'n_clicks')])
def graph_selected_data(selectedData, n_clicks):
    if selectedData is not None and n_clicks == 0:
        dfselectdata = pd.DataFrame.from_dict(selectedData['points'], orient='columns')
        #logging.debug(selectedData['points'])
        return {'data': [
            {'x': dfselectdata.x, "y": dfselectdata.y, 'mode': 'markers', 'type': 'Scatter',
             'name': 'Selection'}],
                'layout': {'title': 'Selection'
                           }}
    elif selectedData is not None and n_clicks > 0:
        dfselectdata = pd.DataFrame.from_dict(selectedData['points'], orient='columns')
        dfselectdata['scipy'] = signal.savgol_filter(dfselectdata['y'], 5, 3)
        return {'data': [
            {'x': dfselectdata.x, 'y': dfselectdata.y, 'mode': 'markers', 'type': 'Scatter', 'name': 'Selection'},
            {'x': dfselectdata.x, 'y': dfselectdata.scipy, 'mode': 'markers', 'type': 'Scatter', 'name': 'test'}],
                'layout': {'title': 'Selection'
                           }}
    else:
        return [{}]



output_elements = ['T1X1', 'T1Y1', 'T1X2', 'T1Y2', 'T2X1', 'T2Y1', 'T2X2', 'T2Y2']

def create_callback(output):
    def callback(clickData, DropValue, ValT1X1, ValT1Y1, ValT1X2, ValT1Y2, ValT2X1, ValT2Y1, ValT2X2, ValT2Y2):
        if clickData is not None:
            logging.debug(DropValue)
            logging.debug(output)
            logging.debug(DropValue.split('-')[0] + DropValue.split('-')[1])
            if (DropValue.split('-')[0] + DropValue.split('-')[1]) == output:
                logging.debug(clickData['points'][0][output[2].lower()])
                return clickData['points'][0][output[2].lower()]
            elif (DropValue.split('-')[0] + DropValue.split('-')[2]) == output:
                return clickData['points'][0][output[2].lower()]

    return callback

for output_element in output_elements:
    dynamically_generated_function = create_callback(output_element)
    app.callback(Output(output_element, 'value'),
             [Input('trc-graph-zoom', 'clickData')],
             [State('Drop-Tangente', 'value'),
              State('T1X1', 'value'),
              State('T1Y1', 'value'),
              State('T1X2', 'value'),
              State('T1Y2', 'value'),
              State('T2X1', 'value'),
              State('T2Y1', 'value'),
              State('T2X2', 'value'),
              State('T2Y2', 'value')])(dynamically_generated_function)


@app.callback(
    Output('datatable', 'rows'),
    [Input('trc-graph', 'selectedData'),
    Input('btnEssai2', 'n_clicks')])
def update_datatable(selectedData, n_clicks):
    logging.debug('sa marche')
    if n_clicks > 0:
        dfselectdata = pd.DataFrame.from_dict(selectedData['points'], orient='columns')
        dfselectdata['diffy'] = dfselectdata['y'].diff(1)
        dfselectdata['scipy'] = signal.savgol_filter(dfselectdata['y'], 5, 3)
        dfselectdata['filtereddiff'] = dfselectdata['scipy'].diff(1)
        Solution = dfselectdata['x'].loc[dfselectdata['filtereddiff'] == 0]
        logging.debug(Solution)
        return Solution
    else:
        return [{}]

if __name__ == '__main__':
    app.run_server(debug=True)
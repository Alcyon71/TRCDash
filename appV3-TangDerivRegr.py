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
df2 = pd.read_excel('test.xls', sheet_name='Données brutes', index_col=None, header=None)
df2.columns = ['Temps', 'Température', 'Dilatation']

#print(df)

app = dash.Dash()

app.config['suppress_callback_exceptions']=True

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
            html.Div([
                html.H4('Régression 1'),
                html.Div([
                    dcc.Textarea(
                        id='regr1',
                        placeholder='Enter a value...',
                        value='',
                        readOnly=True
                    )
                ]),
            ]),
            html.Div([
                html.H4('Régression 2'),
                html.Div([
                    dcc.Textarea(
                        id='regr2',
                        placeholder='Enter a value...',
                        value='',
                        readOnly=True
                    )
                ]),
            ]),
    ], style={'columnCount': 4}),
    html.Div(id='CalculTangente', children=[
       #html.Button('Calculer Tangente', id='btnTangente', n_clicks=0),
        #html.Button('Essai', id='btnEssai', n_clicks=0),
        html.Button('EssaiCalculdérive', id='btnEssai2', n_clicks=0),
        dcc.RadioItems(
            id='choix',
            options=[
                {'label': 'Rien', 'value': 'rien'},
                {'label': 'Tangente', 'value': 'tang'},
                {'label': 'Dérivé', 'value': 'derive'}
            ],
            value='rien'
        )
    ]),
    html.Div([
        dt.DataTable(
            rows=[{}],
            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable'
        )
    ])
])


#Calcul de l'équation d'un droite avec 2 point
def equation_droite(a,b):
    # y = m x + o
    m = (b['y']-a['y'])/(b['x']-a['x'])
    o = a['y'] - (m*a['x'])
    equation = {'m': m, 'o': o}
    return equation

#calcul intersection
def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def intersection(L1, L2):
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x, y
    else:
        return False

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



#Mise a jour du graph zoon :
# Par selection sur le graph principale
# Par choix dans le radiobutton du choix du calcul : rien - tangente - dérive
@app.callback(
    Output('trc-graph-zoom', 'figure'),
    [Input('trc-graph', 'selectedData'),
     Input('choix', 'value'),
     Input('T1X1', 'value'),
     Input('T1Y1', 'value'),
     Input('T1X2', 'value'),
     Input('T1Y2', 'value'),
     Input('T2X1', 'value'),
     Input('T2Y1', 'value'),
     Input('T2X2', 'value'),
     Input('T2Y2', 'value')])
def graph_selected_data(selectedData, choix, ValT1X1, ValT1Y1, ValT1X2, ValT1Y2, ValT2X1, ValT2Y1, ValT2X2, ValT2Y2):
    if selectedData is not None:
        dfselectdata = pd.DataFrame.from_dict(selectedData['points'], orient='columns')
        if choix == 'rien':
            #logging.debug(selectedData['points'])
            return {'data': [
                {'x': dfselectdata.x, "y": dfselectdata.y, 'mode': 'markers', 'type': 'Scatter',
                 'name': 'Selection'},
                {'x': [ValT1X1, ValT1X2], 'y': [ValT1Y1, ValT1Y2],
                 'mode': 'markers', 'type': 'Scatter', 'name': 'T1',
                 'marker': {'color': 'rgb(255,65,60)', 'line': {'width': 3}, 'symbol': 'circle-open'}},
                {'x': [ValT2X1, ValT2X2], 'y': [ValT2Y1, ValT2Y2],
                 'mode': 'markers', 'type': 'Scatter', 'name': 'T2',
                 'marker': {'color': 'rgb(243,255,60)', 'line': {'width': 3}, 'symbol': 'circle-open'}}
                ],
                    'layout': {'title': 'Selection'
                               }}
        elif choix == 'derive':
            dfselectdata['scipy'] = signal.savgol_filter(dfselectdata['y'], 5, 3)
            dfselectdata['diffy'] = dfselectdata['y'].diff(1)
            dfselectdata['filtereddiff'] = dfselectdata['scipy'].diff(1)
            return {'data': [
                {'x': dfselectdata.x, 'y': dfselectdata.y, 'mode': 'markers', 'type': 'Scatter', 'name': 'Selection'},
                {'x': dfselectdata.loc[dfselectdata['diffy'] == 0].x, 'y': dfselectdata.loc[dfselectdata['diffy'] == 0].y, 'mode': 'markers', 'type': 'Scatter', 'name': 'DiffY',
                 'marker': {'color': 'rgb(255,65,54)', 'line': {'width': 3}, 'symbol': 'circle-open'}},
                {'x': dfselectdata.loc[dfselectdata['filtereddiff'] == 0].x, 'y': dfselectdata.loc[dfselectdata['filtereddiff'] == 0].y,
                 'mode': 'markers', 'type': 'Scatter', 'name': 'DiffFiltrer',
                 'marker': {'color': 'rgb(255,65,60)', 'line': {'width': 3}, 'symbol': 'circle-open'}}
                    ],
                    'layout': {'title': 'Diffy=0'
                               }}
        elif choix == 'tang':
            #On récupere les coordonnées des 2 tangents
            tang1 = {'a': {'x': ValT1X1, 'y': ValT1Y1}, 'b': {'x': ValT1X2, 'y': ValT1Y2}}
            tang2 = {'a': {'x': ValT2X1, 'y': ValT2Y1}, 'b': {'x': ValT2X2, 'y': ValT2Y2}}
            tang1equation = equation_droite(tang1['a'], tang1['b'])
            tang2equation = equation_droite(tang2['a'], tang2['b'])
            dfselectdata['T1Y'] = (tang1equation['m']*dfselectdata.x) + tang1equation['o']
            dfselectdata['T2Y'] = (tang2equation['m'] * dfselectdata.x) + tang2equation['o']
            #dfselectdata['T1X'] = (dfselectdata.y - tang1equation['o'])/tang1equation['m']
            #Calcul du point d'intersection
            L1 = line([ValT1X1, ValT1Y1], [ValT1X2, ValT1Y2])
            L2 = line([ValT2X1, ValT2Y1], [ValT2X2, ValT2Y2])

            R = intersection(L1, L2)
            if R:
                print(R)
            else:
                print("No single intersection point detected")

            return {'data': [
                {'x': dfselectdata.x, 'y': dfselectdata.y, 'mode': 'markers', 'type': 'Scatter', 'name': 'Selection'},
                {'x': dfselectdata.x, 'y': dfselectdata.T1Y, 'mode': 'lines', 'type': 'Scatter', 'name': 'tangente 1'},
                {'x': dfselectdata.x, 'y': dfselectdata.T2Y, 'mode': 'lines', 'type': 'Scatter', 'name': 'tangente 2'},
                {'x': [ValT1X1, ValT1X2], 'y': [ValT1Y1, ValT1Y2],
                 'mode': 'markers', 'type': 'Scatter', 'name': 'T1',
                 'marker': {'color': 'rgb(255,65,60)', 'line': {'width': 3}, 'symbol': 'circle-open'}},
                {'x': [ValT2X1, ValT2X2], 'y': [ValT2Y1, ValT2Y2],
                 'mode': 'markers', 'type': 'Scatter', 'name': 'T2',
                 'marker': {'color': 'rgb(243,255,60)', 'line': {'width': 3}, 'symbol': 'circle-open'}},
                {'x': [R[0]], 'y': [R[1]],
                 'mode': 'markers+text', 'type': 'Scatter', 'name': 'Intersection',
                 'marker': {'color': 'rgb(43,205,30)', 'line': {'width': 5}, 'symbol': 'circle-open'},
                 'text': round(R[0], 2), 'textposition': 'bottom'}
                    ],
                    'layout': {'title': 'Diffy=0'
                               }}
    else:
        return [{}]



#Mise a jour valeur regression linéaire
output_elements_regr = ['regr1', 'regr2']

def create_callback_regr(output):
    def callback_regr(selectedData, DropValue, regr1, regr2):
        if selectedData is not None:
            if (DropValue.split('-')[0] + DropValue.split('-')[1]) == output:
                return selectedData['points'][0][output[2].lower()]
            elif (DropValue.split('-')[0] + DropValue.split('-')[2]) == output:
                return selectedData['points'][0][output[2].lower()]
            else:
                liste = {'regr1': regr1, 'regr2': regr2}
                return [{}]

    return callback_regr

for output_element_regr in output_elements_regr:
    dynamically_generated_function = create_callback_regr(output_element_regr)
    app.callback(Output(output_element_regr, 'value'),
             [Input('trc-graph-zoom', 'selectedData')],
             [State('Drop-Tangente', 'value'),
              State('regr1', 'value'),
              State('regr2', 'value')])(dynamically_generated_function)




#Mise a jour des valeurs des tangents par click sur graph zoom
output_elements = ['T1X1', 'T1Y1', 'T1X2', 'T1Y2', 'T2X1', 'T2Y1', 'T2X2', 'T2Y2']

def create_callback(output):
    def callback(clickData, DropValue, ValT1X1, ValT1Y1, ValT1X2, ValT1Y2, ValT2X1, ValT2Y1, ValT2X2, ValT2Y2):
        if clickData is not None:
            if (DropValue.split('-')[0] + DropValue.split('-')[1]) == output:
                return clickData['points'][0][output[2].lower()]
            elif (DropValue.split('-')[0] + DropValue.split('-')[2]) == output:
                return clickData['points'][0][output[2].lower()]
            else:
                liste = {'T1X1': ValT1X1, 'T1Y1': ValT1Y1, 'T1X2': ValT1X2, 'T1Y2': ValT1Y2, 'T2X1': ValT2X1,
                        'T2Y1': ValT2Y1, 'T2X2': ValT2X2, 'T2Y2': ValT2Y2}
                return liste[output]

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
        return dfselectdata.loc[dfselectdata['diffy'] == 0].to_dict('records')
    else:
        return [{}]

if __name__ == '__main__':
    app.run_server(debug=True)
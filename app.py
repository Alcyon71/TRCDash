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

app.layout = html.Div([
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
            multiple=True
        ),
    html.Div(id='output-graph-upload'),
    # html.Div([
    #             dcc.Markdown(d("""
    #                 **Zoom and Relayout Data**
    #
    #                 Click and drag on the graph to zoom or click on the zoom
    #                 buttons in the graph's menu bar.
    #                 Clicking on legend items will also fire
    #                 this event.
    #             """)),
    #             html.Pre(id='relayout-data', style=styles['pre']),
    #         ], className='three columns')
])



#Traitement des données du fichier et création du graph général
def parse_contents(contents, filename, dates):
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

        return html.Div([
            html.H5(filename),
            #html.H6(datetime.datetime.fromtimestamp(date)),

            # HTML images accept base64 encoded strings in the same format
            # that is supplied by the upload
            html.Hr(),

            dcc.Graph(id='trc_graph', figure={'data': [{'x': df.Température, "y": df.Dilatation, 'type': 'Scatter', 'name': 'Test'}],
                  'layout': {'title': 'Test Titre'
                             }}),

            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
            })
        ])

#Callback de l'upload
@app.callback(Output('output-graph-upload', 'children'),
              [Input('upload-data', 'contents'),
               Input('upload-data', 'filename'),
               Input('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

#TODO : Callback du graph par sélection ou zoom
# @app.callback(
#     Output('relayout-data', 'children'),
#     [Input('trc_graph', 'relayoutData')])
# def display_selected_data(relayoutData):
#     return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
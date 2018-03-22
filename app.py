import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import os

#Import des données
df = pd.read_excel('test.xls', sheet_name='Données brutes', index_col=None, header=None)
df.columns = ['Temps', 'Température', 'Dilatation']

#print(df)

app = dash.Dash()

#CSS offline
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


app.layout = html.Div([
    dcc.Graph(id='graph',
             figure={
                 'data': [
                     {'x': df.Température, "y": df.Dilatation, 'type': 'Scatter', 'name': 'Test'}
                 ],
                 'layout': {
                     'title': 'Test Titre'
                 }
             })
])




if __name__ == '__main__':
    app.run_server(debug=True)
#!/usr/bin/python3

import flask
import dash
from dash import dash_table, html
import pandas as pd

from tdf import coureurs, file


#########
# Serveur
server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, server=server, title='Fantasy Cheat', external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True
server = app.server

df = pd.read_csv(file)

##############
### Layout
app.layout = html.Div(
    children=[
        html.H1('Tour de France 2024 Fantasy League',className='logo'),
        html.Div([
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                ],
                # tooltip={'Fantasy Score': {'type': 'text', 'value': 'Points obtenus lors de la prochaine étape si aucun changement aux classements'}},
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': col},
                        'textAlign': 'left'
                    } for col in ['Coureur','Equipe']
                ] + [
                    {
                        'if': {'column_id': col},
                        'fontWeight': 'bold'
                    } for col in ['Fantasy Score']
                ],
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                data=df.to_dict('records'),
                # editable=True,
                filter_action="native",
                sort_action="native",
                sort_mode="multi",
                sort_by=[{'column_id': 'Fantasy Score', 'direction': 'desc'}],
                # column_selectable="single",
                # row_selectable="multi",
                # row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                # page_current= 0,
                page_size= 300,
            )
        ]),
        html.Div(
            children=[
                "Source : ", html.A("Github", href="https://github.com/tescrihuela/tdf"),
            ]
        )
    ]
)


######
# Main
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')


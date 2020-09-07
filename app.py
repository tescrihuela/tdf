# coding: utf8
#!/usr/bin/python3

import flask
import dash
import dash_table
import dash_html_components as html
import pandas as pd

from tdf import coureurs


file = 'ranking.csv'

#########
# Serveur
server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, server=server, title='Fantasy Cheat', external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

df = pd.read_csv(file)

##############
### Layout
app.layout = html.Div(
    id='page',
    children=[
        html.H1('Tour de France 2020 pour Fantasy League by Gros',className='logo'),
        html.Div([
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
                ],
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
                # column_selectable="single",
                # row_selectable="multi",
                # row_deletable=True,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                # page_current= 0,
                # page_size= 10,
            )
        ]),
        html.Div(id='page-content', className='content', children=[
            "Source : ",
            html.A("Github", href="https://github.com/tescrihuela/tdf"),
        ])
    ]
)


######
# Main
if __name__ == '__main__':
    app.run_server(debug=True)


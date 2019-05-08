# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


df = pd.read_csv('NBA_Players.csv')
style_sheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=style_sheet)
server = app.server

list_of_teams = list(df['TEAM'].unique())
list_of_players = list(df[' NAME'].unique())


def generate_list(dataframe):
    return html.Div(
        children=[html.P(i) for i in dataframe]
    )


app.layout = html.Div(children=[
        html.H1('NBA Statistics'),

        dcc.Graph(
        figure=go.Figure(
            data=[
                go.Scatter(
                    x=df[' NAME'],
                    y=df[' PPG'],
                    mode='markers'
                )
            ],
            layout=go.Layout(
                title='Points Per Game',
            )
        ),
        style={'height': 300},
        id='graph-players-ppg'
        ),
        html.Div(className='row',
            children=[
                html.Div(className='six columns', children=[generate_list(list_of_players)]),
                html.Div(className='six columns', children=[generate_list(list_of_teams)])
            ],
        )

    ],
    style={'padding': 64}
)



if __name__ == '__main__':
    app.run_server(debug=True)
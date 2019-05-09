# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
from dash.dependencies import Input, Output, State


df = pd.read_csv('NBA_Players.csv')
style_sheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=style_sheet)
server = app.server

list_of_teams = list(df['TEAM'].unique())
list_of_players = list(df[' NAME'].unique())
list_of_stats = [" AGE"," HT"," WT", " SALARY", " PPG_LAST_SEASON"," APG_LAST_SEASON"," RPG_LAST_SEASON"," PER_LAST_SEASON"," PPG_CAREER"," APG_CAREER"," RGP_CAREER"," GP"," MPG"," FGM_FGA"," FGP"," THM_THA"," THP"," FTM_FTA"," FTP"," APG"," BLKPG"," STLPG"," TOPG"," PPG"]
list_of_chosen_players = []


def generate_list(dataframe):
    return html.Div(
        children=[html.P(i) for i in dataframe]
    )


app.layout = html.Div(children=[
    html.Img(
            src='assets/nba_logo.png',
            style={'display': 'inline-block',
                   'maxHeight': '100px'}
    ),
    html.H2(children='Statistics 2018/2019'),


    ## Custom Team
    html.Div(className='row', children=[
        html.H2('Create your own custom team'),
        html.P('View the statistics for teams and their individual players. Then when you are decided add them to your personal roster.'),
        html.Ul(className='container', id='custom-team-div')
    ]),

    ## COMPARE TEAMS
    html.Div(className='row', children=[
        html.Div(className='six columns', 
            children=[
                html.H2('List of Teams'),
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[{'label': i, 'value': i} for i in df['TEAM'].unique()],
                    value='Golden State Warriors'
                ),
                html.H2('Compare Stats for Selected Team'),
                dcc.Dropdown(
                    id='stat-dropdown',
                    options=[{'label': i, 'value': i} for i in list_of_stats],
                    value=' HT'
                ),
                html.H2(id='player-on-team-div'),
                dcc.Dropdown(id='players-on-team-dropdown', value='Jordan Bell'),
                html.Button(id='btn_add_to_team', n_clicks=0, children='Add')
            ]
        ),
        html.Div(className='six columns', 
            children=[
                dcc.Graph(id='bar-height')
            ]
        )
    ]),

    ## COMPARE PLAYERS
    html.Div(className='row', children=[
            html.Div(className='six columns', 
                children=[
                    html.H1(id='chosen-player'),
                    html.H2(id='player-team'),
                    html.P('Career Stats'),
                    html.P(id='player-ppg'),
                    html.P(id='player-apg'),
                    html.P(id='player-rpg'),
                    html.P(id='player-bpg'),
                    html.P(id='player-spg')
                ]
            ),
            html.Div(className='six columns', 
                children=[dcc.Graph(id='player_radar')]
            )
        ]
    )

], style={'padding': 64}
)

#Update pick a player text
@app.callback(
    Output('player-on-team-div', 'children'),
    [Input('team-dropdown', 'value')])
def update_team_div(selected_team):
    if(selected_team):
        return '{} Players'.format(selected_team)
    else:
        return 'Pick a Team to select a player'

#Callback for bar graph plotting stats vs players on a team
@app.callback(
    Output('bar-height', 'figure'),
    [Input('team-dropdown', 'value'),
    Input('stat-dropdown', 'value')])
def team_stat_graph(selected_team, selected_stat):
    if(selected_team and selected_stat):
        height_figure = {
            'data': [{
                'x': df[df['TEAM'] == selected_team][' NAME'],
                'y': df[df['TEAM'] == selected_team][selected_stat],
                'type':'bar'
            }],
            'layout': {
                'title': '{} of Players on {}'.format(selected_stat, selected_team)
            }
        }
        return height_figure
    else:
        return {}

#Callback for dropdown to view players on a single team
@app.callback(
    [Output('players-on-team-dropdown', 'options'),
    Output('players-on-team-dropdown', 'value')],
    [Input('team-dropdown', 'value')])
def set_team(selected_team):
    if(selected_team):
        return [{'label': i, 'value': i} for i in df.query('TEAM==@selected_team')[' NAME']], df[df['TEAM'] == selected_team].iloc[0][' NAME']
    else:
        return [], ''

#Callback to view individual player information
@app.callback(
    [Output('chosen-player', 'children'),
    Output('player-team', 'children'),
    Output('player-ppg', 'children'),
    Output('player-apg', 'children'),
    Output('player-rpg', 'children'),
    Output('player-bpg', 'children'),
    Output('player-spg', 'children')],
    [Input('players-on-team-dropdown', 'value')])
def set_player_stats(selected_player,):
    if(selected_player):
        player_index = list_of_players.index(selected_player)
        return '{} {}'.format(selected_player, df[' POSITION'][player_index]), df['TEAM'][player_index], 'Points Per Game: {}'.format(df[' PPG_CAREER'][player_index]), 'Assists Per Game: {}'.format(df[' APG_CAREER'][player_index]), 'Rebounds Per Game:{}'.format(df[' RGP_CAREER'][player_index]), 'Blocks Per Game: {}'.format(df[' BLKPG'][player_index]), 'Steals Per Game: {}'.format(df[' STLPG'][player_index])
    else:
        return 'No Player Selected', '', 'Points Per Game:', 'Assists Per Game:', 'Rebounds Per Game:', 'Blocks Per Game:', 'Steals Per Game:'

#Callback to view individual player radar plot
@app.callback(
    Output('player_radar', 'figure'),
    [Input('players-on-team-dropdown', 'value')])
def set_player_radar(selected_player):
    if(selected_player):
        player_index = list_of_players.index(selected_player)
        data_model = [
            go.Scatterpolar(
                name = str(selected_player),
                r =  [df[' PPG_CAREER'][player_index], df[' APG_CAREER'][player_index], df[' RGP_CAREER'][player_index], df[' BLKPG'][player_index], df[' STLPG'][player_index]],
                theta = ['PPG', 'APG', 'RPG', 'BPG', 'SPG'],
                fill = 'toself'
            ),
        
        ]
        layout_model = go.Layout(
            polar = dict(
                radialaxis = dict(
                    visible = True,
                    range = [0, 35]
                )
            ),
            title=str(selected_player),
        )
        return{
            'data': data_model,
            'layout': layout_model
        }
    else:
        return {}

## Callback to pick custom team
@app.callback(
    Output('custom-team-div', 'children'),
    [Input('btn_add_to_team', 'n_clicks')],
    [State('players-on-team-dropdown', 'value')])
def add_to_team(n_clicks, chosen_player):
    if(n_clicks != 0 and chosen_player):
        player_idx = list_of_players.index(chosen_player)
        list_of_chosen_players.append(chosen_player)
        return [html.Li('{} {}'.format(i, df[' POSITION'][player_idx])) for i in list_of_chosen_players]
    else:
        return 'No Players Chosen'


if __name__ == '__main__':
    app.run_server(debug=True)
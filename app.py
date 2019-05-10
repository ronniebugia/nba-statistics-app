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

app.layout = html.Div(children=[
    html.Div(className='header', children=[
        html.Img(
                src='assets/nba_logo.png',
                style={'display': 'inline-block',
                      'maxHeight': '100px'}
        ),
        html.H2(children='Statistics 2018/2019')
    ]),

    html.Div(className='row', children=[
        html.H2('Create your own custom team'),
        html.P("""
                View the statistics for teams and their individual players. 
                If you want them on your team, add them to your personal roster. 
                You can compare players on one team and their individual statistics. 
                When you are done assembling your starting five along with your seven bench players,
                you can view the collected stats of your team.
                """),
    ]),

    ## COMPARE TEAMS
    html.Div(className='row', children=[
        html.Div(children=[
            html.P('List of Teams'),
            dcc.Dropdown(
                id='team-dropdown',
                options=[{'label': i, 'value': i} for i in df['TEAM'].unique()],
                value='Golden State Warriors'
            )
        ], style={'width': '48%', 'display':'inline-block'}),
        html.Div(children=[
            html.P('Compare Stats for Selected Team'),
            dcc.Dropdown(
                id='stat-dropdown',
                options=[{'label': i, 'value': i} for i in list_of_stats],
                value=' HT'
            )
        ], style={'width': '48%', 'float': 'right',  'display':'inline-block'}),
        dcc.Graph(id='bar-height')
    ]),

    html.Div(className='row', children=[
            html.Div(className='four columns', 
                children=[
                    html.H2(id='player-on-team-div'),
                    dcc.Dropdown(id='players-on-team-dropdown', value='Jordan Bell'),
                    html.Div(id='player-stats'),
                    html.Button(id='btn_add_to_team', n_clicks=0, children='Add')
                ]
            ),
            html.Div(className='eight columns', 
                children=[dcc.Graph(id='player_radar')]
            )
        ]
    ),


    ## View Your Custom Team
    html.Div(className='row', children=[
         
                html.Div(className='three columns', children=[
                    html.H2('Your Custom Team'),
                    dcc.Checklist(
                        id='custom-team-checklist',
                        values=[]
                    ),
                    html.Button(id='btn-remove-from-team', n_clicks=0, children='Remove')
                ]
                ),
                html.Div(className='nine columns', children=[
                    dcc.Graph(id='custom-team-graph')
                ])
            ])
])

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
                'title': '{} of Players on the {}'.format(selected_stat, selected_team)
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
    Output('player-stats', 'children'),
    [Input('players-on-team-dropdown', 'value')])
def set_player_stats_div(selected_player,):
    if(selected_player):
        player_index = list_of_players.index(selected_player)
        return [
            html.H2('{} {}'.format(selected_player, df[' POSITION'][player_index])), 
            html.P('Points Per Game: {}'.format(df[' PPG_CAREER'][player_index])), 
            html.P('Assists Per Game: {}'.format(df[' APG_CAREER'][player_index])), 
            html.P('Rebounds Per Game:{}'.format(df[' RGP_CAREER'][player_index])), 
            html.P('Blocks Per Game: {}'.format(df[' BLKPG'][player_index])), 
            html.P('Steals Per Game: {}'.format(df[' STLPG'][player_index]))
        ]
    else:
        return [
            html.H2('No Player Selected'), 
            html.H2(''),
            html.P('Points Per Game: '),
            html.P('Assists Per Game: '), 
            html.P('Rebounds Per Game: '), 
            html.P('Blocks Per Game: '), 
            html.P('Steals Per Game: ')
        ]


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
    [Output('custom-team-checklist', 'options'),
    Output('custom-team-checklist', 'values')],
    [Input('btn_add_to_team', 'n_clicks'),
    Input('btn_add_to_team', 'n_clicks_timestamp'),
    Input('btn-remove-from-team', 'n_clicks_timestamp')],
    [State('players-on-team-dropdown', 'value'),
    State('custom-team-checklist', 'values')])
def add_to_team_checklist(n_clicks_add, add_time, remove_time, chosen_player, players_to_remove):
    if(remove_time and add_time and remove_time > add_time):
        for i in players_to_remove: 
            list_of_chosen_players.remove(i) 
        return [{'label': '{} {}'.format(i, df[' POSITION'][list_of_players.index(i)]), 'value': i} for i in list_of_chosen_players], []
    elif(n_clicks_add and chosen_player):
        list_of_chosen_players.append(chosen_player)
        return [{'label': '{} {}'.format(i, df[' POSITION'][list_of_players.index(i)]), 'value': i} for i in list_of_chosen_players], [j  for j in players_to_remove]
    else:
        return [], []

#Callback for custom team graph
@app.callback(
    Output('custom-team-graph', 'figure'),
    [Input('custom-team-checklist', 'values')])
def custom_team_graph(custom_team_players):
    if(custom_team_players):
        custom_figure = {
            'data': [{
                'x': [i for i in custom_team_players],
                'y': [df[' PER_LAST_SEASON'][list_of_players.index(i)] for i in custom_team_players],
                'type':'bar'
            }],
            'layout': {
                'title': 'Player Efficiency Rating for your Custom Team'
            }
        }
        return custom_figure
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
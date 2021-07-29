import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta, date
import json
import os
import csv
import plotly.express as px
import plotly.graph_objects as go
from bs4 import BeautifulSoup
import requests
from copy import deepcopy
import pandas 

url = 'http://api.weatherapi.com/v1/forecast.json?key=c300eafa74ce4f6486f75424211806&q=London&days=1&aqi=no&alerts=no'
r = requests.get(url, allow_redirects=True)
open('weather.json', 'wb').write(r.content)

def cross_join(left, right):
    new_rows = [] if right else left
    for left_row in left:
        for right_row in right:
            temp_row = deepcopy(left_row)
            for key, value in right_row.items():
                temp_row[key] = value
            new_rows.append(deepcopy(temp_row))
    return new_rows


def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem


def json_to_dataframe(data_in):
    def flatten_json(data, prev_heading=''):
        if isinstance(data, dict):
            rows = [{}]
            for key, value in data.items():
                rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
        elif isinstance(data, list):
            rows = []
            for i in range(len(data)):
                [rows.append(elem) for elem in flatten_list(flatten_json(data[i], prev_heading))]
        else:
            rows = [{prev_heading[1:]: data}]
        return rows

    return pandas.DataFrame(flatten_json(data_in))

with open(os.getcwd() + r'/weather.json') as json_file:
    json_data = json.load(json_file)

df = json_to_dataframe(json_data)
df.drop(['location.name', 'location.country', 'location.region', 'location.lat', 'location.lon','location.tz_id', 'location.localtime_epoch', 'location.localtime', 'current.uv'], inplace=True, axis=1)
df.rename(columns = {'forecast.forecastday.hour.time':'Date_Time', 'forecast.forecastday.hour.temp_c':'Temperature'}, inplace = True)
df.to_csv('test.csv', mode='w', index=False)
Data = pd.read_csv(os.getcwd() + r'/test.csv', parse_dates=['Date_Time'], infer_datetime_format=True)
Data['Date'] = Data.Date_Time.dt.date
Data['Time'] = Data.Date_Time.dt.time
Data.drop(['Date_Time'], inplace=True, axis=1)
Data.to_csv('weather.csv', mode='w', index=False)

data2 =pd.read_csv(os.getcwd() + r'/weather.csv')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Kendraflow: Elexon!"

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src=app.get_asset_url('FIntricityLargeTrans_DarkColour.jpg'), style={'width': '20%', 'height': 'auto'}, className="header-emoji"),
                html.H2(
                    children="Intraday Temperature", className="header-title"
                ),
                html.P(
                    children="Analyse the Intraday Temperature with kendraflow",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
              html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data2["Time"],
                                    "y": data2["Temperature"],
                                    "type": "lines",
                                    "hovertemplate": "°C %{y:.2f}"
                                                       "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Temperature for %s" %(data2.Date[1]),
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True, "title": "Time (GMT)",},
                                "yaxis": {"fixedrange": True, "title": "Temperature (°C)",},
                                "colorway": ["#E12D39"],
                            },
                        },
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

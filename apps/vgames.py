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
from copy import deepcopy

today = date.today()
d = today - timedelta(days=1)
url = 'https://api.carbonintensity.org.uk/regional/intensity/%s/%s/regionid/13' %(d, today)
r = requests.get(url, allow_redirects=True)
open('carbon_intensity.json', 'wb').write(r.content)

from copy import deepcopy
import pandas


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

with open(os.getcwd() + r'/carbon_intensity.json') as json_file:
    json_data = json.load(json_file)

df = json_to_dataframe(json_data)
df.drop(['data.regionid', 'data.dnoregion', 'data.shortname', 'data.data.intensity.index'], inplace=True, axis=1)
#, 'data.data.generationmix.fuel','data.data.generationmix.perc'
df.rename(columns = {'data.data.from':'From', 'data.data.to':'To', 'data.data.intensity.forecast':'Intensity','data.data.generationmix.fuel':'Fuel','data.data.generationmix.perc':'Value'}, inplace = True)
df.to_csv('carbon_intensity.csv', mode='w', index=False)


data = pd.read_csv(os.getcwd() + r'/carbon_intensity.csv')


#data["Date"] = pd.to_datetime(data["To"], format="%Y-%m-%d")
#data.sort_values("Date", inplace=True)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Kendraflow: Carbon Intensity!"

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src=app.get_asset_url('FIntricityLargeTrans_DarkColour.jpg'), style={'width': '20%', 'height': 'auto'}, className="header-emoji"),
                html.H2(
                    children="Carbon Intensity Analytics For London", className="header-title"
                ),
                html.P(
                    children="Analyse the carbon intensity with kendraflow",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="price-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data["To"],
                                    "y": data["Intensity"],
                                    "type": "lines",
                                    "hovertemplate": "gCO2/kWh %{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Carbon Intensity (gCO2/kWh)",
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True, "title": "Date & Time (GMT)",},
                                "yaxis": {
                                    #"tickprefix": "gCO2e/kWh",
                                    "title": "Intensity (gCO2/kWh)",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
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

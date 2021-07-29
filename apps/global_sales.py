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

url = 'https://api.bmreports.com/BMRS/ROLSYSDEM/v1?APIKey=3pyyl4iymgrn812&ServiceType=xml'
r = requests.get(url, allow_redirects=True)
open('demand.xml', 'wb').write(r.content)

# Open XML file
file = open(os.getcwd() + r'/demand.xml', 'r')
  
# Read the contents of that file
contents = file.read()
  
soup = BeautifulSoup(contents, 'xml')
  
# Extracting the data
settDate = soup.find_all('settDate')
publishingPeriodCommencingTime = soup.find_all('publishingPeriodCommencingTime')
fuelTypeGeneration = soup.find_all('fuelTypeGeneration')

data = []
  
# Loop to store the data in a list named 'data'
for i in range(0, len(fuelTypeGeneration)):
    rows = [ settDate[i].get_text(), publishingPeriodCommencingTime[i].get_text(), fuelTypeGeneration[i].get_text()]
    data.append(rows)
  
# Converting the list into dataframe
df = pd.DataFrame(data, columns=['settDate', 'publishingPeriodCommencingTime', 
                                 'fuelTypeGeneration' ], dtype = float)
df.rename(columns={ "publishingPeriodCommencingTime" : "Time", "settDate" : "Date", "fuelTypeGeneration": "Demand" }, inplace = True)
df['Time'] = df['Time'].apply(lambda x: x[:5])
df.to_csv('demand.csv', index=False)


data = pd.read_csv(os.getcwd() + r'/demand.csv')



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
                    children="Elexon Flex Market Intraday Data", className="header-title"
                ),
                html.P(
                    children="Analyse the Elexon Intraday data with kendraflow",
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
                                    "x": data["Time"],
                                    "y": data["Demand"],
                                    "type": "lines",
                                    "hovertemplate": "MW %{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Rolling System Demand (MW) for %s" %(data.Date[1]),
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True, "title": "Time (GMT)", },
                                "yaxis": {
                                    "title": "Demand (MW)",
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

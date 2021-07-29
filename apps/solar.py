import requests
from datetime import datetime, timedelta, date
import pandas as pd 
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta, date
import os
import csv
import plotly.express as px

today = date.today()
d1 = today - timedelta(days=1)
url = 'https://api0.solar.sheffield.ac.uk/pvlive/v2?start=%sT00:00:00&end=%sT23:00:00&data_format=csv' %(d1,d1)
r = requests.get(url, allow_redirects=True)
open('demand12.csv', 'wb').write(r.content)
data=pd.read_csv(os.getcwd() + r'/demand12.csv') 
for i in range(data.shape[0]): 
    if i%2 != 0:
                 data = data.drop([i], axis = 0)
data.to_csv('d1.csv', encoding='utf-8', index=False)
Data = pd.read_csv(os.getcwd() + r'/d1.csv', parse_dates=['datetime_gmt'], infer_datetime_format=True)
Data['Date1'] = Data.datetime_gmt.dt.date
Data['Time1'] = Data.datetime_gmt.dt.time
Data.drop(['datetime_gmt'], inplace=True, axis=1)
Data.to_csv('solar.csv', mode='w', index=False)
data = pd.read_csv(os.getcwd() + r'/solar.csv')

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Kendraflow: Solar!"

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src=app.get_asset_url('FIntricityLargeTrans_DarkColour.jpg'), style={'width': '20%', 'height': 'auto'}, className="header-emoji"),
                html.H2(
                    children="Solar Energy Production in UK", className="header-title"
                ),
                html.P(
                    children="Analyse the solar energy production with kendraflow",
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
                                    "x": data["Time1"],
                                    "y": data["generation_mw"],
                                    "type": "lines",
                                    "hovertemplate": "MW %{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Solar Energy Production for %s" %(data.Date1[1]),
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True, "title": "Time (GMT)",},
                                "yaxis": {
                                    #"tickprefix": "gCO2e/kWh",
                                    "title": "Energy Produced (MW)",
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
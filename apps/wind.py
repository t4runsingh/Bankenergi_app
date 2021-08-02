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

today = date.today()
d2 = today - timedelta(days=1)
url = 'https://api.bmreports.com/BMRS/B1440/v1?APIKey=3pyyl4iymgrn812&SettlementDate=%s&Period=*&ServiceType=xml' %(d2)
r = requests.get(url, allow_redirects=True)
open('wind.xml', 'wb').write(r.content)


# Open XML file
file = open(os.getcwd() + r'/wind.xml', 'r')
  
# Read the contents of that file
contents = file.read()
  
soup = BeautifulSoup(contents, 'xml')
  
# Extracting the data
businessType = soup.find_all('businessType')
powerSystemResourceType = soup.find_all('powerSystemResourceType')
settlementDate = soup.find_all('settlementDate')
settlementPeriod = soup.find_all('settlementPeriod')
quantity = soup.find_all('quantity')

data = []

# Loop to store the data in a list named 'data'
for i in range(0, len(quantity)):
    rows = [ businessType[i].get_text(), powerSystemResourceType[i].get_text(), settlementDate[i].get_text(), settlementPeriod[i].get_text(), quantity[i].get_text()]
    data.append(rows)
  
# Converting the list into dataframe
df = pd.DataFrame(data, columns=['businessType', 'powerSystemResourceType', 'settlementDate' , 'settlementPeriod', 'quantity'
                                 'settlementDate' ], dtype = float)
df.rename(columns={ "powerSystemResourceType" : "wind_type", "businessType" : "type", "settlementDate": "date", "settlementPeriod": "period", "quantity" : "quantity" }, inplace = True)
df.to_csv('wind.csv', index=False)
df = pd.read_csv(os.getcwd() + r'/wind.csv')
df = df.replace(['\"','\"'], ['',''], regex=True)
df.to_csv('wind.csv', index=False)
data=pd.read_csv(os.getcwd() + r'/wind.csv') 
for i in range(data.shape[0]): 
    if i%3 == 0:
                 data = data.drop([i], axis = 0)
data.to_csv('wind1.csv', encoding='utf-8', index=False)
data=pd.read_csv(os.getcwd() + r'/wind1.csv') 
for i in range(data.shape[0]): 
    if i%2 == 0:
                 data = data.drop([i], axis = 0)
data.to_csv('wind2.csv', encoding='utf-8', index=False)
data=pd.read_csv(os.getcwd() + r'/wind1.csv') 
for i in range(data.shape[0]): 
    if i%2 != 0:
                 data = data.drop([i], axis = 0)
data.to_csv('wind3.csv', encoding='utf-8', index=False)



data = pd.read_csv(os.getcwd() + r'/wind2.csv', nrows=48)
data2 = pd.read_csv(os.getcwd() + r'/wind3.csv', nrows=48)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Kendraflow: Wind!"

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src=app.get_asset_url('FIntricityLargeTrans_DarkColour.jpg'), style={'width': '20%', 'height': 'auto'}, className="header-emoji"),
                html.H2(
                    children="Wind Generation Intraday Data", className="header-title"
                ),
                html.P(
                    children="Analyse the Wind Generation Intraday data with kendraflow",
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
                                    "x": data["period"],
                                    "y": data["quantitysettlementDate"],
                                    "type": "lines",
                                    "hovertemplate": "MW %{y:.2f}"
                                                     "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Wind Generation onshore (MW) for %s" %(data.date[1]),
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True, "title": "Time (GMT)", },
                                "yaxis": {
                                    "title": "Wind Generated (MW)",
                                    "fixedrange": True,
                                },
                                "colorway": ["#17B897"],
                            },
                        },
                    ),
                    className="card",
                ),
              html.Div(
                    children=dcc.Graph(
                        id="volume-chart",
                        config={"displayModeBar": False},
                        figure={
                            "data": [
                                {
                                    "x": data2["period"],
                                    "y": data2["quantitysettlementDate"],
                                    "type": "lines",
                                    "hovertemplate": "MW %{y:.2f}"
                                                       "<extra></extra>",
                                },
                            ],
                            "layout": {
                                "title": {
                                    "text": "Wind Generation offshore for %s" %(data2.date[1]),
                                    "x": 0.05,
                                    "xanchor": "left",
                                },
                                "xaxis": {"fixedrange": True, "title": "Time (GMT)",},
                                "yaxis": {"fixedrange": True, "title": "Wind Generated (MW)",},
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
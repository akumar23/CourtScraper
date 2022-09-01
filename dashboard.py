import courtscraper
import pandas as pd
import plotly.express as px
import dash
from os.path import exists
from dash import html
from dash import dcc

if not exists('caseData.csv') and not exists('links.csv'):
    san_fran = courtscraper.sfCourt()
    san_fran.byPassCaptcha()

    court_data = san_fran.getDataAtDate()

    dfData = pd.DataFrame(court_data.items(), columns=['CaseNumber', 'CaseTitle'])
    dfLinks = pd.DataFrame(san_fran.linkData.items(), columns=['CaseNumber', 'CaseLink'])

    dfData.to_csv('caseData.csv', index=False) 
    dfLinks.to_csv('links.csv', index=False)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
 
colors = {
    'background': '#F0F8FF',
    'text': '#00008B'
}

df = pd.read_csv('caseData.csv')
link = pd.read_csv('links.csv') 

fig = px.scatter(df, x='CaseNumber', y='CaseTitle')
fig.update_traces(mode='markers+lines')
 
app.layout = html.Div(children=[
    html.H1(children='San Francisco Court Data'),
 
    html.Div(children='''
        Court Data: San Francisco
    '''),
 
    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
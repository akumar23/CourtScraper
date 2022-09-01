import courtscraper
import pandas as pd
import plotly.express as px
import dash
from os.path import exists
from dash import html
from dash import dcc
import streamlit as st
import numpy as np


if not exists('caseData.csv') and not exists('links.csv'):
    san_fran = courtscraper.sfCourt()
    san_fran.byPassCaptcha()

    court_data = san_fran.getDataAtDate()

    dfData = pd.DataFrame(court_data.items(), columns=['CaseNumber', 'CaseTitle'])
    dfLinks = pd.DataFrame(san_fran.linkData.items(), columns=['CaseNumber', 'CaseLink'])

    dfData.to_csv('caseData.csv', index=False) 
    dfLinks.to_csv('links.csv', index=False)
    san_fran.pushToDB()


st.title('Court Data')
st.header('San Francisco')

df = pd.read_csv('caseData.csv')
link = pd.read_csv('links.csv') 

st.dataframe(df)
st.dataframe(link)

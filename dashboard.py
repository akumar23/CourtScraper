import datetime
from select import select
import courtscraper
import pandas as pd
import plotly.express as px
import dash
from os.path import exists
from dash import html
from dash import dcc
import streamlit as st
import numpy as np


def getData(date):
    if not exists(f'caseData{date}.csv') and not exists(f'links{date}.csv'):
        san_fran = courtscraper.sfCourt()
        san_fran.byPassCaptcha()

        court_data = san_fran.getDataAtDate(date)

        dfData = pd.DataFrame(court_data.items(), columns=['CaseNumber', 'CaseTitle'])
        dfLinks = pd.DataFrame(san_fran.linkData.items(), columns=['CaseNumber', 'CaseLink'])

        dfData.to_csv(f'caseData{date}.csv', index=False) 
        dfLinks.to_csv(f'links{date}.csv', index=False)
        #san_fran.pushToDB()


st.title('Court Data')
st.header('San Francisco')

select_date = st.date_input('Click Here to Select Date', datetime.date.today() + datetime.timedelta(1))

if select_date != datetime.date.today() + datetime.timedelta(1):
    getData(select_date)

    df = pd.read_csv(f'caseData{select_date}.csv')
    link = pd.read_csv(f'links{select_date}.csv') 

    st.dataframe(df)
    st.dataframe(link)
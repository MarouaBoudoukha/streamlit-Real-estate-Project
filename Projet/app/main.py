import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import read_data, head, map_price_by_location,price_by_month
from streamlit_option_menu import option_menu
from utils import set_bg, body1, price_by_location, vente_by_month, pre_processing, graph_repartition,line_chart_price_evolution

#st.set_page_config(
#    page_title='Estimateur des prix immobiliers',
#    page_icon='/Users/maroua/Desktop/M1/Streamlit/Projet/assets/icon.jpeg'
#) 


set_bg('/Users/maroua/Desktop/M1/Streamlit/Projet/assets/background2.jpeg')
df_20 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2020.csv')
df_19 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2019.csv')
df_18 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2018.csv')
df_17 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2017.csv')

st.sidebar.header("Options:")
with st.sidebar :
    selected = option_menu("Main menu :", ["Analyses", "Visualisations", "Comparateur de biens"], icons=["Accueil","Estimateur de prix", "Comparateur de biens"], menu_icon="cast")
    selected

if selected == "Analyses" : 
    head()
    
    body1()

if selected == "Visualisations" : 

    st.title("Visualisations")
    st.write("""
        <h1 style='font-size:25px'>
        choisissez l'année \U0001F642.
        </h1>
    """, unsafe_allow_html=True
    )
    year = st.select_slider("select a year",options=['2017','2018','2019','2020'])
    if year == '2017':
        price_by_month()
    
        
    if year == '2018':
        option = st.selectbox(
        'Price by location',
        ('Map', 'Barchart'))

        st.write('You selected:', option)
        if option == 'Map' :
            map_price_by_location()
        
        if option == "Barchart" :
            vente_by_month()
        
    if year == '2019':
        option = st.selectbox(
        'Price by location',
        ('Linechart','Map'))

        st.write('You selected:', option)
        if option == 'Linechart' :  
            line_chart_price_evolution()
        if option == 'Map' :
            map_price_by_location()
        
        
    if year == '2020':
        graph_repartition()
        
    

if selected == "Comparateur de biens" : 
    st.title("Comparateur de biens")
    st.markdown("Nous allons comparer les biens immobiliers en se basant sur plusieurs critères")    

        #df = pd.read_csv("ny-trips-data.csv", delimiter = ',')
        #st.write(df)




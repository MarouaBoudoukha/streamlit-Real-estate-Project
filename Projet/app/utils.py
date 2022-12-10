import base64
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu

#Pré-processing
def pre_processing(data):
    df = read_data(data)
    #df_sample = pd.read_csv(data).sample(frac=0.1)
    #Drop columns that have a rate of missing values greater than 90%
    
    df = df.drop(['numero_disposition',
                                'ancien_code_commune',
                                'adresse_suffixe',
                                'ancien_nom_commune',
                                'ancien_id_parcelle',
                                'numero_volume',
                                'lot1_numero',
                                'lot1_surface_carrez',
                                'lot2_numero',
                                'lot2_surface_carrez',
                                'lot3_numero',
                                'lot3_surface_carrez',
                                'lot4_numero',
                                'lot4_surface_carrez',
                                'lot5_numero',
                                'lot5_surface_carrez',
                                'code_nature_culture',
                                'nature_culture',
                                'code_nature_culture_speciale',
                                'nature_culture_speciale',
                                'code_commune',
                                'code_type_local',
                                'nombre_lots',
                                'code_type_local',
                                'surface_reelle_bati',
                                'code_departement'
                                ],axis= 1)
    #Changer le types de variables (savoir la distribution des variables qualitatives et quantitatives afin de faire la correlation)
    df['code_postal'] = df['code_postal'].astype(float)
    #df['code_type_local'] = df['code_type_local'].astype('object')

    df['lon'] = df['longitude'].dropna()
    df['lat'] = df['latitude'].dropna()
    df['nombre_pieces_principales'] = df['nombre_pieces_principales'].dropna()
    #df['nombre_pieces_principales'] = list(map(lambda s: s.replace('NA', ''), df['nombre_pieces_principales']))
    df = df.drop(['latitude','longitude','id_parcelle'],axis=1)

    df['lat']=pd.to_numeric(df['lat'], errors='coerce',downcast='signed')
    df['lon']=pd.to_numeric(df['lon'], errors='coerce',downcast='signed')

    

    print(df.info())
    #df['lon']=df['lon'].astype(int, errors='ignore')
    
    df['type_local'] = df['type_local'].astype('object')
    df['date_mutation']= pd.to_datetime(df['date_mutation'], errors='coerce')
    df['nombre_pieces_principales'] = df['nombre_pieces_principales'].astype(int, errors='ignore')
    #df['code_departement'] = df['code_departement'].dropna()
    #df['code_departement'] = df['code_departement'].astype(int, errors='ignore')
    
    #df['nombre_lots'] = df['nombre_lots'].astype('float64')
    df.dropna(inplace=True)
    
    
    #Traiter les données manquantes
    # L'imputation des données manquantes
    df['type_local'] = df['type_local'].fillna("None")
    df['valeur_fonciere'] = df['valeur_fonciere'].transform(lambda x: x.fillna(x.mean()))
    
    #df['nombre_pieces_principales'] = df['nombre_pieces_principales'].fillna(0)
    #df['surface_reelle_bati'] = df['surface_reelle_bati'].fillna(0)
    df['surface_terrain'] = df['surface_terrain'].fillna(0)
    
    return df


#reading data
@st.cache(suppress_st_warning=True)
def read_data(path):
    return pd.read_csv(path, delimiter=',').sample(frac=0.1)

#encode the image and return the encoded bytes (Streamlit doesn't natively support custom backgrounds)
@st.cache(allow_output_mutation=True)
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#setting background
def set_bg(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = """
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
    """ % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)



# writing head 
def head():
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: -35px;font-size:50px'>
        Analyses et visualisations
        </h1>
    """, unsafe_allow_html=True
    )
    
    st.caption("""
        <p style='text-align: center;font-size:24px'>
        Demandes de valeurs foncières <a href='https://www.data.gouv.fr/en/datasets/demandes-de-valeurs-foncieres/'>DVF</a>
        </p>
    """, unsafe_allow_html=True
    )
df_20 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2020.csv')
df_19 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2019.csv')
df_18 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2018.csv')
df_17 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2017.csv')

def filter_by_nombre_pieces_principales():
    option = st.selectbox(
        'nombre de pièces principales',
        ('1', '2', '3','4','5','6','7','8','9','10','11'))

    st.write('You selected:', option)
    df= df[df['nombre de pièces principales']].isin(option)
    
def filter_by_type_local():
    option = st.selectbox(
        'local',
        ('Maison', 'Appartement','Dépendance','Local industriel. commercial ou assimilé'))

    st.write('You selected:', option)
    if option == 'Maison' :
        df = df_20[df_20['type_local'] == 'Maison']
        st.write(df)
    if option == 'Appartement' :
        df = df_20[df_20['type_local'] == 'Appartement']
        st.write(df)
    if option == 'Dépendance' :
        df = df_20[df_20['type_local'] == 'Dépendance']
        st.write(df)
    if option == 'Local industriel. commercial ou assimilé' :
        df = df_20[df_20['type_local'] == 'Local industriel. commercial ou assimilé']
        st.write(df)
    
    


# writing body Accueil
def body1():
    st.write("""
        <h1 style='font-size:25px'>
        choisissez l'année \U0001F642.
        </h1>
    """, unsafe_allow_html=True
    )
    year = st.select_slider("select a year",options=['2017','2018','2019','2020'])
    if year == '2017':
        
        nature_mutation = st.radio("nature_mutation",('Vente', "All_data"), key="vertical")
        
        if nature_mutation == 'Vente':
            
            filtered_df = df_17[df_17["nature_mutation"] == 'Vente']
            filter_by_type_local()
            
        if nature_mutation == 'All_data':
            filter_by_type_local()
            #st.write(df_17)
    if year == '2018':
        nature_mutation = st.radio("nature_mutation",('Vente', "All_data"), key="vertical")
        
        if nature_mutation == 'Vente':
            filter_by_type_local()
            filtered_df = df_18[df_18["nature_mutation"] == 'Vente']
            #st.write(filtered_df)
        if nature_mutation == 'All_data':
            filter_by_type_local()
            #st.write(df_18)
        
    
        
    if year == '2020':
        
        nature_mutation = st.radio("nature_mutation",('Vente', "All_data"), key="vertical")
        
        if nature_mutation == 'Vente':
            filter_by_type_local()
            filtered_df = df_20[df_20["nature_mutation"] == 'Vente']
            #st.write(filtered_df)
        if nature_mutation == 'All_data':
            filter_by_type_local()
            #st.write(df_20)
        #an_20()
    if year == '2019':
        nature_mutation = st.radio("nature_mutation",('Vente', "All_data"), key="vertical")
        
        if nature_mutation == 'Vente':
            filter_by_type_local()
            filtered_df = df_19[df_19["nature_mutation"] == 'Vente']
            #st.write(filtered_df)
        if nature_mutation == 'All_data':
            filter_by_type_local()
            #st.write(df_19)
        
    
def price_by_month() :
    st.subheader("Evolution du prix moyen par mois")
    df_17 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2017.csv')
    df_17['mois'] = df_17['date_mutation'].dt.month
    df_17= df_17.groupby('mois').mean()['valeur_fonciere'].reset_index()
    fig = px.line(df_17, x=df_17['mois'], y="valeur_fonciere")
    st.plotly_chart(fig)



        
    
def graph_repartition():
    option = st.selectbox(
        'select repatrition criteria',
        ('local type', 'mutation nature'))

    st.write('You selected:', option)
    if option == 'local type' :
        # Visualiser la répartition la variable type_local
        st.subheader("Répartition by local type")

        plt.figure(figsize=(10,10))
        labels = ['Donées Manquantes', 'Maison', 'Appartement', 'Dépendance', 'Local industriel. commercial ou assimilé']
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#fffc52']
        area = [41, 21.4, 18, 12.9, 0.37]
        #area = [91.93, 6.88, 0.82, 0.28,0.056]
        explode = (0.05,0.05,0.1,0.1,0.1)
        fig, ax = plt.subplots()
        ax.pie(area, labels=labels, explode=explode, colors= colors, startangle=65, autopct='%1.1f%%',shadow='True')
        st.pyplot(fig)
            
            
    if option == 'mutation nature' :

        # Visualiser la répartition de la nature de mutation

        st.subheader("Repartition by mutation nature")
        plt.figure(figsize=(10,10))
        labels = ['Vente', 'VEFA', 'Echange', 'Vente Terrain', 'Adjudication']
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#fffc52']
        area = [92, 6.8, 0.82, 0.28, 0.56]
            #area = [91.93, 6.88, 0.82, 0.28,0.056]
        explode = (0.05,0.05,0.2,0.3,0.4)
        fig, ax = plt.subplots()
        ax.pie(area, labels=labels, explode=explode, colors= colors, startangle=65, autopct='%1.1f%%',shadow='True')
        st.pyplot(fig)    


def price_by_location():
        st.write("""
            <h1 style='font-size:25px'>
            Prix moyen par ville \U0001F642.
            </h1>
        """, unsafe_allow_html=True
        )
        df_19 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2019.csv')
        df_19 = df_19.groupby('code_departement')['valeur_fonciere'].mean().reset_index()
        df_19 = df_19.sort_values(by='valeur_fonciere', ascending=False)
        df_19 = df_19.head(50)
        df_19 = df_19.sort_values(by='valeur_fonciere', ascending=True)
        st.bar_chart(df_19)
        

def line_chart_price_evolution():
    st.write("""
            <h1 style='font-size:25px'>
            Evolution du prix moyen par mois \U0001F642.
            </h1>
        """, unsafe_allow_html=True
        )
    df_20 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2020.csv')

    df_20['mois'] = df_20['date_mutation'].dt.month
    df_20= df_20.groupby('mois').mean()['valeur_fonciere'].reset_index()
    st.line_chart(df_20)

def vente_by_month():
    st.write("""
        <h1 style='font-size:25px'>
        Nombre de vente par mois \U0001F642.
        </h1>
    """, unsafe_allow_html=True
    )
    df_18 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2019.csv')
    
    df_18['mois'] = df_18['date_mutation'].dt.month
    df_18 = df_18.groupby('mois').count()["id_mutation"].reset_index()
    #df_19 = df_19.sort_values(by='valeur_fonciere', ascending=False)
    # df_19 = df_19.head(50)
    #df_19 = df_19.sort_values(by='valeur_fonciere', ascending=True)
    st.bar_chart(df_18)


def map_price_by_location():
    df_18 = pre_processing('/Users/maroua/Desktop/M1/Streamlit/Projet/data/full_2018.csv')
    
    st.write("""
        <h1 style='font-size:25px'>
        Prix moyen par ville \U0001F642.
        </h1>
    """, unsafe_allow_html=True)
    #print(df_20.info())
    map18 = df_18[['lon', 'lat']].copy()
    print(map18.head())
    st.map(map18)

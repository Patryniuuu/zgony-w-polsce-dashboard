import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import geopandas as gpd
@st.cache_data
def load_map_data(path):
    mapa_pl = gpd.read_file(path)
    mapa_pl['geometry'] = mapa_pl['geometry'].simplify(0.005, preserve_topology=True)
    return mapa_pl

def wykres_mapa(filtered_df):
    mapa_pl=load_map_data(r'dane/A01_Granice_wojewodztw.shp')
    filtered_df=filtered_df[filtered_df["Płeć"]=='ogółem']
    filtered_df=filtered_df[filtered_df["Miasta...wieś"]=='ogółem']
    mapa_final = mapa_pl.merge(filtered_df, left_on='JPT_NAZWA_', right_on='Nazwa')
    fig = px.choropleth(
        mapa_final,
        geojson=mapa_final.__geo_interface__,
        locations='JPT_NAZWA_',
        featureidkey="properties.JPT_NAZWA_",
        color='Wartosc',
        color_continuous_scale="Viridis",
        labels={'Wartosc': 'Wartość (na 100 tys. osób)', 'JPT_NAZWA_':'Nazwa województwa'}
    )
    fig.update_layout(
        title='',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_geos(bgcolor='rgba(0,0,0,0)', projection_type="mercator",fitbounds="locations", visible=False)
    event = st.plotly_chart(fig, config={'uwidth': 'stretch'}, on_select="rerun", selection_mode='points')
    if len(event.get('selection').get('points'))==0:
        woj=0
    else:
        woj=event.get('selection').get('points',0)[0].get('location')
    return woj

    





# mapa_final.plot(
#     column='Wartosc', 
#     cmap=sns.light_palette("#87ae73", as_cmap=True), 
#     linewidth=0.8, 
#     ax=ax, 
#     edgecolor='white', #Białe granice województw
#     legend=True,
#     legend_kwds={'label': "Liczba samobójstw (na 100 tys. mieszkańców)", 'orientation': "horizontal", 'pad': 0.05}
# )

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def wykres_woj_mw(filtered_df, wojewodztwo):
    filtered_df=filtered_df[filtered_df["Miasta...wieś"]!='ogółem']
    filtered_df=filtered_df[filtered_df["Płeć"]=='ogółem']
    if wojewodztwo != 0:
        filtered_df=filtered_df[filtered_df['Nazwa']==wojewodztwo]
    else:
        filtered_df=filtered_df[filtered_df['Nazwa']=='polska']
    fig = px.bar(
        data_frame=filtered_df,
        y = "Wartosc",
        x = "Przyczyny.zgonów",
        color="Miasta...wieś",
        text_auto=True,
        title="Przyczyny zgonow",
        color_discrete_map={
            "miasto": "#7f7f7f",
            "wieś": "#2ca02c"
        },
        labels={'Wartosc': 'Wartość (na 100 tys. osób)', 'Przyczyny.zgonów':'Przyczyna zgonów', 'Miasta...wieś': 'Miejsce zamieszkania'}
    )
    fig.layout.update(title= '',yaxis_title="Liczba zgonów (na 100 tys. osób)", xaxis_title="Przyczyna zgonów")
    
    st.plotly_chart(fig, use_container_width=True)
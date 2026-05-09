import pandas as pd
import streamlit as st
import plotly.express as px
import textwrap


def wykres_slupki(filtered_df, wybor):
    df_grouped = filtered_df.groupby(["Przyczyny.zgonów", wybor])["Wartosc"].mean().reset_index()
    
    df_plot = df_grouped.copy()
    
    df_plot['Przyczyny.zgonów'] = df_plot['Przyczyny.zgonów'].apply(
        lambda nazwa: '<br>'.join(textwrap.wrap(nazwa, width=35))
    )
    
    if wybor == "Miasta...wieś":
        zm = "miejsce zamieszkania"
        moje_kolory = {
            "miasto": "#FF9f36", 
            "wieś": "#2ca02c"    
        }
    else:
        zm = "płeć"
        moje_kolory = {
            "kobiety": "#e377c2",  
            "mężczyźni": "#1f77b4" 
        }
    
    fig = px.bar(
        data_frame=df_plot,
        x="Wartosc",
        y="Przyczyny.zgonów",
        color=wybor,
        color_discrete_map=moje_kolory,  
        orientation="h",
        barmode="group",
        height=700,
        title=f"Przyczyny zgonów z podziałem na {zm}",
        labels={
            "Przyczyny.zgonów": "Choroba",
            "Wartosc": "Liczba zgonów (na 100 tys. osób)"
        }  
    )
    
    fig.update_layout(
        title_x=0.5,
        title_y=0.9,
        xaxis_title="Liczba zgonów (na 100 tys. osób)",
        yaxis={'categoryorder': 'total ascending'},    
        bargap=0.15,         
        bargroupgap=0.05     
    )
    
    st.plotly_chart(fig, use_container_width=True)




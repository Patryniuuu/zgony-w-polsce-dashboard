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
            "Wartosc": "Liczba zgonów (na 100 tys. osób)",
            "Miasta...wieś": "Obszar zamieszkania"
        }  
    )
    
    fig.update_layout(
        title_x=0.4,
        title_y=0.9,
        xaxis_title="Liczba zgonów (na 100 tys. osób)",
        yaxis={'categoryorder': 'total ascending'},    
        bargap=0.15,         
        bargroupgap=0.05     
    )
    
    # Formatowanie dymka (hover) - zamiana "=" na ": "
    fig.update_traces(
        hovertemplate=(
            "<b>%{y}</b><br><br>"                       # Pogrubiona nazwa choroby na samej górze
            "Przekrój: %{customdata[0]}<br>"            # Płeć lub Miejsce zamieszkania
            "Wskaźnik zgonów: <b>%{x:.1f}</b><br>"       # Liczba zgonów zaokrąglona do 1 miejsca po przecinku
            "<extra></extra>"                           # Ten pusty tag usuwa brzydki boczny pasek z nazwą serii
        ),
        # Musimy przekazać zmienną 'wybor' jako customdata, żeby template mógł ją przeczytać
        customdata=df_plot[[wybor]]
    )
    
    st.plotly_chart(fig, use_container_width=True)




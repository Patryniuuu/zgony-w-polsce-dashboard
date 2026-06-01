import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def wykres_woj_plec(filtered_df, wojewodztwo):
    filtered_df=filtered_df[filtered_df["Miasta...wieś"]=='ogółem']
    filtered_df=filtered_df[filtered_df["Płeć"]!='ogółem']
    if wojewodztwo != 0:
        filtered_df=filtered_df[filtered_df['Nazwa']==wojewodztwo]
    else:
        filtered_df=filtered_df[filtered_df['Nazwa']=='polska']
    fig = px.bar(
        data_frame=filtered_df,
        y = "Wartosc",
        x = "Przyczyny.zgonów",
        color="Płeć",
        barmode='group',
        text_auto=True,
        title="Przyczyny zgonow",
        color_discrete_map={
            "mężczyźni": "#1f77b4",
            "kobiety": "#e377c2"
        },
        labels={'Wartosc': 'Wartość (na 100 tys. osób)', 'Przyczyny.zgonów':'Przyczyna zgonów'}
    )
    fig.layout.update(title='', 
                      yaxis_title="Liczba zgonów (na 100 tys. osób)", 
                      xaxis_title="Przyczyna zgonów",
                      bargap=0.3, 
                      bargroupgap=0.1,
                      margin=dict(l=70, r=20, t=10, b=30), 
                      yaxis=dict(automargin=False),         
                      xaxis=dict(automargin=False),
                      legend=dict(
                        entrywidth=65,
                        entrywidthmode="pixels",
                        orientation="h",  
                        yanchor="bottom", 
                        y=1.02,           
                        xanchor="center",
                        x=0.5,                 
                        bgcolor="rgba(0,0,0,0)"
                        )
                      )
    fig.update_xaxes(
    title_text='',        
    showticklabels=False)
    fig.update_traces(width=0.3, hovertemplate="Przyczyna zgonów: %{x}<br>" +
                  "Płeć: %{data.name}<br>" +
                  "Wartość (na 100 tys. osób): %{y}" +
                  "<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)
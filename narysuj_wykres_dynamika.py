import pandas as pd
import streamlit as st
import plotly.express as px



def wykres_dynamika(filtered_df):
    fig = px.line(
        data_frame = filtered_df,
        x = "Rok",
        y = "Wartosc",
        color = "Przyczyny.zgonów",
        markers = True,
        range_y=[0,filtered_df["Wartosc"].max() *1.1],
        labels={
        "Przyczyny.zgonów": "Choroba",
        "Wartość": "Wskaźnik zgonów",
        "Rok": "Rok badania"}   
    )
    fig.update_layout(
        title="Wskaźnik zgonów (na 100 tys. mieszkańców)",
        xaxis_title="Rok",
        yaxis_title="Wskaźnik śmiertelności (na 100 tys. osób)",
        # Na osi X ma byc co roku tick
        xaxis=dict(tickmode='linear', dtick=1), 
        
        #legenda na dole
        legend=dict(
            title=None,              # Usuwamy zbędny napis "Przyczyny.zgonów" nad legendą
            orientation="h",         # Ustawiamy legendę poziomo 
            yanchor="top", y=-0.2,   # Wypychamy ją pod oś X
            xanchor="center", x=0.5  # Centrujemy idealnie na środku
        ),
        
        # dymek po najechaniu
        hovermode="x unified", 
        
        font=dict(size=14)
    )    
    
    st.plotly_chart(fig, use_container_width=True)
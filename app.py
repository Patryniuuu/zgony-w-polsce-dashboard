import pandas as pd
import streamlit as st
import plotly.express as px
import narysuj_wykres_dynamika
import narysuj_wykres_mapa
import narysuj_wykres_przyczyny
import narysuj_wykres_woj_plec
import narysuj_wykres_woj_mw

st.set_page_config(page_title="Na co umierają Polacy - dashboard", layout="wide")
import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
    <style>
        /* Celujemy w główny kontener treści */
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem !important; /* Zmniejsza odstęp od sidebar */
            padding-right: 1rem !important; /* Zmniejsza odstęp od prawej krawędzi */
            max-width: 98% !important;     /* Pozwala treści rozciągnąć się bardziej na boki */
        }
        /* 2. Celujemy bezpośrednio w listę stron (nawigację) */
        [data-testid="stSidebarNav"] {
            padding-top: 0rem !important;
            margin-top: -2rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
st.title('Na co umierają Polacy?')
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df = df.drop(columns=['Unnamed: 0', "Jednostka.miary", "Atrybut", "X"])
    stara_nazwa = "objawy, cechy chorobowe i nieprawidłowe wyniki badań klinicznych i laboratoryjnych"
    nowa_nazwa = "przyczyny niedokładnie określone"
    df['Przyczyny.zgonów'] = df['Przyczyny.zgonów'].replace(stara_nazwa, nowa_nazwa)
    df['Nazwa']=df['Nazwa'].str.lower()
    return df

dane = load_data(r"dane/dane_bdl_zgony_2010_2024.csv")

def strona_glowna():
    st.subheader('Strona główna')
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec lectus est, eleifend et interdum et, commodo at tortor. Integer eleifend lorem ac rhoncus luctus. Aliquam ac mattis ligula. Morbi fermentum arcu pharetra nibh placerat, nec aliquet est varius. Proin in accumsan tellus. Donec id justo sed nibh ullamcorper pharetra. Nunc ultricies neque ac ex porta, vitae sollicitudin massa sodales. Sed a imperdiet est. Etiam porta odio nec vulputate volutpat. Vivamus pulvinar enim ut diam sagittis ornare. Vivamus posuere nisi nunc, vitae interdum lectus efficitur eget. Etiam at facilisis libero, in scelerisque nulla. Vestibulum consequat erat nec nibh mollis mollis. Curabitur at ullamcorper nibh. Donec rutrum fermentum velit, eu pretium lectus ullamcorper eu. Integer egestas ullamcorper imperdiet. Suspendisse egestas, est eu tempor tempus, ante lacus volutpat ante, vel condimentum erat metus rhoncus sem. Vivamus egestas imperdiet ipsum, ac dapibus mauris bibendum facilisis. Etiam non congue risus, id molestie ipsum. In hac habitasse platea dictumst. Vestibulum interdum, mi molestie dictum rutrum, justo ante egestas libero, sed consequat erat ipsum vel ante. Donec risus arcu, euismod aliquam tristique in, elementum a velit. Aenean facilisis, justo vel efficitur cursus, sem mauris pretium turpis, non dictum augue mi ut diam. Quisque feugiat eget massa at semper. Aliquam erat volutpat. Pellentesque quam ipsum, placerat a quam vel, venenatis luctus enim. Pellentesque at arcu in mauris eleifend condimentum in vitae purus. Curabitur bibendum maximus elit, mattis dignissim nulla rutrum eget. Suspendisse varius condimentum elit eget laoreet.")

def strona_dynamika():
    st.subheader('Dynamika chorób w Polsce')
    st.sidebar.write('Filtry do dynamiki chorób')
    #Odfiltrujemy chorobe ogolem
    df = dane[dane["Przyczyny.zgonów"]!="ogółem"]
    
    lata = st.sidebar.slider("Wybierz lata", 2010, 2024, (2010, 2024))
    choroby = st.sidebar.multiselect("wybierz choroby", df["Przyczyny.zgonów"].unique(), default=df["Przyczyny.zgonów"].unique()[0])
    plec = st.sidebar.selectbox("Wybierz płeć", df["Płeć"].unique())
    wojewodztwo = st.sidebar.selectbox("Wybierz rozważany obszar", df["Nazwa"].unique())
    obszar = st.sidebar.selectbox("Wybierz rozważany obszar", df["Miasta...wieś"].unique())
    df_filtered = df[(df['Rok'] >= lata[0]) & 
                       (df['Rok'] <= lata[1]) & 
                       (df['Przyczyny.zgonów'].isin(choroby)) & 
                       (df['Płeć'] == plec) &
                       (df['Nazwa'] == wojewodztwo) &
                       (df["Miasta...wieś"] == obszar)]
    df_filtered = df_filtered.sort_values(by="Rok", ascending = True)
    narysuj_wykres_dynamika.wykres_dynamika(df_filtered)


def strona_wykresy():
    st.subheader('Porównanie przyczyn zgonów ze względu na płeć lub miejsce zamieszkania')
    st.sidebar.write('Filtry dla porównań')
    dane_filtered = dane[dane["Przyczyny.zgonów"]!="ogółem"]
    
    rok = st.sidebar.selectbox("Wybierz rok", sorted(dane['Rok'].unique(), reverse=True))
    
    # Sprawdzamy, czy w pamięci Streamlita NIE MA jeszcze naszych chorób
    if "zapisane_choroby" not in st.session_state:
        # Skoro nie ma, to znaczy, że użytkownik dopiero wszedł na stronę.
        # Liczymy domyślne Top 10 dla aktualnie wybranego roku
        dane_dla_roku = dane_filtered[dane_filtered['Rok'] == rok]
        top10_startowe = (
            dane_dla_roku.groupby("Przyczyny.zgonów")["Wartosc"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .index.tolist()
        )
        # Zapisujemy ten startowy zestaw do pamięci
        st.session_state["zapisane_choroby"] = top10_startowe
    
    choroby = st.sidebar.multiselect(
        "Wybierz choroby", 
        options=dane_filtered["Przyczyny.zgonów"].unique(), 
        key="zapisane_choroby" 
    )
    wybor = st.sidebar.radio("Wybierz porównanie", ["Płeć", "Obszar"])
    if wybor == "Obszar":
        wybor = "Miasta...wieś"
    df_filtered = dane_filtered[(dane_filtered['Rok'] == rok) & 
                       (dane_filtered['Przyczyny.zgonów'].isin(choroby))&
                       (dane_filtered[wybor] != "ogółem")]
    narysuj_wykres_przyczyny.wykres_slupki(df_filtered, wybor)
    
    
def strona_mapa():
    
    st.sidebar.write('Filtry dla mapy')
    rok = st.sidebar.selectbox("Wybierz rok", sorted(dane['Rok'].unique(), reverse=True))
    choroba = st.sidebar.selectbox('Wybierz chorobę', dane["Przyczyny.zgonów"].unique())
    df_filtered = dane[(dane["Rok"]==rok) & (dane["Przyczyny.zgonów"]==choroba)]
    col1, col2 = st.columns(2)
    with col1:
        #st.header('Mapa Polski')
        st.subheader(f"Mapa zgonów spowodowanych przez {df_filtered["Przyczyny.zgonów"].unique()[0]} w roku {df_filtered["Rok"].unique()[0]}")
        woj=narysuj_wykres_mapa.wykres_mapa(df_filtered)
    with col2:
        st.subheader('Rozkłady ze względu na płeć i miejsce zamieszkania')
        col21, col22 = st.columns(2)
        with col21:
            #st.subheader('Płeć')
            narysuj_wykres_woj_plec.wykres_woj_plec(df_filtered, woj)
        with col22:
            #st.subheader('Miejsce zamieszkania')
            narysuj_wykres_woj_mw.wykres_woj_mw(df_filtered, woj)
        if woj==0:
            st.write(f"Wybrane województwo: brak, wybrany rok: {rok}")
        else:
            st.write(f"Wybrane województwo: {woj}, wybrany rok: {rok}")


pg = st.navigation([
    st.Page(strona_glowna, title="Strona główna", icon='🏠'),
    st.Page(strona_dynamika, title="Dynamika chorób", icon="📈"),
    st.Page(strona_mapa, title="Przestrzenna analiza dancyh chorobowych", icon="🗺️"),
    st.Page(strona_wykresy, title="Porównanie przyczyn zgonów", icon="📊")
])

pg.run()
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
    df.loc[df['Nazwa'] == 'polska', 'Nazwa'] = 'Polska'
    return df

dane = load_data(r"dane/dane_bdl_zgony_2010_2024.csv")

def strona_glowna():
    st.header('Strona główna')
    st.subheader('🏠 O projekcie')
    
    st.markdown("""
    Witaj w interaktywnym dashboardzie analitycznym poświęconym analizie struktury i dynamiki umieralności w Polsce. 
    Projekt został stworzony w celach edukacyjnych, aby w przystępny i wizualny sposób zobrazować, jakie schorzenia i czynniki 
    mają największy wpływ na śmiertelność Polaków na przestrzeni ostatnich kilkunastu lat.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📅 **Zakres czasowy:**\n\nLata 2010 – 2024")
    with col2:
        st.info("🧬 **Przekroje analizy:**\n\nPłeć, Województwo, Miasto/Wieś")
    with col3:
        st.info("📉 **Jednostka miary:**\n\nWskaźnik na 100 tys. ludności")

    st.markdown("---")
    
    st.subheader('🗺️ Struktura i nawigacja aplikacji')
    st.markdown("""
    Aplikacja została zaprojektowana w sposób modułowy i pozwala na analizę danych z różnych perspektyw:  
    **📈 Dynamika chorób:**  
                Moduł dedykowany analizie trendów czasowych. Pozwala prześledzić, jak zmieniała się śmiertelność na wybrane choroby na przestrzeni lat, a także porównać strukturę zgonów (według płci lub miejsca zamieszkania) dla konkretnego, wskazanego roku.  
    **🗺️ Przestrzenna analiza danych:**  
                Interaktywna mapa Polski w podziale na województwa. Pozwala zidentyfikować regiony o najwyższym i najniższym nasileniu zgonów z powodu konkretnej choroby, uzupełniona o lokalne wykresy rozkładów demograficznych.
    """)

    st.markdown("---")

    st.subheader('🗃️ Źródło danych')
    st.caption("""
    Dane wykorzystane w projekcie pochodzą z *Banku Danych Lokalnych Głównego Urzędu Statystycznego (GUS)*. 
    Zbiór danych obejmuje oficjalne statystyki medyczne dotyczące zarejestrowanych przyczyn zgonów w Polsce. 
    Wskaźniki zostały ustandaryzowane na 100 tysięcy mieszkańców, co pozwala na obiektywne porównywanie 
    regionów o różnej liczbie ludności oraz grup o różnej liczebności.
    🔗 **[Przejdź do źródła danych w BDL](https://bdl.stat.gov.pl/bdl/metadane/metryka/3977#)**
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: right; color: gray; font-style: italic;">
        Projekt został zrealizowany w ramach przedmiotu Wstęp do Eksploracji Danych.<br>
        <b>Autorzy:</b> Patryk Kubik, Bartosz Obłoj, Patrycja Olszańska
    </div>
    """, unsafe_allow_html=True)
def strona_dynamika():
    
    st.info("""
    💡 **Jak korzystać z tej zakładki:**
    * **Wykres górny (Dynamika):** Domyślnie pokazuje trend czasowy dla pierwszej choroby z listy, uwzględniając ogólne statystyki dla całej Polski. W panelu bocznym możesz dodać kolejne choroby do porównania, zawęzić zakres lat oraz przefiltrować dane dla konkretnego województwa, płci lub miejsca zamieszkania.
    * **Wykres dolny (Struktura):** Pojawia się automatycznie po wybraniu chorób. Pozwala sprawdzić szczegółowy podział (na płeć lub obszar) w konkretnym roku. Możesz zmieniać badany rok za pomocą selektora pod wykresem dynamiki.
    """)
    st.markdown("💡 **[Kliknij tutaj, aby zjechać w dół do komentarza odnośnie domyślnie wybranego zestawienia chorób 👇](#komentarz)**")
    st.markdown("---")
    
    st.sidebar.write('Filtry do dynamiki chorób')
    #Odfiltrujemy chorobe ogolem
    df = dane[dane["Przyczyny.zgonów"]!="ogółem"]
    
    lata = st.sidebar.slider("Wybierz lata", 2010, 2024, (2010, 2024))
    top5_chorob = (
        df.groupby("Przyczyny.zgonów")["Wartosc"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .index.tolist()
    )
    
    # Przekazujemy top5_chorob jako domyślnie zaznaczone (default)
    choroby = st.sidebar.multiselect(
        "Wybierz choroby", 
        options=df["Przyczyny.zgonów"].unique(), 
        default=top5_chorob,
        max_selections=5
    )
    plec = st.sidebar.selectbox("Wybierz płeć", df["Płeć"].unique())
    wojewodztwo = st.sidebar.selectbox("Wybierz rozważany obszar (Polska/województwo)", df["Nazwa"].unique())
    obszar = st.sidebar.selectbox("Wybierz rozważany obszar zamieszkania", df["Miasta...wieś"].unique())
    df_filtered = df[(df['Rok'] >= lata[0]) & 
                       (df['Rok'] <= lata[1]) & 
                       (df['Przyczyny.zgonów'].isin(choroby)) & 
                       (df['Płeć'] == plec) &
                       (df['Nazwa'] == wojewodztwo) &   
                       (df["Miasta...wieś"] == obszar)]
    df_filtered = df_filtered.sort_values(by="Rok", ascending = True)
    narysuj_wykres_dynamika.wykres_dynamika(df_filtered, wojewodztwo, plec, obszar)
    
    
    
    st.markdown("---")
    
    st.subheader(f"Szczegółowa struktura dla wybranego roku ({wojewodztwo})")
    
    lata_dostepne = list(range(lata[0], lata[1] + 1))
    wybrany_rok = st.selectbox("Wybierz rok do analizy struktury (podział na płeć/obszar):", lata_dostepne)
    
    
    df_slupki = df[(df['Rok'] == wybrany_rok) & 
                   (df['Przyczyny.zgonów'].isin(choroby)) & 
                   (df['Nazwa'] == wojewodztwo)]
    
    wybor_struktury = st.radio("Porównaj według:", ["Płeć", "Obszar zamieszkania"], horizontal=True)
    if wybor_struktury == "Obszar zamieszkania":
        wybor_struktury = "Miasta...wieś"

    df_slupki = df_slupki[df_slupki[wybor_struktury] != "ogółem"]
    
    if len(choroby) > 0:
        narysuj_wykres_przyczyny.wykres_slupki(df_slupki, wybor_struktury)
    else:
        st.warning("Wybierz przynajmniej jedną chorobę w panelu bocznym.")
    
    st.markdown("<div id='komentarz'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📝 Komentarz: Krajobraz epidemiologiczny Polski")
    
    st.markdown("""
    Prezentowany domyślnie zestaw pięciu najczęstszych przyczyn zgonów w Polsce w latach 2010 – 2024 pozwala na wyciągnięcie kluczowych wniosków:

    * **Bezwzględna dominacja układu krążenia:** Wykres wyraźnie pokazuje, że **choroby układu krążenia** (jasnoniebieska linia) drastycznie odskakują od pozostałych przyczyn, utrzymując się na poziomie między 400 a 500 zgonów na 100 tys. mieszkańców. To niezmiennie główny czynnik umieralności w polskim społeczeństwie.
    
    * **Stabilny i wysoki trend onkologiczny:** Linie reprezentujące **nowotwory** (zielona) oraz **nowotwory złośliwe** (różowa) biegną niemal równolegle w okolicach 250 zgonów na 100 tys. osób. W przeciwieństwie do układu krążenia, nowotwory wykazują stały, lekki trend wzrostowy na przestrzeni całego badanego okresu, co obrazuje starzenie się społeczeństwa.
    
    * **Wpływ pandemii i umieralność nadmiarowa (2020 – 2022):** 
        * Na wykresie doskonale widać załamanie trendów w okresie COVID-19. Dla chorób układu krążenia pik przypada na **2021 rok** (blisko 480 zgonów). 
        * Zwróć uwagę na ciemnoniebieską linię (**choroba niedokrwienna serca**) – tam również najwyższy punkt przypada na 2021 rok (około 200 zgonów).
        * Czerwona linia (**przyczyny niedokładnie określone**) dynamicznie rosła już od 2016 roku, osiągając swój szczyt w pandemicznym roku 2020 (ok. 130 zgonów), co może świadczyć o trudnościach diagnostycznych w początkowej fazie paraliżu służby zdrowia.
    
    * **Powrót do bazy po 2022 roku:** W latach 2023 – 2024 widoczne jest wyraźne opadanie linii układu krążenia oraz choroby niedokrwiennej serca. Statystyki powracają do wieloletnich trendów sprzed pandemii, co oznacza wygasanie fali zgonów nadmiarowych.
    """)
# SEKCJA Z SŁUPAKMI POKI CO USUWAMY JĄ
# def strona_wykresy():
#     st.subheader('Porównanie przyczyn zgonów ze względu na płeć lub miejsce zamieszkania')
#     st.sidebar.write('Filtry dla porównań')
#     dane_filtered = dane[dane["Przyczyny.zgonów"]!="ogółem"]
    
#     rok = st.sidebar.selectbox("Wybierz rok", sorted(dane['Rok'].unique(), reverse=True))
    
#     # Sprawdzamy, czy w pamięci Streamlita NIE MA jeszcze naszych chorób
#     if "zapisane_choroby" not in st.session_state:
#         # Skoro nie ma, to znaczy, że użytkownik dopiero wszedł na stronę.
#         # Liczymy domyślne Top 10 dla aktualnie wybranego roku
#         dane_dla_roku = dane_filtered[dane_filtered['Rok'] == rok]
#         top10_startowe = (
#             dane_dla_roku.groupby("Przyczyny.zgonów")["Wartosc"]
#             .mean()
#             .sort_values(ascending=False)
#             .head(10)
#             .index.tolist()
#         )
#         # Zapisujemy ten startowy zestaw do pamięci
#         st.session_state["zapisane_choroby"] = top10_startowe
    
#     choroby = st.sidebar.multiselect(
#         "Wybierz choroby", 
#         options=dane_filtered["Przyczyny.zgonów"].unique(), 
#         key="zapisane_choroby" 
#     )
#     wybor = st.sidebar.radio("Wybierz porównanie", ["Płeć", "Obszar"])
#     if wybor == "Obszar":
#         wybor = "Miasta...wieś"
#     df_filtered = dane_filtered[(dane_filtered['Rok'] == rok) & 
#                        (dane_filtered['Przyczyny.zgonów'].isin(choroby))&
#                        (dane_filtered[wybor] != "ogółem")]
#     narysuj_wykres_przyczyny.wykres_slupki(df_filtered, wybor)
    
    
def strona_mapa():
    
    st.sidebar.write('Filtry dla mapy')
    rok = st.sidebar.selectbox("Wybierz rok", sorted(dane['Rok'].unique(), reverse=True))
    choroba = st.sidebar.selectbox('Wybierz przyczynę', dane["Przyczyny.zgonów"].unique())
    df_filtered = dane[(dane["Rok"]==rok) & (dane["Przyczyny.zgonów"]==choroba)]
    st.info("""
    💡 **Jak korzystać z tej zakładki:**

    * **Panel boczny (Filtry dla strony):**
    Z rozwijanych list po lewej stronie wybierz interesujący Cię **rok** oraz **chorobę** (przyczynę zgonów). Zmiana tych parametrów automatycznie zaktualizuje całą stronę – zarówno mapę, jak i wykresy po prawej stronie.

    * **Lewa strona (Analiza przestrzenna):**
    Mapa Polski przedstawia natężenie wybranego zjawiska w poszczególnych województwach. Im ciemniejszy kolor, tym wyższy wskaźnik (liczba zgonów na 100 tys. osób). **Najedź kursorem** na dowolne województwo, aby zobaczyć jego nazwę i dokładną wartość. **Kliknij na region**, aby przefiltrować wykresy słupkowe wyłącznie do danych z tego województwa (kliknij ponownie, by wrócić do widoku całej Polski).
    
    * **Prawa strona (Rozkłady demograficzne):**
    Wykresy szczegółowo rozbijają wybrane statystyki ze względu na **płeć** (lewy wykres) oraz **miejsce zamieszkania** (prawy wykres).
    """)
    st.markdown("💡 **[Kliknij tutaj, aby zjechać w dół do najciekawszych przypadków w danych 👇](#ciekawostki2)**")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        #st.header('Mapa Polski')
        st.subheader(f"Mapa zgonów spowodowanych przez {df_filtered['Przyczyny.zgonów'].unique()[0]} w roku {df_filtered['Rok'].unique()[0]}")
        st.subheader('')
        woj=narysuj_wykres_mapa.wykres_mapa(df_filtered)
    with col2:
        if woj==0:
            st.subheader(f'Rozkłady ze względu na płeć i miejsce zamieszkania')
            st.subheader(f'(Polska | {choroba} | {rok})')
        else:
            st.subheader(f'Rozkłady ze względu na płeć i miejsce zamieszkania ')
            st.subheader(f'({woj} | {choroba} | {rok})')
        col21, col22 = st.columns(2)
        with col21:
            #st.subheader('Płeć')
            narysuj_wykres_woj_plec.wykres_woj_plec(df_filtered, woj)
        with col22:
            #st.subheader('Miejsce zamieszkania')
            narysuj_wykres_woj_mw.wykres_woj_mw(df_filtered, woj)
    st.markdown("<div id='ciekawostki2'></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📝 Ciekawe przypadki, które można zaobserwować")
    st.markdown("""
    Pobaw się filtrami w panelu bocznym i sprawdź, czy uda Ci się zaobserwować te znane zjawiska demograficzne i epidemiologiczne:

    * 📉 **„Ciemna plama” na mapie (Fenomen województwa łódzkiego):** Nawet w statystykach dla przyczyny **„ogółem”**, województwo łódzkie od lat wyróżnia się najciemniejszym kolorem. Wynika to z historycznych i ekonomicznych uwarunkowań regionu, który mierzy się z najszybciej starzejącym się społeczeństwem i najkrótszą przewidywaną długością życia w Polsce.
    
    * ⚠️ **Tragiczne skutki wypadków i samobójstw:** Wybierz **„wypadki komunikacyjne”**, **"samobójstwa"** lub **"zewnętrzne przyczyny zgonu"**. Lewy wykres słupkowy pokaże drastyczną, kilkukrotną przewagę mężczyzn. To smutne zjawisko ogólnoświatowe, wynikające z częstszego podejmowania ryzykownych zachowań, pracy w niebezpiecznych zawodach oraz rzadszego szukania pomocy psychologicznej.

    * 🧠 **Paradoks długowieczności (Alzheimer i nadciśnienie):** Zmień przyczynę na **„chorobę Alzheimera”** lub **„chorobę nadciśnieniową"**. Tym razem sytuacja się odwraca i to słupek kobiet jest znacznie wyższy. Nie oznacza to jednak, że są one biologicznie słabsze – kobiety w Polsce żyją średnio o około 8 lat dłużej od mężczyzn, dlatego znacznie częściej dożywają sędziwego wieku, w którym te konkretne schorzenia zbierają największe żniwo.
            
    * 🏭 **Nowotwory a miejsce zamieszkania:** Wybierz **„nowotwory”**. Spójrz na prawy wykres słupkowy. Bardzo często to mieszkańcy miast charakteryzują się wyższymi wskaźnikami zachorowalności na raka, co bywa wiązane z większym zanieczyszczeniem środowiska w aglomeracjach oraz innym stylem życia, ale też... z lepszą i szybszą diagnostyką w ośrodkach miejskich.
    """)



pg = st.navigation([
    st.Page(strona_glowna, title="Strona główna", icon='🏠'),
    st.Page(strona_dynamika, title="Dynamika chorób", icon="📈"),
    st.Page(strona_mapa, title="Przestrzenna analiza danych chorobowych", icon="🗺️")
])

pg.run()
# 📊 Analiza przyczyn zgonów w Polsce (2010-2024)

Interaktywny dashboard stworzony w Pythonie z wykorzystaniem biblioteki **Streamlit**, służący do wizualizacji i analizy danych demograficznych dotyczących przyczyn zgonów w Polsce. Dane pochodzą z Banku Danych Lokalnych GUS.

## 🚀 Link do aplikacji
[👉 KLIKNIJ TUTAJ, ABY OTWORZYĆ DASHBOARD](https://zgony-w-polsce-dashboard-pk-bo.streamlit.app/)

---

## 🛠️ Funkcjonalności
Aplikacja podzielona jest na trzy główne moduły:
* **Dynamika chorób:** Analiza trendów czasowych dla wybranych jednostek chorobowych z możliwością filtrowania po płci, województwie i obszarze (miasto/wieś).
* **Porównanie przyczyn:** Interaktywny wykres słupkowy (Top 10) pozwalający zestawić wpływ konkretnych chorób na różne grupy społeczne.
* **Analiza przestrzenna (Mapa):** Wizualizacja natężenia zgonów w podziale na województwa (geowizualizacja).

## 🧰 Technologie
* **Python** (3.x)
* **Streamlit** (Frontend aplikacji)
* **Plotly Express** (Interaktywne wykresy)
* **Pandas** (Przetwarzanie danych)
* **Geopandas** (Obsługa danych przestrzennych i map)

## 📁 Struktura plików
* `app.py` - Główny plik sterujący nawigacją aplikacji.
* `narysuj_wykres_... .py` - Moduły zawierające logikę generowania konkretnych wizualizacji.
* `dane/` - Katalog zawierający pliki źródłowe CSV oraz pliki wektorowe (Shapefiles) dla map.
* `requirements.txt` - Lista bibliotek niezbędnych do uruchomienia projektu na serwerze.

## 👥 Autorzy
* [Patryk Kubik](https://github.com/Patryyniuuu)
* [Bartosz Obłoj](https://github.com/oblojb)


import streamlit as st
from login import login_screen
from database_portal import database_portal
from analysis import analysis_page
from database_diagram import database_diagram_page  # Přidání stránky s diagramem
from lottie_animation import show_animation

# Hlavní logika aplikace
def main():
    # Zkontroluj, jestli je session_state pro animaci nastaveno
    if 'animation_shown' not in st.session_state:
        st.session_state['animation_shown'] = False

    # Zobraz animaci jen při prvním načtení
    if not st.session_state['animation_shown']:
        show_animation()
        st.session_state['animation_shown'] = True

    # Zobrazit pouze login obrazovku, dokud uživatel není přihlášen
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        login_screen()  # Zobrazit přihlašovací stránku
    else:
        # Po přihlášení zobrazit sidebar a další stránky
        with st.sidebar:
             page = st.sidebar.selectbox("Vyberte stránku", ["Databázový portál", "Analýza Dat", "Databázový diagram"])

        # Navigace mezi stránkami po přihlášení
        if page == "Databázový portál":
            database_portal()  # Načítáme portál z database_portal.py
        elif page == "Analýza Dat":
            analysis_page()  # Načítáme analýzu dat z analysis.py
        elif page == "Databázový diagram":
            database_diagram_page()  # Načítáme stránku s databázovým diagramem

if __name__ == "__main__":
    main()

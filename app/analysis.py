import streamlit as st
import pandas as pd
from sqlalchemy import text

# Funkce pro načtení tabulek z dané databáze a schématu
def load_tables(engine, schema):
    query = f"""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE'
    """
    return pd.read_sql(query, engine)

# Funkce pro spuštění SQL dotazu
def run_query(engine, query):
    try:
        # Používáme SQLAlchemy text() pro bezpečné provedení dotazu
        result = pd.read_sql(text(query), engine)
        return result
    except Exception as e:
        st.error(f"Chyba při provádění dotazu: {e}")
        return None

# Funkce pro analýzu dat
def analysis_page():
    st.title("Analýza Dat")

    # Načtení připojení k databázi z session state
    engine = st.session_state.get('engine')

    if not engine:
        st.error("Není dostupné připojení k databázi.")
        return

    # Vybrané hodnoty pro databázi a schéma (zůstávají otevřené a lze je kdykoliv měnit)
    selected_database = st.selectbox("Vyberte databázi", ["master", "Eshop", "DalšíDatabáze"])  # Zde může být dynamické načítání
    selected_schema = st.selectbox("Vyberte schéma", ["dbo", "Production", "Sales"])  # Dynamické načítání schémat

    # Načtení a zobrazení tabulek po výběru databáze a schématu
    st.write(f"Aktuální databáze: `{selected_database}`")
    st.write(f"Aktuální schéma: `{selected_schema}`")

    if st.button("Načíst tabulky"):
        try:
            tables = load_tables(engine, selected_schema)
            st.write("Dostupné tabulky ve schématu:")
            st.dataframe(tables)
        except Exception as e:
            st.error(f"Chyba při načítání tabulek: {e}")

    # Vstupní pole pro SQL dotaz
    st.write("Zadejte SQL dotaz níže:")
    query = st.text_area("SQL dotaz", height=200)

    if st.button("Spustit dotaz"):
        if query.strip() == "":
            st.error("SQL dotaz nemůže být prázdný.")
        else:
            # Spuštění dotazu a zobrazení výsledků
            data = run_query(engine, query)
            if data is not None:
                st.write("Výsledky dotazu:")
                st.dataframe(data)

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components  # pro zobrazení HTML

# Funkce pro vytvoření SQLAlchemy připojení
def get_sqlalchemy_engine(server, username, password):
    connection_string = f"mssql+pyodbc://{username}:{password}@{server}/master?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(connection_string)
    return engine

# Načtení dostupných databází
def load_databases(engine):
    query = "SELECT name FROM sys.databases"
    databases = pd.read_sql(query, engine)
    return databases['name'].tolist()

# Načtení schémat z vybrané databáze
def load_schemas(engine, database):
    query = f"SELECT DISTINCT TABLE_SCHEMA FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
    schemas = pd.read_sql(query, engine)
    return schemas['TABLE_SCHEMA'].tolist()

# Načtení tabulek z vybraného schématu
def load_tables(engine, database, schema):
    query = f"SELECT TABLE_NAME FROM {database}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE'"
    tables = pd.read_sql(query, engine)
    return tables['TABLE_NAME'].tolist()

# Načtení dat z vybrané tabulky
def load_table_data(engine, database, schema, table_name):
    query = f"SELECT * FROM {database}.{schema}.{table_name} WHERE 1=1"
    df = pd.read_sql(query, engine)
    return df

# Analýza tabulky pomocí ydata_profiling a zobrazení výsledků
def analyze_with_profiling(df):
    profile = ProfileReport(df, title="Profiling Report")
    profile_html = profile.to_html()  # Vygeneruj HTML
    components.html(profile_html, height=1000, width=1200, scrolling=True)  # Zobraz HTML ve Streamlit s větší šířkou

# Hlavní portál
def database_portal():
    engine = st.session_state.get('engine')
    
    if engine:
        st.title("Profilace Tabulek")
        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            databases = load_databases(engine)
            if databases:
                database = st.selectbox("🗄 Vyber Databázi", databases)
            else:
                st.error("Nebyly nalezeny žádné databáze.")
                return

        if database:
            with col2:
                schemas = load_schemas(engine, database)
                if schemas:
                    schema = st.selectbox("📂 Vyber Schéma", schemas)
                else:
                    st.error("Nebyla nalezena žádná schémata pro vybranou databázi.")
                    return

            if schema:
                with col3:
                    tables = load_tables(engine, database, schema)
                    if tables:
                        table = st.selectbox("📑 Vyber Tabulku", tables)
                    else:
                        st.error("Nebyly nalezeny žádné tabulky pro vybrané schéma.")
                        return

                if table:
                    st.markdown(f"#### 🗃 Načítání dat z tabulky: `{schema}.{table}`")
                    df = load_table_data(engine, database, schema, table)
                    st.dataframe(df.head(10))

                    # Přidání tlačítka pro spuštění analýzy pomocí ydata_profiling
                    if st.button("Analyzovat"):
                        analyze_with_profiling(df)

# Přihlašovací formulář
def login_screen():
    st.title("Přihlášení k databázi")
    server = st.text_input("Server:")
    username = st.text_input("Uživatelské jméno:")
    password = st.text_input("Heslo:", type="password")
    if st.button("Přihlásit se"):
        engine = get_sqlalchemy_engine(server, username, password)
        if engine:
            st.session_state['engine'] = engine
            st.session_state['logged_in'] = True
            st.success("Úspěšně připojeno k databázi!")

# Hlavní aplikace
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    database_portal()
else:
    login_screen()

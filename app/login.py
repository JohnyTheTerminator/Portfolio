import streamlit as st
import time
from sqlalchemy import create_engine, text

# Funkce pro připojení k databázi pomocí SQLAlchemy
def connect_to_db(server, username, password):
    try:
        connection_string = f'mssql+pyodbc://{username}:{password}@{server}/master?driver=ODBC+Driver+17+for+SQL+Server'
        engine = create_engine(connection_string)
        # Otestování připojení pomocí SQLAlchemy textového dotazu
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        st.error(f"Chyba při připojení k serveru: {e}")
        return None

# Přihlašovací obrazovka
def login_screen():
    st.title("Data Analyzer")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("login_form"):
        server_name = st.text_input("Server Name *", placeholder="Enter your Server Name")
        username = st.text_input("Username *", placeholder="Enter your Username")
        password = st.text_input("Password *", type="password", placeholder="Enter your Password")
        remember_me = st.checkbox("Remember me")
        submit_button = st.form_submit_button(label="Přihlásit se", help="Click to login")

    if submit_button:
        loading_text = st.empty()

        # Simulace "Připojuji se..." s animací teček
        for i in range(3):
            loading_text.text(f"Připojuji se{'.' * (i % 3 + 1)}")
            time.sleep(1)

        # Ověření přihlašovacích údajů a připojení
        engine = connect_to_db(server_name, username, password)
        if engine:
            st.session_state['engine'] = engine
            st.session_state['logged_in'] = True
            st.success("Úspěšně přihlášeno!")
        else:
            loading_text.empty()

import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# Funkce pro načítání Lottie animací z URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Načítání Lottie animace
lottie_hello = load_lottieurl("https://lottie.host/408934d2-05a4-4c4c-80c0-a9086bcf6a6f/kOGpnUWO0u.json")

# Zobrazení Lottie animace
def show_animation():
    lottie_container = st.empty()
    with lottie_container:
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low",
            height=None,
            width=None,
            key=None,
        )
    time.sleep(3)
    lottie_container.empty()
import streamlit as st

from streamlit_navigation_bar import st_navbar

import pages as pg
 

st.set_page_config(initial_sidebar_state="collapsed")

styles = {
    "nav": {
        "background-color": "rgb(41, 86, 172)",
        "justify-content": "right",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(49, 51, 63)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}
options = {
    "show_menu": True,
    "show_sidebar": True,
}


bars = ["Home", "Pricing", "Contact", "Chatbots"]
page = st_navbar(bars, styles = styles, options = options)
# --- SHARED ON ALL PAGES ---
st.logo("assets/logo2.png")
if page == "Home":
    pg.home()
elif page == "Pricing":
    pg.pricing()
elif page == "Contact":
    pg.contact()
elif page == "Chatbots":
    pg.chatbot()
    


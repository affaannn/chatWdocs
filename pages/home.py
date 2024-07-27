import streamlit as st
import json
import requests  # pip install requests
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

# GitHub: https://github.com/andfanilo/streamlit-lottie
# Lottie Files: https://lottiefiles.com/




def home():
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)


    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    c1, c2, c3 = st.columns([1,1,1], vertical_alignment="center")
    lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")
    with c2:
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            #renderer="svg", # canvas
            height=300,
            width=300,
            key=None,

        )
    a1, a2, a3 = st.columns([1,5,1], vertical_alignment="center")
    with a2:
        #st.title("Your AI for your Documents")
        st.markdown("<h1 style='text-align: center;'>Your AI for your Documents</h1>", unsafe_allow_html=True)
    with a2:
        st.markdown("<h4 style='text-align: center;'>From text to clarity in seconds, AI summaries and answers at your command. Transform your documents effortlessly.</h4>", unsafe_allow_html=True)
    with a2:
        st.markdown("<h6 style='text-align: center;'>Here to help you in: </h6>", unsafe_allow_html=True)
    col0 ,col1, col2, col3 = st.columns([.25,1,1,1], vertical_alignment="center")
    lottie_book = load_lottieurl("https://lottie.host/38e9e241-1104-4602-9c58-61ce98f893ad/18KPDu3L5B.json")
    lottie_fin = load_lottieurl("https://lottie.host/daf6268f-8594-48e5-a68f-8d9ca15696ee/rgAMCQqZxW.json")
    lottie_sch = load_lottieurl("https://lottie.host/f2362e2e-1639-4359-aff1-ed3e937641a2/948yYIbSAa.json")
    with col1:
        st_lottie(
            lottie_book,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            #renderer="svg", # canvas
            height=250,
            width=250,
            key=None,

        )    
    with col2:
        st_lottie(
            lottie_fin,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            #renderer="svg", # canvas
            height=250,
            width=250,
            key=None,

        )    
            
    with col3:
        st_lottie(
            lottie_sch,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            #renderer="svg", # canvas
            height=250,
            width=250,
            key=None,

        )   
    #lottie_coding = load_lottiefile("lottiefile.json")  # replace link to local lottie file
    

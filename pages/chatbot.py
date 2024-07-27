import streamlit as st
from chatbots.agent import agent
from chatbots.finsage import finsage
from chatbots.careersage import careersage
from chatbots.scholarsage import scholarsage
from streamlit_option_menu import option_menu

def chatbot():
    
    styles = {
        "container": {"background-color": "rgb(41, 86, 160)", "border-radius": "10px"},
        "icon": {"color": "black"},
        "nav-link": {"color": "black", "backgroung-color": "rgb(41, 86, 172)", "--hover-color": "rgb(41, 86, 172)", "border-radius": "5px"},
        "nav-link-selected": {"color": "black", "backgroung-color": "rgb(41, 86, 10)", "border-radius": "5px"},
        "active": {"background-color": "rgba(255, 255, 255, 0.25)"},
        "position": "fixed",
    }
 
    menu_dict = {
        "Agent" : {"fn": agent},
        "FinSage" : {"fn": finsage},
        "CareerSage" : {"fn": careersage},
        "ScholarSage" : {"fn": scholarsage}
    }

    selected = option_menu(None, 
        ["Agent", "FinSage", "CareerSage", "ScholarSage"], 
        icons=["file-earmark-pdf", "bank", "briefcase", "mortarboard"],
        default_index=0,
        styles = styles,
        orientation="horizontal")
    if selected in menu_dict.keys():
        menu_dict[selected]["fn"]()
    

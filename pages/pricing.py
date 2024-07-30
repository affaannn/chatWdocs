import streamlit as st
import pandas as pd
import numpy as np
def pricing():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700&display=swap');
        body, h1, h2, h3, h4, h5, h6, p, div, span, a, input, button {
            font-family: 'Sora', sans-serif;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
    "<h1 style='text-align: center; color: rgb(41, 86, 160);'>Find a perfect plan for your use</h1>", 
    unsafe_allow_html=True)

    

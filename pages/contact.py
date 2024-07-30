import streamlit as st
from contact_form import contact_form
def contact():
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
    
    #@st.experimental_dialog("Contact Me")
    def show_contact_form():
        contact_form()

    st.markdown("<h1 style='text-align: left; color: rgb(41, 86, 160);'>Contact Us</h1>", unsafe_allow_html=True)
    # --- HERO SECTION ---
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        show_contact_form()
        #st.image("./assets/images.png", width=230)

    with col2:
        st.markdown("<h3 style='text-align: left; color: rgb(41, 86, 160);'>We're Here to Assist You</h3>", unsafe_allow_html=True)
        st.write(
            "Thank you for your interest in chatWdocs. Whether you have questions, suggestions, or concerns, we are dedicated to providing the support you need."
            )
        
        st.markdown("<h3 style='text-align: left; color: rgb(41, 86, 160);'>Getting Started with chatWdocs:</h3>", unsafe_allow_html=True)
        st.write("For comprehensive guidance on using chatWdocs, please visit our Tutorials or Blogs.")
    
        st.markdown("<h3 style='text-align: left; color: rgb(41, 86, 160);'>Business Inquiries:</h3>", unsafe_allow_html=True)
        st.write("If you are reaching out about chatWdocs for Business, kindly include a brief overview of your business requirements to help us serve you better")
        st.markdown("<h3 style='text-align: left; color: rgb(41, 86, 160);'>Mailing Address:</h3>", unsafe_allow_html=True)
        st.write("""955 Astralis Tower 
                 Supernova sector 94 
                 Noida Utter pradesh 201307""")
        #if st.button("✉️ Contact Me"):
            

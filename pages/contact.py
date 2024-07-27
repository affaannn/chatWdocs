import streamlit as st
from contact_form import contact_form
def contact():

    
    #@st.experimental_dialog("Contact Me")
    def show_contact_form():
        contact_form()

    st.markdown("<h1 style='text-align: left;'>Contact Us</h1>", unsafe_allow_html=True)
    # --- HERO SECTION ---
    col1, col2 = st.columns(2, gap="medium", vertical_alignment="center")
    
    with col1:
        show_contact_form()
        #st.image("./assets/images.png", width=230)

    with col2:
        st.markdown("**We're Here to Assist You**")
        st.write(
            "Thank you for your interest in chatWdocs. Whether you have questions, suggestions, or concerns, we are dedicated to providing the support you need."
            )
        st.markdown("**Getting Started with chatWdocs:**")
        st.write("For comprehensive guidance on using chatWdocs, please visit our Tutorials or Blogs.")
        st.markdown("**Business Inquiries:**")
        st.write("If you are reaching out about chatWdocs for Business, kindly include a brief overview of your business requirements to help us serve you better")
        st.markdown("**Mailing Address:**")
        st.write("""955 Astralis Tower 
                 Supernova sector 94 
                 Noida Utter pradesh 201307""")
        #if st.button("✉️ Contact Me"):
            

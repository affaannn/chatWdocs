

# bring in deps
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv
load_dotenv()
#GOOGLE_API_KEY = 'AIzaSyBm1C6ay9dMiWZrPOb7YaKFsvaI_EcgGss'

# set up parser
parser = LlamaParse(
    result_type="markdown"  # "markdown" and "text" are available
)

# use SimpleDirectoryReader to parse our file
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(input_files=['C:\\Users\\moham\\OneDrive\\Desktop\\img\\ANB.pdf']).load_data()
print(documents)



    home_page = st.Page(
        "pages/home.py",
        title="Home",
        icon=":material/home:",
        default=True,
    )
    pricing = st.Page(
        "pages/pricing.py",
        title="Pricing",
        icon=":material/paid:"
    )
    contact = st.Page(
        "pages/contact.py",
        title="Contact",
        icon=":material/contact_page:"
    )

    project_1_page = st.Page(
        "chatbot/agent.py",
        title="Agent",
        icon=":material/description:",
    )
    project_2_page = st.Page(
        "chatbot/finsage.py",
        title="FinSage",
        icon=":material/account_balance:",
    )
    project_3_page = st.Page(
        "chatbot/careersage.py",
        title="CareerSage",
        icon=":material/work:",
    )
    project_4_page = st.Page(
        "chatbot/scholarsage.py",
        title="ScholarSage",
        icon=":material/school:",
    )


    # --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
    # pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

    # --- NAVIGATION SETUP [WITH SECTIONS]---
    page = st.navigation(
        {
            " " : [home_page, pricing, contact], 
            "Chatbots" : [project_1_page, project_2_page, project_3_page, project_4_page]
        }
    )
     
    return page

    
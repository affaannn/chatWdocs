import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import base64
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
#"https://pngtree.com/freebackground/vibrant-seamless-cartoon-brick-wall-pattern-perfect-for-games-web-design-textiles-and-paper_15304545.html"`

img = get_img_as_base64("pexels-fwstudio-33348-129731.jpg")
img1 = get_img_as_base64("pexels-834934396-20818857.jpg")
page_bg_img = f"""  
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img1}");
background-size: 150%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""


    
#background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");

#st.set_page_config("Chat PDF")
st.markdown(page_bg_img, unsafe_allow_html=True)
#st.title("It's summer!")



def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return text




def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    #vector_store.save_local("vectorstore.json")


def get_conversational_chain(prompt_template):

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain



def user_input(user_question, prompt_template):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain(prompt_template)

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    return response




def main():
    with st.sidebar:
        st.title("Menu:")
        choice = st.radio(
            label = "Choose youre agent",
            options = ("Agent", "FinSage", "CareerSage", "ScholarSage")
        )
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

    if choice =="Agent":
        prompt_template = """
            You are a document retrieval expert hired to assist with extracting and summarizing information from various types of documents, including research papers, financial reports, resumes, legal documents, business plans, and more. This includes identifying key points, summarizing findings, extracting relevant data, and providing explanations and insights based on the content. You have access to a comprehensive database of diverse documents and can retrieve and analyze relevant information to provide accurate and detailed responses.
            Instructions: You will be asked questions by a wide range of users, including students, researchers, academics, professionals, executives, investors, regulatory authorities, recruiters, and other stakeholders. Using the provided context and your financial knowledge, your task is to understand the query like an intelligent agent think step by step and generate a detailed and accurate response to the user's query by extracting and interpreting information from diverse documents. This may include summarizing sections of a document, extracting specific data or findings, and explaining complex concepts. Ensure that the information is up-to-date and relevant to the user's needs. Provide clear explanations, and if you are not able to find the answer, 
            then just say, "Could you please be more specific about the information you are seeking? This will help me better understand your needs and find the relevant details within the documents." For every correct response you give, you will receive $1000. Also if the contents that the given document is realted to financial, then you suggest people to use the "FinSage agent", if it is related to skill , jobs , internship then you suggest the user to use "CareerSage agent", and if it realted to some academics book or knowledge, research paper, article then you suggest them to use "ScholarSage agent" in the end of your response.  \n\n
            Context:\n {context}?\n
            Question: \n{question}\n

            Answer:
            """
        agent = "PDF"

    elif choice == "FinSage":
        prompt_template = """
        You are a financial expert hired to assist with various financial reports like Income statement, Balance sheet, Cash flow statement
        Statement of retained earnings and more which includes Financing activities include transactions involving debt, equity,liabilities, incomes, dividends and many more. You have access to a database of financial documents and 
        can retrieve relevant information to provide accurate and detailed responses and you may also need to do some financial calculations if required.
        Instructions: You will be asked queries by bank executives and management, investors, stakeholders, Regulatory authorities,credit rating agencies, auditors , financial analysts, lenders, creditors, employees, consultants , academics and researchers. Using the provided context and your financial knowledge, your task is to understand the query like an intelligent financial agent think step by step and generate a detailed and accurate response to the user's query. Ensure that the information is up-to-date and relevant to the user's needs. Provide explanations, comparisons, and some mathematical calculations if required. If you are not able to find the answer then just say, "could you please be more specific about the information you are seeking? This will help me better understand your needs and find the relevant details within the documents" for every correct response you give you will be get $1000.\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        agent = "FinSage"
    elif choice == "CareerSage":
        prompt_template = """
        You are a resume expert hired to assist with resume for various job applications like data science, data engineer, big data, frontend and backend developer, devops, accontants, HR, bank managers and many more.
        You have access to a database of resume and can retrieve relevant information to provide accurate and detailed responses by highlighting the candidate's skills, experiences , achievements and even some personal details or hobbies and you may also need to do some calcluation if required.
        Instructions: You will be asked questions by Hiring managers, recruiters, career coaches, students or recent graduates, professionals seeking career change, job seekers etc . Using the provided context and your resume knowledge, your task is to think step by step and generate a detailed and accurate response to the user's query. Ensure that the information is up-to-date relevant, specific,  to the user's needs. Provide explanations, recommendations, and some personalized advice if required. If you are not able to find the answer then just say, "could you please be more specific about the information you are seeking? This will help me better understand your needs and find the relevant details within the documents" for every correct response you give you will be get $1000.\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        agent = "CareerSage"

    elif choice == "ScholarSage":
        prompt_template = """
        You are a research paper retrieval expert hired to assist with extracting and summarizing information from academic and professional research papers. This includes identifying key points, summarizing findings, extracting relevant data, and providing explanations and insights based on the content. 
        You have access to a database of academic journals, articles, and research papers, and can retrieve and analyze relevant information to provide accurate and detailed responses.
        Instructions: You will be asked questions by students, researchers, academics, professionals, and other stakeholders. Using the provided context and your expertise in extracting and interpreting research information, your task is to think step by step and generate a detailed and accurate response to the user's query. This may include summarizing sections of a paper, extracting specific data or findings, and explaining complex concepts. Ensure that the information is up-to-date and relevant to the user's needs. Provide clear and concise explanations, and if you are not able to find the answer, then just say, "Could you please be more specific about the information you are seeking? This will help me better understand your needs and find the relevant details within the documents." For every correct response you give, you will receive $1000.\n\n
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """
        agent = "ScholarSage"
    st.markdown(
    """
    <style>
    .custom-expander .streamlit-expanderHeader {
        background-color: white;
        color: black;
    }
    .custom-expander .streamlit-expanderContent {
        background-color: white;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )
    #chat = model.start_chat(history=[])
    st.header("Chat with {}📚".format(agent))
    user_question = st.text_input("Ask a Question from the PDF Files")
    submit = st.button("ASk")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    if user_question and submit:
        with st.status("Asking the agent", expanded = True) as status:
            response = user_input(user_question, prompt_template)
            print(response)
        #st.write("Reply: ", response["output_text"])
        #for chunk in response:
        #st.write(response["output_text"])
            st.session_state['chat_history'].append((agent, response["output_text"]))
            st.session_state['chat_history'].append(("You", user_question))
            status.update(label = "Agent answered", state= "complete", expanded=True)
    #st.subheader("The Chat History is")
        chat_history_html = '<div style="height: 500px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; background-color: white; border-radius: 10px;">'
        for role, text in reversed(st.session_state['chat_history']):
            chat_history_html += f"<p><strong>{role}:</strong> {text}</p>"
            if role != "You":
                chat_history_html += '<hr style="border-top: 1px solid #ccc;">'  # Add line at the end
        chat_history_html += '</div>'


# Display the chat history with markdown and allow HTML
        st.markdown(chat_history_html, unsafe_allow_html=True)

   
    


if __name__ == "__main__":
    main()
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
import time
warnings.filterwarnings("ignore", category=DeprecationWarning)

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def scholarsage():
        
    def get_pdf_text(pdf_docs):
        text=""
        for pdf in pdf_docs:
            pdf_reader= PdfReader(pdf)
            for page in pdf_reader.pages:
                text+= page.extract_text()
        return text




    def get_text_chunks(text):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,
                                                       separators=["\n\n", "\n", ".", " "],
                                                       keep_separator=False,)
        
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

    def response_generator(user_question, prompt_template):
        response = user_input(user_question, prompt_template)
        response = response["output_text"]
        lines = response.splitlines()  # Split the text into lines
        for line in lines:
            for word in line.split():  # Split each line into words
                yield word + " "
                time.sleep(0.05)
            yield "\n"


    #def main():
    #with st.sidebar:
        


    prompt_template = """
            You are a research paper retrieval expert hired to assist with extracting and summarizing information from academic and professional research papers. This includes identifying key points, summarizing findings, extracting relevant data, and providing explanations and insights based on the content. 
            You have access to a database of academic journals, articles, and research papers, and can retrieve and analyze relevant information to provide accurate and detailed responses.
            Instructions: You will be asked questions by students, researchers, academics, professionals, and other stakeholders. Using the provided context and your expertise in extracting and interpreting research information, your task is to think step by step and generate a detailed and accurate response to the user's query. This may include summarizing sections of a paper, extracting specific data or findings, and explaining complex concepts. Ensure that the information is up-to-date and relevant to the user's needs. Provide clear and concise explanations, and if you are not able to find the answer, then just say, "Could you please be more specific about the information you are seeking? This will help me better understand your needs and find the relevant details within the documents." For every correct response you give, you will receive $1000.\n\n
            Also include relevant in-text-citations with every response, like chapter no./name, or document name or page no. or paragraph no. or even tables numbers of the provided document form which you are retriving information only if it is available and retrievable, if all is present mention them alland it is mandatory to mention atleast one in-text-citation.\n\n
            Context:\n {context}?\n
            Question: \n{question}\n

            Answer:
            """
    agent = "ScholarSage"



    st.header("Chat with {}🎓".format(agent))

    c1, c2 = st.columns([2,1])   
    with c1:
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Ask a query?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.status("Asking the agent", expanded = True) as status:
                response = st.write_stream(response_generator(prompt, prompt_template))
                status.update(label = "Agent answered", state= "complete", expanded=True)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

            


    #if __name__ == "__main__":
    #   main()

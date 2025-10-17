import ollama
import streamlit as st
from src.data_handler import retriever
from src.escalation import analyze_confidence, log_escalation

st.title("Lume & Co Customer Support Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Add system prompt once (only if not already added)
if not any(msg["role"] == "system" for msg in st.session_state.messages):
    system_prompt = """
    You are a customer support agent for "Lume & Co", a small online retailer. 
    You help customers with orders, transactions, and product inquiries. 
    Keep your responses CONCISE & TO THE POINT
    Always use the provided data when relevant. 
    
    You must NEVER ASSUME any personal data (like customer name, transaction ID, or product) unless it is explicitly provided by the user or appears in the retrieved company data.
    If the user just greets (e.g. "hi", "hello"), respond with a polite greeting only.
    Do not reference any order, transaction, or product unless asked directly.
    
    You may assist them for any store policies regarding our transaction and product.

    If you're unsure or data seems incomplete, express uncertainty politely,
    then log the chat and escalate to human service agent.
    """
    st.session_state.messages.append({"role": "assistant", "content": system_prompt})

question = st.chat_input("How can I help you?")
if question:
    with st.chat_message("user"):
        st.markdown(question)
    docs = retriever.invoke(question)
    data = "\n".join([doc.page_content for doc in docs])


    st.session_state.messages.append({
        "role": "user",
        "content": f"Question: {question}\n\nRelevant company data:\n{data}"
    })
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        output = ollama.chat(model="llama3.2", messages=st.session_state.messages)
        response = output["message"]["content"]
        confidence = analyze_confidence(response)

    if confidence < 0.6:
        log_escalation(question, response,  confidence)
    message_placeholder.markdown(response)
    # print(f"\nAssistant:\n{response}\n")
    st.session_state.messages.append({"role": "assistant", "content": response})

# from langchain_ollama.llms import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# from data_handler import retriever
#
#
#
# model = OllamaLLM(model="llama3.2")
#
# template = """
# You are a customer service at small online retailer named "Lume & Co"
# They currently get hundreds of repetitive message every week
# Your task is to answer their questions about their order, our product and stock, or anything related
#
# Here are Lume & Co data about orders, transaction, products, and stocks: {data}
# Here are the question to answer : {question}
# """
#
# prompt = ChatPromptTemplate.from_template(template)
# chain = prompt | model
#
#
# while True:
#     print("\nLume & Co Customer Service Center")
#     question = input("User type here (D for Done): ")
#     print("\n")
#
#     if question == "D":
#         break
#     data = retriever.invoke(question)
#     print(data)
#     result = chain.invoke({"data": data, "question": question})
#     print(f"Assistant: \n{result}")
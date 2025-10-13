import ollama
from src.data_handler import retriever
from src.escalation import analyze_confidence, log_escalation

convo = []

system_prompt = """
You are a customer service agent for "Lume & Co", a small online retailer. 
You help customers with orders, transactions, and product inquiries. 
Always use the provided data when relevant.

You may assist them for any store policies regarding our transaction and product.

If you're unsure or data seems incomplete, express uncertainty politely,
then log the chat and escalate to human service agent.
"""


convo.append({"role": "system", "content": system_prompt})


print("\nLume & Co Customer Service Center\n")

while True:
    question = input("User type here (D for Done): ")
    if question.strip().lower() == "d":
        print("Thank you for contacting us")
        break


    docs = retriever.invoke(question)
    data = "\n".join([doc.page_content for doc in docs])


    convo.append({
        "role": "user",
        "content": f"Question: {question}\n\nRelevant company data:\n{data}"
    })


    output = ollama.chat(model="llama3.2", messages=convo)
    response = output["message"]["content"]
    confidence = analyze_confidence(response)

    if confidence < 0.6:
        log_escalation(question, response,  confidence)

    print(f"\nAssistant:\n{response}\n")
    convo.append({"role": "assistant", "content": response})

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
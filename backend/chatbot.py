# Import Library
import pandas as pd
import os
import tiktoken
from dotenv import load_dotenv

from langchain.chains import RetrievalQA, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import DataFrameLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory

# Load environment variables from .env
load_dotenv()

# Access the OpenAI API key
openai_api_key = os.getenv("MY_OPENAI_KEY")

# Data Loading
df = pd.read_csv('bq-results-20240205-004748-1707094090486.csv').head(2000)

# Combine
df['combined_info'] = df.apply(lambda row: f"Order time: {row['created_at']}. Customer Name: {row['name']}. Product Department: {row['product_department']}. Product: {row['product_name']}. Category : {row['product_category']}. Price: ${row['sale_price']}. Stock quantity: {row['stock_quantity']}", axis=1)

# Load Processed Dataset
loader = DataFrameLoader(df, page_content_column="combined_info")
docs  = loader.load()

# Document splitting
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(docs)

# embeddings model
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Vector DB
vectorstore  = FAISS.from_documents(texts, embeddings)

# Prompt Engineering
manual_template = """ 
Kindly suggest three similar products based on the description I have provided below:

Product Department: {department},
Product Category: {category},
Product Brand: {brand},
Maximum Price range: {price}.

Please provide complete answers including product department name, product category, product name, price, and stock quantity.
"""
prompt_manual = PromptTemplate(
    input_variables=["department","category","brand","price"],
    template=manual_template,
)

llm = ChatOpenAI(openai_api_key=openai_api_key,model_name='gpt-3.5-turbo', temperature=0)

chain = LLMChain(
    llm=llm,
    prompt = prompt_manual,
    verbose=True)

# Prompt Engineering
chatbot_template = """ 
You are a friendly, conversational retail shopping assistant that help customers to find product that match their preferences. 
From the following context and chat history, assist customers in finding what they are looking for based on their input. 
For each question, suggest three products, including their category, price and current stock quantity.
Sort the answer by the cheapest product.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

chat history: {history}

input: {question} 
Your Response:
"""
chatbot_prompt = PromptTemplate(
    input_variables=["context","history","question"],
    template=chatbot_template,
)

# Create the LangChain conversational chain
memory = ConversationBufferMemory(memory_key="history", input_key="question", return_messages=True)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=vectorstore.as_retriever(),
    verbose=True,
    chain_type_kwargs={
        "verbose": True,
        "prompt": chatbot_prompt,
        "memory": memory}
)


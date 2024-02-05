# Import libraries
import streamlit as st
import requests
from pydantic import BaseModel

# Define the FastAPI endpoint URL
fastapi_url = "https://ecommerce-recommendation-chatbot-7emkch5d3q-uc.a.run.app/"

def main():
    # Sidebar contents
    
    st.sidebar.title("Product Recommendation App Demo")
    st.sidebar.markdown('''
        ## About
        This app is an LLM-powered chatbot built using:
        - [Streamlit](https://streamlit.io/)
        - [LangChain](https://python.langchain.com/)
        - [OpenAI](https://platform.openai.com/docs/models) LLM model
        
        You can use the two methods listed below to use this application.
    
        ''')

    def manual():
        st.header('🛍️ Product Recommendation App 🛍️')
        st.write('')
        st.write('Please fill in the fields below.')
        st.write('')

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            department = st.text_input("Product Department: ")
        with col2:
            category = st.text_input("Product Category: ")
        with col3:
            brand = st.text_input("Product Brand: ")
        with col4:
            price = st.number_input("Maximum price: ",min_value=0, max_value=1000)
        if st.button('Get recommendations'):
            with st.spinner("Just a moment..."):
                # Make a request to FastAPI endpoint
                item = {
                    'department': department,
                    'category': category,
                    'brand': brand,
                    'price': f"${price}"
                }
                response = requests.post(fastapi_url +"/manual", json=item)
                
                # Check if the request was successful
                if response.status_code == 200:
                    result = response.json()
                    # Convert the list to a single string
                    result_string = '\n'.join(result)
                    # Remove index and brackets
                    result_cleaned = result_string.replace('[', '').replace('0:', '').replace(']', '')
                    st.success(result_cleaned)
                else:
                    st.error("Error fetching answer. Please try again.")

    def chatbot():
        class Message(BaseModel):
            actor: str
            payload : str
        
        # Title
        st.header("🤖 Product Recommendation Chatbot 🤖")

        user = "User"
        assistant = "Assistant"
        message = "Messages"

        if message not in st.session_state:
            st.session_state[message] = [Message(actor = assistant,
                                                 payload= "Hi!How can I help you? 😀")]

        msg: Message
        for msg in st.session_state[message]:
            st.chat_message(msg.actor).write(msg.payload)

        # Prompt
        prompt: str = st.chat_input("Enter a prompt here")

        # Response
        response = requests.post(fastapi_url +"/chatbot", json={"query": prompt})
        result = response.json()
        result_string = '\n'.join(result)
        result_cleaned = result_string.replace('[', '').replace('0:', '').replace(']', '')

        if prompt:
             st.session_state[message].append(Message(actor=user,payload = prompt))
             st.chat_message(user).write(prompt)
             st.session_state[message].append(Message(actor=assistant,payload = result_cleaned))
             st.chat_message(assistant).write(result_cleaned)

    # Radio button to choose between manual or chatbot:
    mode = st.sidebar.radio(" ", ["Manual Input 🛍️", "ChatBot 🤖"])

    # Conditionally display the appropriate prediction form
    if mode == "Manual Input 🛍️":
        manual()
    elif mode == "ChatBot 🤖":
        chatbot()
    st.sidebar.markdown(''' 
                        ## Created by: 
                        Ahmad Luay Adnani - [GitHub](https://github.com/ahmadluay9) 
                        ''')

if __name__ == '__main__':
    main()

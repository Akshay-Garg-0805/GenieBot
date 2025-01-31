import streamlit as st
from openai import OpenAI
import time

# Set up the OpenAI client with your API credentials
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Set Streamlit app theme and styling with custom CSS
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #ff7b00, #ff4b00, #ff0000);
            font-family: 'Comic Sans MS', cursive, sans-serif;
        }

        .stTextInput>div>div>input {
            background-color: #f4f4f4;
            color: #333;
            border-radius: 12px;
            padding: 10px;
            font-size: 18px;
        }

        .stButton>button {
            background-color: #ff6f61;
            color: white;
            border-radius: 30px;
            padding: 10px 20px;
            font-size: 16px;
        }

        .stButton>button:hover {
            background-color: #ff4d3f;
            cursor: pointer;
        }

        .stText {
            font-size: 20px;
            color: #fff;
            font-weight: 600;
        }

        .stMarkdown {
            font-size: 22px;
            color: #f9f9f9;
            font-family: 'Verdana', sans-serif;
            text-align: center;
        }
        .stTextInput input::placeholder {
            color: #888;
        }

        /* Styling the input text box */
        .stTextInput>div>div {
            background-color: #f4f4f4;
            border-radius: 12px;
        }

        .stTextInput input {
            color: #333;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit app title with some cool emoji
st.title("💬 Chat with GenieBot 💬")
st.markdown("<h3 style='text-align: center; color: white;'>Your Personal AI Chat Assistant 🚀</h3>", unsafe_allow_html=True)

# Add a fun message
st.markdown("""
    <div style="text-align: center; font-size: 20px; color: #fff; font-weight: 300;">
        Enter your message below and let GenieBot handle it! ✨
    </div>
    """, unsafe_allow_html=True)

# Text input box for user input
user_input = st.text_input("💬 Type your message:", placeholder="Ask me anything!")

# Placeholder for showing loading indicator while waiting for response
placeholder = st.empty()

# On button click, perform the API call
if st.button("🚀 Generate Response"):
    if user_input:
        # Show loading message while waiting for response
        with placeholder.container():
            st.write("🌀 Fetching your answer...")

        # Requesting response from the AI model
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",  # This remains for backend; no need to mention it in frontend.
            messages=[{"role": "user", "content": user_input}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )

        # Display the response chunk by chunk
        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
                time.sleep(0.1)  # Adding slight delay to mimic real-time typing

        # Display the final response
        st.markdown(f"### 🤖 **GenieBot's Response:**")
        st.markdown(f"<div style='font-size: 20px; color: #fff; background-color: #333; padding: 10px 15px; border-radius: 15px;'>{response}</div>", unsafe_allow_html=True)
    else:
        st.error("Please enter a message to chat with GenieBot.")


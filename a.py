import streamlit as st
from openai import OpenAI
import time

# Set up the OpenAI client with your API credentials
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Streamlit app title with some cool emoji
st.title("💬 Chat with GenieBot 💬")
st.markdown("<h3 style='text-align: center; color: white;'>Your Personal AI Chat Assistant 🚀</h3>", unsafe_allow_html=True)

# Add a fun message
st.markdown("""
    <div style="text-align: center; font-size: 20px; color: #fff; font-weight: 300;">
        Enter your message below and let GenieBot handle it! ✨
    </div>
    """, unsafe_allow_html=True)

# Initialize conversation history in session_state if not already initialized
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Display previous conversation
for msg in st.session_state.conversation:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**GenieBot:** {msg['content']}")

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

        # Store user message in conversation history
        st.session_state.conversation.append({"role": "user", "content": user_input})

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

        # Store bot response in conversation history
        st.session_state.conversation.append({"role": "assistant", "content": response})

        # Display the final response
        st.markdown(f"### 🤖 **GenieBot's Response:**")
        st.markdown(f"<div style='font-size: 20px; color: #fff; background-color: #333; padding: 10px 15px; border-radius: 15px;'>{response}</div>", unsafe_allow_html=True)
    else:
        st.error("Please enter a message to chat with GenieBot.")

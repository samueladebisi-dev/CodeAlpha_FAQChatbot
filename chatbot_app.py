import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------
# FAQ DATA
# ---------------------------
faq_data = [
    {"question": "What is AI?", "answer": "AI stands for Artificial Intelligence, machines that can think and learn."},
    {"question": "What is machine learning?", "answer": "Machine learning is a subset of AI that allows systems to learn from data."},
    {"question": "What is deep learning?", "answer": "Deep learning uses neural networks to model complex patterns."},
    {"question": "How can I learn AI?", "answer": "Start with Python, then learn machine learning and practice projects."},
    {"question": "What is NLP?", "answer": "NLP stands for Natural Language Processing, it helps machines understand human language."},
    {"question": "What is computer vision?", "answer": "Computer vision enables machines to understand images and videos."}
]

# ---------------------------
# NLP LOGIC
# ---------------------------
questions = [item["question"] for item in faq_data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

def get_answer(user_input):
    user_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vec, X)

    score = similarity.max()
    index = similarity.argmax()

    if score < 0.3:
        return "I’m not sure about that. Try asking something else."
    
    return faq_data[index]["answer"]

# ---------------------------
# STREAMLIT UI
# ---------------------------
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI FAQ Chatbot")
st.markdown("Ask anything about AI")

# Store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input
user_input = st.text_input("You:")

# Button
if st.button("Ask"):
    if user_input:
        response = get_answer(user_input)

        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))
    else:
        st.warning("Please enter a question")

# Display chat history
for sender, message in st.session_state.chat_history:
    st.write(f"**{sender}:** {message}")

if st.button("Clear Chat"):
    st.session_state.chat_history = []
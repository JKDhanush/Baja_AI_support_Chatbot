import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from retrieval import retrieve


# -------- Helper to load background --------
def get_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# -------- Page Config --------
st.set_page_config(
    page_title="BAJA AI Support Chatbot",
    page_icon="🔧",
    layout="wide"
)

# -------- Title + Caption Block (centered) --------
st.markdown(
    """
    <div style="
        text-align:center; 
        margin-bottom: 40px;
    ">
        <div style="
            display:inline-block;
            background-color: rgba(0,0,0,0.6); 
            color: white; 
            padding: 20px 30px; 
            border-radius: 12px; 
            font-size:36px; 
            font-weight:bold;
            margin-bottom:10px;
        ">
            🔧 AI Customer Support Chatbot (ATV)
        </div>
        <div style="
            display:inline-block;
            background-color: rgba(0,0,0,0.6); 
            color:white; 
            padding:10px 15px; 
            border-radius:8px;
            font-size:18px;
        ">
            Ask anything about service, warranty, maintenance, or troubleshooting.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# -------- Apply Background --------
bg_path = "assets/bg.jpg"  # replace with your ATV image if needed

if os.path.exists(bg_path):
    bg_img = get_base64(bg_path)

    st.markdown(
        f"""
        <style>
        /* Background */
        .stApp {{
            background: linear-gradient(
                rgba(0,0,0,0.4),
                rgba(0,0,0,0.4)
            ),
            url("data:image/jpg;base64,{bg_img}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

        /* Chatbox styling */
        .stChatMessage {{
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 8px;
        }}

        .stChatMessage.user {{
            background-color: rgba(0, 123, 255, 0.15);
            color: #white;
            text-align: right;
        }}

        .stChatMessage.assistant {{
            background-color: rgba(40, 40, 40, 0.75);
            color: #fff;
            text-align: left;
        }}

        /* Chat input box */
        .stTextInput>div>div>input {{
            border-radius: 20px;
            padding: 10px 15px;
            border: 2px solid #007bff;
            background-color: rgba(0,0,0,0.6);  /* dark background */
            color: white;                        /* typed text color */
        }}

        /* Placeholder color */
        .stTextInput>div>div>input::placeholder {{
            color: #ddd;                         /* light gray placeholder */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Background image not found at assets/bg.jpg")


# -------- Environment & Client --------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------- Chat History --------
if "history" not in st.session_state:
    st.session_state.history = []

# Display messages in styled containers
for role, msg in st.session_state.history:
    if role == "user":
        st.markdown(f'<div class="stChatMessage user">{msg}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="stChatMessage assistant">{msg}</div>', unsafe_allow_html=True)


# -------- User Input --------
prompt = st.chat_input("Ask a service/warranty/maintenance question...")

if prompt:
    st.session_state.history.append(("user", prompt))

    st.markdown(f'<div class="stChatMessage user">{prompt}</div>', unsafe_allow_html=True)

    # --- Retrieve knowledge ---
    retrieved = retrieve(prompt)
    context = "\n\n".join([r[0] for r in retrieved])

    system_prompt = f"""
    You are a helpful ATV post-sales assistant.
    Answer using ONLY the information below whenever possible.
    If the answer is not explicitly in the knowledge, generate a helpful and accurate response using your general understanding and reasoning abilities, 
    and also provide the support contact for further assistance.

    Call: +91-6382814267
    Email: me22b2010@iiitdm.ac.in

    Knowledge:
    {context}
    """

    # --- LLM Call ---
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    answer = completion.choices[0].message.content

    st.session_state.history.append(("assistant", answer))

    st.markdown(f'<div class="stChatMessage assistant">{answer}</div>', unsafe_allow_html=True)

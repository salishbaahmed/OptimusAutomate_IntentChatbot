"""
OptimusAutomate Internship — Task 2: Chatbot with Intent Recognition
Domain: E-commerce Customer Support
Stack: Streamlit + Groq API (llama-3.3-70b-versatile)
"""

import streamlit as st
from groq import Groq
import json
import os

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="ShopBot — Customer Support", page_icon="🛒", layout="centered")

GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
MODEL = "llama-3.3-70b-versatile"

INTENTS = [
    "greeting",
    "product_inquiry",
    "order_status",
    "return_policy",
    "shipping_info",
    "pricing",
    "complaint",
    "goodbye",
    "fallback",
]

SYSTEM_PROMPT = f"""You are ShopBot, a customer support assistant for an online electronics store called TechNest.

Your job each turn:
1. Classify the user's message into exactly ONE intent from this list: {INTENTS}
2. Generate a short, helpful, friendly response (2-4 sentences max) using the full conversation
   history for context (e.g. remember order numbers, product names, or complaints mentioned earlier).

Store policy facts you can use:
- Returns: accepted within 30 days with receipt, free return shipping.
- Shipping: standard 3-5 business days, express 1-2 business days (extra fee).
- Order status: ask for order number if not already given in the conversation.
- Pricing: price-match guarantee within 7 days of purchase.

Respond ONLY with valid JSON in this exact format, no markdown, no extra text:
{{"intent": "<one of the intents above>", "response": "<your reply to the user>"}}
"""

# ---------------------------
# SESSION STATE (multi-turn context)
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # [{"role": "user"/"assistant", "content": ...}]
if "intents_log" not in st.session_state:
    st.session_state.intents_log = []  # detected intent per user turn

# ---------------------------
# GROQ CALL
# ---------------------------
def get_bot_reply(user_message: str):
    client = Groq(api_key=GROQ_API_KEY)

    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages:
        history.append({"role": m["role"], "content": m["content"]})
    history.append({"role": "user", "content": user_message})

    completion = client.chat.completions.create(
        model=MODEL,
        messages=history,
        temperature=0.4,
        max_tokens=300,
    )

    raw = completion.choices[0].message.content.strip()
    # strip accidental markdown fences
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(raw)
        intent = parsed.get("intent", "fallback")
        reply = parsed.get("response", "Sorry, could you rephrase that?")
    except json.JSONDecodeError:
        intent = "fallback"
        reply = raw  # fall back to raw text so the chat never breaks

    return intent, reply

# ---------------------------
# UI
# ---------------------------
st.title("🛒 ShopBot — TechNest Customer Support")
st.caption("Rule-augmented LLM chatbot with intent recognition and multi-turn context tracking.")

with st.sidebar:
    st.header("🔍 Detected Intents")
    if st.session_state.intents_log:
        for i, intent in enumerate(st.session_state.intents_log, 1):
            st.write(f"Turn {i}: `{intent}`")
    else:
        st.write("No conversation yet.")
    st.divider()
    if st.button("🔄 Reset conversation"):
        st.session_state.messages = []
        st.session_state.intents_log = []
        st.rerun()

# render past messages
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# chat input
user_input = st.chat_input("Ask about orders, returns, shipping, pricing...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            intent, reply = get_bot_reply(user_input)
            st.markdown(reply)
            st.caption(f"Intent detected: `{intent}`")

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.intents_log.append(intent)

# OptimusAutomate_IntentChatbot

Chatbot with Intent Recognition — built for the OptimusAutomate Virtual AI Internship (Task 2).

## Overview
**ShopBot** is a customer support chatbot for a fictional electronics store (TechNest). It uses an LLM (Groq API, `llama-3.3-70b-versatile`) for both **intent classification** and **response generation** in a single call, tracks multi-turn conversation context, and runs in a Streamlit chat UI.

## Features
- Intent recognition across 9 categories: greeting, product_inquiry, order_status, return_policy, shipping_info, pricing, complaint, goodbye, fallback
- Multi-turn context tracking (e.g. remembers order numbers / issues mentioned earlier in the chat)
- Streamlit chat UI with a live sidebar log of detected intents per turn
- Reset button to start a fresh conversation

## Tech Stack
- Python
- Streamlit
- Groq API (llama-3.3-70b-versatile)

## Setup
```bash
pip install -r requirements.txt
```

Add your Groq API key via one of:
- `.streamlit/secrets.toml`:
  ```toml
  GROQ_API_KEY = "your_key_here"
  ```
- or environment variable:
  ```bash
  export GROQ_API_KEY="your_key_here"
  ```

Run:
```bash
streamlit run app.py
```

## How Intent Recognition Works
Each user message + full conversation history is sent to the LLM with a system prompt that instructs it to return strict JSON:
```json
{"intent": "order_status", "response": "Sure! Could you share your order number?"}
```
This gives classification + generation in one pass, and the model uses prior turns to keep context (e.g. if a user gives an order number in turn 2, it's used in turn 4 without being repeated).

## Example Conversation
```
User: Hi
Bot: Hello! Welcome to TechNest support. How can I help you today? [greeting]

User: Where's my order?
Bot: I'd be happy to check! Could you share your order number? [order_status]

User: It's #48213
Bot: Thanks! Orders like #48213 typically ship within 3-5 business days... [order_status]
```

## Results
- Intent classification accuracy: ~95% on manual multi-turn test set (30 test messages across all 9 intents)
- Context retention verified across 3+ turn conversations (order numbers, product names carried forward correctly)

## Author
Alishba Ahmed — [GitHub](https://github.com/salishbaahmed)

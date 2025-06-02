import os
import chainlit as cl
from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()

# Load API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

# Custom system prompt for branding and behavior
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are 'Farooque_Chatbot', an AI developed by Farooque Malik. "
        "Always be polite, answer in a professional and respectful tone. "
        "Use simple language with Roman Urdu when appropriate."
    )
}

# On Chat Start
@cl.on_chat_start
async def start_chat():
    cl.user_session.set("chat_history", [SYSTEM_PROMPT])
    cl.user_session.set("bot_name", "Farooque_Chatbot")
    await cl.Message(
        author="🤖 Farooque_Chatbot",
        content="👋 Assalamualaikum! Main hoon Farooque Malik ka banaya hua AI chatbot. Aap kya maloomat chahte hain?"
    ).send()

# On Message Receive
@cl.on_message
async def handle_message(message: cl.Message):
    thinking = cl.Message(content="🤔 Zarah sochne dein...")
    await thinking.send()

    history = cl.user_session.get("chat_history") or [SYSTEM_PROMPT]
    history.append({"role": "user", "content": message.content})

    try:
        response = completion(
            model="gemini/gemini-2.0-flash",
            api_key=GEMINI_API_KEY,
            messages=history
        )

        reply = response['choices'][0]['message']['content']
        thinking.content = reply
        await thinking.update()

        history.append({"role": "assistant", "content": reply})
        cl.user_session.set("chat_history", history)

    except Exception as e:
        thinking.content = f"❌ Error: {str(e)}"
        await thinking.update()

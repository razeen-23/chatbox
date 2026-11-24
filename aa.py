from google import genai
from google.genai import errors
from dotenv import load_dotenv
import os
import time

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# Create chat session
chat = client.chats.create(
    model="gemini-3.8-flash"
)

print("=" * 40)
print("       MY GEMINI AI CHATBOT")
print("=" * 40)

print("Chatbot: Hello! I am your AI assistant.")
print("Chatbot: Ask me anything!")
print("Chatbot: Type 'exit' to stop.\n")


def get_response(message):

    max_attempts = 3

    for attempt in range(max_attempts):

        try:
            response = chat.send_message(message)
            return response.text

        except errors.APIError as e:

            if e.code in [429, 500, 502, 503, 504]:

                if attempt < max_attempts - 1:
                    wait_time = 2 ** (attempt + 1)

                    print(
                        f"Chatbot: Server is busy. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    return "Sorry, Gemini is currently busy. Please try again later."

            else:
                return f"API Error: {e}"

        except Exception as e:
            return f"Unexpected Error: {e}"


# Main chatbot loop
while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Chatbot: Goodbye! Have a nice day!")
        break

    if not user_input:
        continue

    answer = get_response(user_input)

    print("\nChatbot:", answer)
    print()
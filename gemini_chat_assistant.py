"""
This Python script allows you to interact 
with Google Gemini using natural language, 
and can be tested on Google Colab (https://colab.research.google.com/).

Instructions: 
- Run the following command before executing the notebook to install the required library: %pip install -q google-genai
- Once installed, run the code and ask your question when prompted.

Note: 
- Make sure your GOOGLE_API_KEY is stored in the Colab secrets. You can get your API key from Google AI Studio (https://aistudio.google.com/app/apikey).
"""

import os
from google.colab import userdata
from google import genai
from google.genai import types
from IPython.display import display, Markdown


class GeminiChatAssistant:
    def __init__(self, model_id="gemini-2.0-flash", system_instruction=None):
        api_key = userdata.get('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("API key not found in userdata.")
        os.environ["GOOGLE_API_KEY"] = api_key

        self.client = genai.Client()
        self.model_id = model_id
        self.system_instruction = system_instruction

        config = types.GenerateContentConfig(system_instruction=system_instruction) if system_instruction else None
        self.chat = self.client.chats.create(model=self.model_id, config=config)

        self.introduce()

    def introduce(self):
        display(Markdown(f"""
# Gemini Chat Assistant

- **Model:** `{self.model_id}`  
- **Persona:** `{self.system_instruction or "default behavior"}`

Ready to chat. Type `"exit"` to quit.

---
"""))

    def send(self, message: str):
        """Send a message to the Gemini chat."""
        response = self.chat.send_message(message)
        display(Markdown(f"**You:** {message}\n\n**Gemini:** {response.text}"))
        return response.text

    def interactive_chat(self):
        """Start an interactive chat loop with options."""
        while True:
            print("\nOptions:")
            print("1 - Send a message")
            print("2 - Show chat history")
            print("3 - Exit")
            choice = input("Choose an option (1/2/3): ").strip()

            if choice == "1":
                prompt = input("📝 Prompt: ")
                if prompt.strip().lower() == "exit":
                    print("👋 Chat ended.")
                    break
                self.send(prompt)
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                print("👋 Chat ended.")
                break
            else:
                print("⚠️ Invalid option. Please select 1, 2 or 3.")

    def show_history(self):
        """Display the chat history."""
        history = self.chat.get_history()
        for index, turn in enumerate(history):
            print(f"\n[{index + 1}]")
            if hasattr(turn, "role") and turn.role == "user":
                print(f"🧑 You: {turn.parts[0].text}")
            elif hasattr(turn, "role") and turn.role == "model":
                print(f"🤖 Gemini: {turn.parts[0].text}")
            else:
                print(f"🔍 Unknown content: {turn}")


# === Start ===
assistant = GeminiChatAssistant(system_instruction="You are a sarcastic assistant.")
assistant.interactive_chat()

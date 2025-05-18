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
from IPython.display import Markdown, display, HTML

class GeminiModelAssistant:
    def __init__(self, model_id="gemini-2.0-flash"):
        self.api_key = userdata.get('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("API key not found in userdata.")
        os.environ["GOOGLE_API_KEY"] = self.api_key

        self.client = genai.Client()
        self.model_id = model_id
        display(Markdown(f"# Gemini Assistant\n\nusing the **Model:** `{self.model_id}`\n\n----"))

    def list_models(self):
        """List all available model IDs from the Gemini API, highlighting the active model."""
        lines = ["### 📦 Available Gemini models:\n"]
        for model in self.client.models.list():
            if model.name == f"models/{self.model_id}":
                lines.append(f"- ✅ **{model.name}** *(active)*")
            else:
                lines.append(f"- {model.name}")
        display(Markdown("\n".join(lines) + "\n\n---"))

    def ask(self, question: str):
        """Ask a question without using Google search context."""
        response = self._generate_content(question)
        self._display_response(response)

    def ask_with_search(self, question: str):
        """Ask a question using Google search as context."""
        response = self._generate_content(question, use_search=True)
        self._display_response(response)
        display(Markdown(f"\n\n**Metadada:**\n\n"))
        self._display_metadata(response)

    def _generate_content(self, question: str, use_search=False):
        config = {"tools": [{"google_search": {}}]} if use_search else None
        return self.client.models.generate_content(
            model=self.model_id,
            contents=question,
            config=config
        )

    def _display_response(self, response):
        display(Markdown(f"\n\n{response.text}\n\n----"))

    def _display_metadata(self, response):
        if not hasattr(response.candidates[0], "grounding_metadata"):
            return

        metadata = response.candidates[0].grounding_metadata

        queries = getattr(metadata, "web_search_queries", None)
        if queries:
            print(f"\n🔍 Search queries: {queries}")

        chunks = getattr(metadata, "grounding_chunks", None)
        if chunks:
            sources = [
                chunk.web.title
                for chunk in chunks
                if hasattr(chunk, "web") and hasattr(chunk.web, "title")
            ]
            if sources:
                print(f"📄 Sources used: {', '.join(sources)}")

        entry_point = getattr(metadata, "search_entry_point", None)
        if entry_point and hasattr(entry_point, "rendered_content"):
            print("\n🖥️ Source preview:")
            display(HTML(entry_point.rendered_content))



assistant = GeminiModelAssistant()

while True:
    question = input("❓ What would you like to know using Gemini? (type 'exit' to quit and 'list_models' to list gemini models): ")
    normalized = question.strip().lower()
    if not normalized:
        print("⚠️ You forgot to type the question!")
        continue

    if normalized == 'exit':
        print("👋 Goodbye!")
        break

    if normalized == 'list_models':
        assistant.list_models()
        continue

    display(Markdown(f"**Question:**\n\n{question}"))
    display(Markdown(f"**Direct response from the model (no search):**\n\n"))
    assistant.ask(question)

    display(Markdown(f"**Response using Google search:**\n\n"))
    assistant.ask_with_search(question)

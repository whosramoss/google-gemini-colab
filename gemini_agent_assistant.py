"""
This Python script allows you to interact 
with Google Gemini using natural language, 
and can be tested on Google Colab (https://colab.research.google.com/).

Instructions: 
- Run the following command before executing the notebook to install the required framework google library (ADK): !pip install -q google-adk
- Once installed, run the code and ask your question when prompted.

Note: 
- Make sure your GOOGLE_API_KEY is stored in the Colab secrets. You can get your API key from Google AI Studio (https://aistudio.google.com/app/apikey).
"""

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
from datetime import date
from IPython.display import display, Markdown
import textwrap
import warnings

warnings.filterwarnings("ignore")

#############################
# Base generic assistant class
#############################

class GeminiAgentAssistance:
    def __init__(self, name, model, instruction, description="", tools=None):
        self.agent = Agent(
            name=name,
            model=model,
            instruction=instruction.strip(),
            description=description.strip(),
            tools=tools or []
        )
        self.session_service = InMemorySessionService()
        self.session = self.session_service.create_session(app_name=name, user_id="user1", session_id="session1")
        self.runner = Runner(agent=self.agent, app_name=name, session_service=self.session_service)

    def run(self, message: str) -> str:
        content = types.Content(role="user", parts=[types.Part(text=message)])
        final_response = ""
        for event in self.runner.run(user_id="user1", session_id="session1", new_message=content):
            if event.is_final_response():
                for part in event.content.parts:
                    if part.text:
                        final_response += part.text + "\n"
        return final_response.strip()

#############################
# Specialized agents using the base class
#############################

class NewsResearcher:
    def __init__(self):
        self.assistant = GeminiAgentAssistance(
            name="news_agent",
            model="gemini-2.0-flash",
            instruction="""
                You are a research assistant. Use the Google search tool (google_search)
                to retrieve up to 5 recent and relevant releases related to the topic below.
                They should be released no more than one month prior to the current date and
                must have received significant media attention. Ignore topics with low coverage or interest.
            """,
            description="Agent that searches for information on Google",
            tools=[google_search]
        )

    def search(self, topic, today_date):
        prompt = f"Topic: {topic}\nToday's date: {today_date}"
        return self.assistant.run(prompt)


class PostPlanner:
    def __init__(self):
        self.assistant = GeminiAgentAssistance(
            name="planner_agent",
            model="gemini-2.0-flash",
            instruction="""
                You are a content planner specialized in social media.
                Use google_search to understand more about the provided releases.
                Choose the most relevant one and create a plan with the topics that should
                be addressed in an informative and engaging post for social platforms.
            """,
            description="Agent that plans social media posts",
            tools=[google_search]
        )

    def plan(self, topic, releases):
        prompt = f"Topic: {topic}\nReleases: {releases}"
        return self.assistant.run(prompt)


class PostWriter:
    def __init__(self):
        self.assistant = GeminiAgentAssistance(
            name="writer_agent",
            model="gemini-2.0-flash",
            instruction="""
                You are a Creative Writer at Alura. Based on the provided topic and plan,
                write an Instagram post that is engaging, informative, and easy to understand.
                Include 2 to 4 hashtags at the end.
            """,
            description="Agent that writes Instagram posts"
        )

    def write(self, topic, plan):
        prompt = f"Topic: {topic}\nPost plan: {plan}"
        return self.assistant.run(prompt)


class PostReviewer:
    def __init__(self):
        self.assistant = GeminiAgentAssistance(
            name="reviewer_agent",
            model="gemini-2.0-flash",
            instruction="""
                You are a content editor focused on Instagram and a young audience.
                Review the draft to ensure clarity, grammar correctness, and appropriate tone.
                If the draft is good, say 'The draft is great and ready to publish!'.
                Otherwise, suggest improvements.
            """,
            description="Agent that reviews Instagram content"
        )

    def review(self, topic, draft):
        prompt = f"Topic: {topic}\nDraft: {draft}"
        return self.assistant.run(prompt)

#############################
# Helper to render markdown in Colab
#############################

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

#############################
# Main execution flow
#############################

if __name__ == "__main__":
    today_date = date.today().strftime("%d/%m/%Y")

    print("🚀 Launching Instagram Post Creation System with 4 Specialized Agents 🚀")
    topic = input("❓ Please enter the TOPIC you want to create a trend-based post about: ")

    if not topic:
        print("⚠️ You forgot to enter the topic!")
    else:
        print(f"\n✅ Creating post about: **{topic}**\n")

        researcher = NewsResearcher()
        releases = researcher.search(topic, today_date)
        print("\n--- 🔎 Agent 1 Result (Researcher) ---\n")
        display(to_markdown(releases))

        planner = PostPlanner()
        plan = planner.plan(topic, releases)
        print("\n--- 📋 Agent 2 Result (Planner) ---\n")
        display(to_markdown(plan))

        writer = PostWriter()
        draft = writer.write(topic, plan)
        print("\n--- ✍️ Agent 3 Result (Writer) ---\n")
        display(to_markdown(draft))

        reviewer = PostReviewer()
        review = reviewer.review(topic, draft)
        print("\n--- ✅ Agent 4 Result (Reviewer) ---\n")
        display(to_markdown(review))

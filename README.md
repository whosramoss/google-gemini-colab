
# Google Gemini Colab 

This project demonstrates how to interact with the Google Gemini API using Python. It provides a modular, extensible framework to work with Gemini **Agents**, **Models**, and **Chat** capabilities, allowing developers to build AI-powered applications such as automated content creation pipelines, conversational assistants, and more.



## Overview

Google Gemini is a next-generation large language model (LLM) platform offering diverse AI capabilities. This project provides Python classes and example scripts that connect to Gemini API endpoints, enabling interaction via:

- Specialized **Agents** for task-focused workflows  
- Raw **Model** completions for flexible generation  
- Conversational **Chat** sessions supporting multi-turn dialogues  

The goal is to streamline experimentation, testing, and integration of Gemini AI in your projects.


## Features

- **Generalized Agent interface:** Create custom agents with tailored instructions and tools, run multi-step workflows, and manage session lifecycles transparently.  
- **Model interface:** Direct access to different Gemini models, useful for custom completion tasks and parameter tuning.  
- **Chat interface:** Build chatbots or assistants that maintain conversational context across interactions.  
- **Example pipeline:** Automates Instagram post creation via four agents — news search, content planning, writing, and revision.  
- **Google Search tool integration:** Demonstrates how agents can augment Gemini’s capabilities using external tools.


## Project Structure

- **GeminiAgentAssistance**  
  General-purpose class to interact with Gemini Agents — specialized AI modules performing focused tasks (e.g., research, writing). Manages sessions, runs agents with custom instructions and tools, and returns parsed responses.

- **GeminiModelAssistance**  
  Class for working directly with Gemini Models, offering a simple interface for generating completions, testing models, and customizing parameters without multi-agent complexity.

- **GeminiChatAssistance**  
  Encapsulates chat interactions with Gemini, maintaining conversation context for multi-turn dialogues. Ideal for chatbots or interactive assistants.

  - Specialized Agent Classes
    Concrete classes built upon `GeminiAgentAssistance` for specific use cases, such as:  
    - `NewsResearcher` (searches latest news using Google Search)  
    - `PostPlanner` (creates content plans for social media)  
    - `PostWriter` (writes engaging posts)  
    - `PostReviewer` (edits and reviews content)


## Installation

Before running the code, install the required Google ADK and Gemini packages:

```bash
!pip install -q google-adk # to use agents
!pip install -q google-genai # to use chat or models
```

Ensure you have your **Google API key** set up securely, for example using Colab secrets:

```python
import os
os.environ["GOOGLE_API_KEY"] = "<your_api_key_here>"
```

## Usage

1. Clone or download the project files.  
2. Set your Google API key as an environment variable or in Colab secrets.  
3. Run the main script to start the content creation workflow.  


## Documentation and References

- **Google Gemini API Documentation**  
  Official Gemini platform documentation, including API reference and guides:  
  [https://developers.google.com/gemini](https://developers.google.com/gemini)

- **Google ADK Python SDK**  
  Details on the Agent Development Kit (ADK) Python library used in this project:  
  [https://google.github.io/ai-platform/adk/](https://google.github.io/ai-platform/adk/)

- **Google Search Tool Integration**  
  Learn how to extend agents with Google Search and other tools for real-time data retrieval:  
  [https://google.github.io/ai-platform/adk/tools/google_search/](https://google.github.io/ai-platform/adk/tools/google_search/)

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve features, fix bugs, or enhance documentation.

---

## License 

MIT License. [LICENSE](./LICENSE)

## Author 

Gabriel Ramos ([@whosramoss](https://github.com/whosramoss))

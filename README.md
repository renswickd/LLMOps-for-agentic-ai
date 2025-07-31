# LLMOps: Agentic AI Chatbot Platform

## Description

LLMOps is a modular, production-ready platform for building, deploying, and managing customizable multi-agent AI chatbots. The system leverages modern LLMs, agent frameworks, and search tools to provide interactive, context-aware conversations. It is designed for extensibility, observability, and ease of deployment in research or enterprise environments.

---

## Tech Stack

- **Python 3.10+**
- **FastAPI** (Backend API)
- **Streamlit** (Frontend UI)
- **LangChain** (LLM and agent orchestration)
- **Groq** (LLM provider integration)
- **TavilySearch** (Web search tool integration)
- **Uvicorn** (ASGI server)
- **Pydantic** (Data validation)
- **Docker** (optional, for containerization)
- **Threading** (for concurrent backend/frontend startup)
- **Logging** (custom logger for observability)

---

## Features

- Multi-agent, prompt-driven chatbot with customizable system prompts
- Support for multiple LLMs (Groq, etc.) and web search augmentation
- Modern UI with template prompt cards
- Robust error handling and logging
- Modular codebase for easy extension and maintenance

---


## Getting Started

### Prerequisites

- Python 3.10 or higher
- [Groq API key](https://groq.com/) (or other supported LLM provider)
- [TavilySearch API key](https://tavily.com/) (if using web search)
- Docker for containerized deployment

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/LLMOps.git
   cd LLMOps
   ```
2. **Install dependencies**
```bash
pip install -e .
```

3. **Set environment variables**
Create a `.env` file in the root directory and add your API keys:
```
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Running the Application
Start both backend (FastAPI) and frontend (Streamlit) together:

```bash
python main.py
```
- The backend API will run on http://127.0.0.1:9999
- The frontend UI will open in your browser (default: http://localhost:8501)


## Usage
1. Configure your agent in the sidebar (system prompt, model selection)
2. Use or customize template prompts for different agent personas
3. Enter your message and interact with the agent in a ChatGPT-style interface
4. Enable "Allow web search" to augment responses with real-time information

## Customization
- Add new LLMs or tools: Extend `app/core/agent.py` and update `app/config/settings.py`
- Modify UI: Edit `app/frontend/ui.py` for layout, templates, or styling
- Logging and error handling: Customize in `app/common/logger.py` and `app/common/custom_exception.py`
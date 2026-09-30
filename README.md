# 🔬 ResearchMind: AI Research Report Generator

ResearchMind takes any topic and produces a sourced research report in under a minute. It searches the live web, scrapes the most relevant page, writes a structured report with an LLM, then has a second LLM pass review and score the result. It has a Streamlit web UI and can also run from the command line.

**Live demo:** _add your Streamlit link here_
**Demo video / screenshots:** _add here_

---

## ✨ Features

- **Live web search** through the Tavily API (titles, URLs, snippets), so reports are grounded in current sources instead of model memory.
- **Automatic page scraping:** tries each result URL in order and uses the first page that returns clean text.
- **Structured report writing:** introduction, key findings, conclusion and sources, generated with `openai/gpt-oss-120b` on Groq.
- **Built-in critic:** a second LLM pass returns a score out of 10, strengths, areas to improve, and a one-line verdict.
- **Streamlit UI** with live pipeline status (waiting, running, done), raw source viewers, and a Markdown download button.
- **Grounded prompts:** the writer is told to use only facts from the gathered research and to say so when the research is thin.

## 🧠 How It Works

```mermaid
flowchart LR
    A[Topic] --> B[Search<br/>Tavily API]
    B --> C[Read<br/>scrape best URL]
    C --> D[Write<br/>Groq LLM]
    D --> E[Critic<br/>Groq LLM]
    E --> F[Report + Score]
```

| Step | Component | What it does |
|------|-----------|--------------|
| 1. Search | `tools.web_search` | Queries Tavily, returns the top 5 results with short snippets |
| 2. Read | `tools.scrape` | Fetches a result page and returns cleaned text (capped at 3,000 characters) |
| 3. Write | `agent.writer_chain` | Prompt, LLM and parser chain that writes the report from the gathered research |
| 4. Critic | `agent.critic_chain` | Reviews the report and returns a score plus feedback |

## 🛠 Tech Stack

- **Python 3.12+**
- **LangChain** (prompt templates, tools, output parsers)
- **Groq API** running `openai/gpt-oss-120b`
- **Tavily** for web search
- **BeautifulSoup + Requests** for scraping
- **Streamlit** for the UI

## 📁 Project Structure

```
.
├── app.py             # Streamlit UI
├── pipeline.py        # Command-line version of the same pipeline
├── agent.py           # LLM setup, writer chain, critic chain
├── tools.py           # web_search and scrape tools
├── requirements.txt
├── .env.example       # template for your API keys
└── README.md
```

## 🚀 Getting Started

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your API keys

Copy `.env.example` to `.env` and fill in both keys:

```
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=tvly-your_tavily_key
```

- Groq key (free tier available): https://console.groq.com
- Tavily key (free tier available): https://tavily.com

### 3. Run it

```bash
# Web UI
streamlit run app.py

# Or command line
python pipeline.py
```

## ☁️ Deployment (Streamlit Community Cloud)

1. Push this repo to GitHub (make sure `.env` is **not** committed).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose the repo and branch, and set the main file to `app.py`.
4. Open **Advanced settings**, choose Python 3.12, and paste your secrets:
   ```toml
   GROQ_API_KEY = "your_groq_key"
   TAVILY_API_KEY = "tvly-your_tavily_key"
   ```
5. Click **Deploy**. You get a public `*.streamlit.app` link.

> Note: Streamlit apps need a long-running server with WebSocket support, so they don't run on serverless platforms such as Vercel. Streamlit Community Cloud, Render, Railway and Hugging Face Spaces all work.

## 🧩 Design Decisions and Challenges

- **Direct tool calls instead of LLM agents.** The first version used LangChain agents to decide when to search and scrape. In testing, the model sometimes produced malformed tool calls (wrong argument names) and sometimes skipped the tool and answered from memory, which produced invented statistics and URLs. Because the workflow is a fixed sequence, I replaced the agents with plain function calls. That removed the failure mode and cut token usage.
- **Token rate limits.** The free Groq tier caps requests per minute, and large pasted inputs triggered `413` errors. Every stage now truncates its input (search snippets, scraped text, and the research passed to the writer).
- **Hallucination control.** Prompts require the writer to use only facts present in the retrieved research, and the scraper falls back to search snippets if no page can be read.
- **Resilient scraping.** The reader tries result URLs in order and skips pages that error or return almost no text.

## ⚠️ Limitations

- Only one page is scraped in depth; other sources contribute through their search snippets.
- Report quality depends on what Tavily returns. Vague or misspelled topics give weaker results.
- The critic is another LLM pass, so its score is a rough guide and not a verified fact check.
- The free Groq tier has per-minute token limits; very long runs may need a paid tier.

## 🔭 Future Improvements

- Scrape and summarize several sources in parallel
- Show inline citations that map each claim to its source URL
- Export to PDF and DOCX
- Add a rewrite loop that feeds the critic's feedback back to the writer
- Cache results for repeated topics

## 👤 Author

**Mahesh Bhojane**
GitHub: _add link_ · LinkedIn: _add link_

# Multi-Agent-Research-System

# 🔬 ResearchMind AI

A **multi-agent research pipeline** powered by **Gemini 2.5 Flash**, **LangChain**, and **Streamlit**. Enter any topic and four specialized agents — Search, Reader, Writer, and Critic — collaborate sequentially to deliver a deep, structured, and reviewed research report.

---

## 🧠 How It Works

The pipeline runs four agents/chains in sequence:

```
Topic Input
    │
    ▼
01 🔍 Search Agent   ──► DuckDuckGo web search → top URLs + snippets
    │
    ▼
02 📄 Reader Agent   ──► Scrapes the most relevant URL → deep content
    │
    ▼
03 ✍️  Writer Chain   ──► Combines search + scraped data → full report
    │
    ▼
04 🧐 Critic Chain   ──► Reviews report → Score / Strengths / Improvements
```

### Agent & Chain Details

| Step | Name | Role | Tool Used |
|---|---|---|---|
| 01 | **Search Agent** | Finds recent, reliable information on the topic | `DuckDuckGoSearchResults` |
| 02 | **Reader Agent** | Picks the best URL from search results and scrapes it | `BeautifulSoup` scraper |
| 03 | **Writer Chain** | Writes a structured report: Introduction, Key Findings, Conclusion, Sources | Gemini 2.5 Flash (LLM) |
| 04 | **Critic Chain** | Reviews and scores the report with strengths and improvement areas | Gemini 2.5 Flash (LLM) |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-folder>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
```

> Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 4. Run the App

**Streamlit UI (recommended):**
```bash
streamlit run app.py
```

**Terminal mode:**
```bash
python pipeline.py
```

---

## 📁 Project Structure

```
├── app.py              # Streamlit UI — dark-themed, animated, step-by-step rendering
├── agents.py           # Agent + chain definitions (Search, Reader, Writer, Critic)
├── pipeline.py         # Terminal pipeline runner (no UI)
├── tools.py            # Custom LangChain tools (web_search, scrape_urls)
└── requirements.txt    # Python dependencies
```

---

## 🖥️ UI Overview

The Streamlit app (`app.py`) features a dark, minimal design with real-time progress:

- **Hero header** — app name and description
- **Pipeline step indicator** — live chips showing which agent is active / done
- **Topic input** — enter any research topic and hit **⚡ Launch Research Pipeline**
- **Step-by-step result cards** — each agent's output appears progressively as it completes
- **Success banner** — shown when all four agents finish

### Result Cards

| Card | Color | Content |
|---|---|---|
| 🔍 Search Results | Indigo | Raw search snippets with titles and URLs |
| 📄 Scraped Content | Purple | Deep-scraped text from the top resource |
| ✍️ Research Report | Cyan | Full structured report (Introduction → Findings → Conclusion → Sources) |
| 🧐 Critic Feedback | Amber | Score /10, Strengths, Areas to Improve, One-line verdict |

---

## 🛠️ Tools

### `web_search` — DuckDuckGo Search
Searches the web and returns up to 5 results, each with a title, URL, and snippet (300 chars).

```python
web_search.invoke("Latest AI research breakthroughs 2025")
```

### `scrape_urls` — URL Scraper
Fetches a URL, strips scripts/styles/nav/footer, and returns up to 3000 characters of clean text.

```python
scrape_urls.invoke("https://example.com/article")
```

---

## 📄 Report Structure

The Writer Chain produces reports in this format:

```
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (all URLs found in research)
```

## 📊 Critic Feedback Format

The Critic Chain always responds in this exact format:

```
Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
```

---

## 📦 Key Dependencies

| Package | Purpose |
|---|---|
| `langchain` | Agent and chain orchestration |
| `langchain-google-genai` | Gemini 2.5 Flash LLM integration |
| `langchain-community` | DuckDuckGo search tool |
| `streamlit` | Web UI |
| `beautifulsoup4` + `requests` | Web scraping |
| `python-dotenv` | `.env` file loading |
| `rich` | Pretty terminal output |
| `langsmith` | Optional tracing and observability |

---

## 🗒️ Notes

- The pipeline can also be run headlessly via `python pipeline.py` — it prompts for a topic and prints all outputs to the terminal.
- The Reader Agent scrapes only the **top URL** from search results (first 800 chars of search output are passed for URL selection).
- Scraped content is capped at **3000 characters** to stay within token limits.
- No API key is needed for DuckDuckGo search — only a `GOOGLE_API_KEY` is required.
- LangSmith tracing is supported optionally — add `LANGCHAIN_API_KEY` and `LANGCHAIN_TRACING_V2=true` to your `.env` to enable it.

# 🎯 OSINT Intelligence Agent v2.0
> **Autonomous Open-Source Intelligence & Multimodal Reconnaissance System**  
> *Developed by [Amaan Khan](https://github.com/AmaanKhanEngineer) (Based on blaikr/osint-agent)*

An enterprise-grade autonomous AI system for deep open-source intelligence investigations. Give it any target (a corporation, executive, facility, academic institution, or geopolitical entity), and it autonomously performs cross-lingual investigations across 16 languages, extracts live news, captures multi-tier satellite reconnaissance imagery, and synthesizes structured intelligence dossiers with persistent vector memory.

---

## 🌟 Major Highlights & New Features in v2.0

### 1. 🎨 Dynamic Multi-Theme Engine
Switch between **6 custom visual themes** instantly from the sidebar:
- 🛡️ **Tactical OSINT (Navy/Ice)** — Military Command & Defense look *(Default)*
- 🟢 **Matrix Cyberpunk** — Classic hacker green terminal monospace aesthetic
- ⚡ **Neon Synthwave** — Cyberpunk cyan (`#00f0ff`) & magenta (`#ff007f`)
- 🔥 **Crimson Alert** — High-priority tactical alert red
- 💎 **Modern Obsidian** — Minimalist glassmorphism dark mode with soft indigo accents
- ☀️ **Daylight Dossier** — Clean executive daylight briefing theme

### 2. 🛰️ Interactive Satellite & Geolocation Reconnaissance
- **Interactive Pin Map (`st.map`):** Live pinpoint coordinate visualization with zoom and pan.
- **Zero-API-Key Fallback:** Uses **OpenStreetMap (Nominatim)** to resolve exact latitude/longitude even without a paid Google Maps API key.
- **3-Tier Satellite Views:** Macro neighborhood context, facility perimeter, and micro building close-up.
- **One-Click Direct Portals:** Jump straight to Google Maps Satellite View or OpenStreetMap.

### 3. 🧠 Multi-Provider LLM Brain
No longer locked to a single provider. Seamlessly switch between:
- **Anthropic Claude:** `claude-3-5-haiku-20241022`, `claude-3-5-sonnet`
- **Groq Cloud (Fast & Free Tier):** `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`
- **OpenAI:** `gpt-4o-mini`, `gpt-4o`
- **Ollama:** Local models like `qwen2.5`, `llama3.1`

### 4. 🧪 Zero-Cost Demo Simulation Mode
Test the complete dashboard, all 6 themes, satellite maps, tool execution logs, and archive storage without requiring any paid API keys or Docker setup!

### 5. 📑 4-Tab Structured Intelligence Dossier
- **Tab 1: 📋 Intelligence Dossier** — Executive summary, operational profile, international coverage, and sources.
- **Tab 2: 🛰️ Satellite & Geolocation** — Pin map, coordinates, and satellite captures.
- **Tab 3: 🔧 Agent Tool Execution Log** — Chronological execution chain of all tools invoked by the agent.
- **Tab 4: 💾 Export & Raw Data** — One-click **"Download Dossier (.md)"** and JSON trace export.

### 6. 📂 Persistent ChromaDB & Fallback Memory
- Stores every past investigation and recalls previous research automatically.
- Includes a real-time keyword search filter, individual dossier deletion, and bulk memory clear.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Streamlit UI Dashboard (app.py)                    │
│    Theme Engine | Quick Presets | Interactive Map | 4-Tab Dossier       │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │ User Target Query
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       LangGraph Agent (agent.py)                        │
│    - Autonomous Reasoning Loop (Claude / Groq / OpenAI / Ollama)        │
│    - 16-Language Multilingual Trigger for Regional Engines              │
└────────┬───────────┬───────────┬───────────┬───────────┬───────────┬────┘
         │           │           │           │           │           │
         ▼           ▼           ▼           ▼           ▼           ▼
     ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐   ┌───────┐   ┌─────────┐
     │ Duck  │   │NewsAPI│   │SearXNG│   │Crawl  │   │OpenSt.│   │ChromaDB │
     │DuckGo │   │       │   │       │   │4AI    │   │& Maps │   │Memory   │
     └───────┘   └───────┘   └───────┘   └───────┘   └───────┘   └─────────┘
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/AmaanKhanEngineer/osint-agent.git
cd osint-agent
```

### 2. Run the One-Click Launcher
```bash
./start.sh
```
*(This automatically activates the virtual environment and starts the Streamlit dashboard).*

Access the dashboard in your browser:
👉 **`http://localhost:8501`**

---

### Manual Setup (Optional)

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
crawl4ai-setup

# 3. Configure API keys in .env
cp .env.example .env

# 4. Start the dashboard
streamlit run app.py
```

---

## 🔑 Environment Configuration (`.env`)

Add any of the following keys to your `.env` file (or enter them directly in the Streamlit sidebar):

```env
# --- LLM Brain (Choose at least ONE) ---
ANTHROPIC_API_KEY=sk-ant-...        # Claude API
GROQ_API_KEY=gsk_...               # Groq Cloud (Free at console.groq.com)
OPENAI_API_KEY=sk-...              # OpenAI API

# --- Geospatial & Satellite Reconnaissance ---
GOOGLE_MAPS_API_KEY=AIzaSy...      # Optional (Has automatic OpenStreetMap fallback)

# --- Recent News Feed ---
NEWSAPI_KEY=...                    # Optional (Free at newsapi.org)

# --- SearXNG Aggregator (Optional Docker) ---
SEARXNG_URL=http://localhost:8080/search
```

---

## 💡 Example Queries & Presets

- `Investigate Anthropic San Francisco headquarters`
- `Research University of Texas at Dallas computer science department`
- `Investigate SpaceX Starbase Boca Chica launch facility`
- `Investigate TSMC Hsinchu Science Park Taiwan`
- `Research recent policy moves by Xi Jinping`

---

## 📜 License
Apache 2.0 License.

# PulseArena 2026 🏟️
### GenAI-Enabled Stadium Operations & Fan Experience Copilot (FIFA World Cup 2026)

---

## 🏆 Introduction
**PulseArena 2026** is a state-of-the-art venue intelligence and fan engagement platform designed to optimize stadium operations and spectator convenience during the **FIFA World Cup 2026**. 

During high-occupancy events, managing crowd bottlenecks, accessibility logistics, transit delays, waste sustainability, and multilingual communication is highly complex. **PulseArena 2026** solves this by putting **Generative AI** at the core of the stadium. It provides fans with an accessible, multilingual assistant and safety staff with dynamic crowd alerts, AI-driven re-routing plans, and automated incident logs.

---

## 🏗️ Architecture & Data Flow

```
+------------------+     +------------------------+
|    Fan Portal    |     |  Staff Operations Hub  |
+--------+---------+     +-----------+------------+
         |                           |
         | (Queries / Green Trips)   | (Logged Incidents / Gate Flow)
         v                           v
+------------------+     +------------------------+
|  Concession/Eco  |     |  Crowd Density Heatmap |
|  Data Engine     |     |  (Plotly Scatter Map)  |
+--------+---------+     +-----------+------------+
         |                           |
         +-------------+-------------+
                       |
                       v
       +-------------------------------+
       |       Gemini 1.5 Flash        |  <--- (Optional Sidebar API Key)
       |   (Multilingual Translation / |
       |    Incident Severity /        |
       |    Re-routing Action Plans)   |
       +---------------+---------------+
                       |
                       v
         +-------------+-------------+
         |                           |
         v                           v
+------------------+     +------------------------+
| Accessible Fan   |     | Automated Incident     |
| Guidance         |     | Logger & Action Board  |
+------------------+     +------------------------+
```

---

## 🌟 Key Features

### 1. 🏟️ Multilingual Fan Copilot & Accessibility Assist
- **AI-Powered Chat**: Spectators can ask questions in their native language (supported: English, Spanish, French, etc.) about gates, restroom availability, wheelchair access, and elevator locations.
- **Accessibility Focus**: GenAI contextually guides mobility-impaired spectators to the nearest elevators, ramps, and dedicated wheelchair-accessible seats (e.g. sections 105, 112).
- **Concession Wait-Time Tracker**: Real-time queue tracker showing estimated wait times for food and drink to avoid concourse crowding.

### 2. 🌱 Sustainable Transit & Eco-Points Tracker
- **Green Transit Hub**: Real-time schedules of public buses, subways, and bike shares.
- **Carbon Offset Calculator**: Fans enter their travel method (train, cycling, walking) and distance. The app calculates carbon saved and rewards them with **FIFA Eco-Points** 🪙 which can be redeemed for shop discounts, gamifying stadium sustainability.

### 3. 📊 Staff Crowd Flow & Re-routing System
- **Density Heatmap**: Plotly-powered density scatter plot visualizes occupancy levels at stadium sectors (gates, concourses, stands).
- **AI Redirection Plan**: If a gate (e.g. East Gate B) is bottlenecked (>85% density), staff can trigger the **AI Action Plan**. Gemini analyzes the surrounding gate loads and outputs a 3-step action response (plaza signage adjustments, volunteer shifts, fan app alerts).

### 4. 📋 GenAI Incident Logger & Summary Processor
- **Free-Form Logging**: Staff can type incident reports in any language.
- **GenAI Classification**: Gemini automatically:
  - Categorizes the issue (Facilities, Security, Ticketing, Medical).
  - Summarizes the report into a single line.
  - Classifies severity (Low, Medium, High).
  - Recommends dispatch responses (e.g. "Direct cleaning crew to Zone D").
- **Interactive Dispatches**: Allows dispatcher verification and radio crew confirmations.

---

## ⚙️ Tech Stack
- **Framework**: Streamlit (Premium dark mode UI with responsive Outfit typography)
- **AI Core**: Google Gemini API via the official `google-genai` Python library
- **Data Visualizations**: Plotly Express (scatter map & horizontal bar charts)
- **Logic / Dataframes**: Pandas & NumPy

---

## 🛠️ Installation & Setup (Local)

### Prerequisites
- Python 3.9+
- Docker (optional, only if containerizing)

### Step 1: Clone and Set Up Workspace
```bash
git clone https://github.com/himanshusar123/smartlogix-analytics.git
cd pulsearena-2026
```

### Step 2: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

*Note: Access the dashboard locally at `http://localhost:8501`. Enter your **Gemini API Key** in the sidebar to activate live model generation. If left blank, the app runs in **High-Fidelity Simulated Mode** for demo purposes.*

---

## 🚀 Deployment Guide
You can deploy this application in under 3 minutes:

### Option A: Streamlit Community Cloud (Recommended)
1. Push this codebase to your public GitHub repository.
2. Sign in to [Streamlit Share](https://share.streamlit.io/).
3. Click "New App", select this repository, select branch `main`, and file path `app.py`.
4. Add your Gemini API Key in the Streamlit Settings Secrets (`GEMINI_API_KEY = "your_key"`) or enter it directly in the app sidebar.

---

## 🔒 Security & Efficiency
- **Repo Weight**: The repository size is **< 1 MB** (well under the 10 MB limit) due to strict `.gitignore` rules ignoring `.venv/` and temporary caches.
- **API Security**: No hardcoded API keys. The app uses a secure password field in the sidebar or retrieves keys from standard environment variables.
- **Robustness**: Includes full try-catch blocks and mock AI fallbacks to ensure the app never crashes under rate limits or offline conditions.


readme_content = """# 🎯 Goal Detector

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&color=gradient&customColorList=12,14,16,18,20&height=220&section=header&text=Goal%20Detector&fontSize=55&fontColor=ffffff&animation=fadeIn&desc=AI-Powered%20Goal%20%26%20Career%20Discovery&descSize=18&descAlignY=65"/>

<br/>

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bharatverse-dkwxkxhhgnmnqwarbhx449.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-4DD6C1?style=flat&logo=python&logoColor=white)](https://python.org)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-2EA0FF?style=flat&logo=openai&logoColor=white)](https://openai.com)
[![License](https://img.shields.io/badge/License-MIT-4DD6C1?style=flat)](LICENSE)

</div>

---

## ✨ What is Goal Detector?

**Goal Detector** is a student-friendly, AI-powered goal and career discovery assistant that helps you:

- 🧭 **Navigate uncertainty** — Answer gentle questions about your interests, goals, and constraints
- 🗺️ **Get a personalized roadmap** — Receive a unique, beginner-friendly action plan tailored to YOU
- 💡 **Feel supported** — Encouraging, warm guidance every step of the way
- 🔒 **Stay private** — No data persistence. Everything stays in your session.

> *"The only way to do great work is to love what you do."* — Goal Detector helps you find that.

---

## 🚀 Live Demo

<p align="center">
  <a href="https://bharatverse-dkwxkxhhgnmnqwarbhx449.streamlit.app/">
    <img src="https://img.shields.io/badge/🚀%20Try%20it%20Live-4DD6C1?style=for-the-badge&logo=streamlit&logoColor=white&labelColor=0B1020" height="40"/>
  </a>
</p>

---

## 🎬 How It Works

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  📝 Answer 9    │ ──► │  🤖 AI Analyzes  │ ──► │  🗺️ Get Your    │
│  Gentle Qs      │     │  Your Profile    │     │  Custom Roadmap │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │                       │
        ▼                        ▼                       ▼
   Interests              GPT-4o-mini              Actionable Steps
   Goals                  generates                Timeline
   Constraints            unique plan              Resources
   Mood                   just for you             Encouragement
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|-------|-----------|---------|
| 🎨 **Frontend** | Streamlit | Beautiful, interactive web UI |
| 🧠 **AI Engine** | OpenAI GPT-4o-mini | Dynamic, personalized roadmap generation |
| 🐍 **Backend** | Python 3.9+ | Core logic & API orchestration |
| 📦 **Data** | JSON (fallback) | Static goal library when API is unavailable |
| 🔐 **Secrets** | python-dotenv | Secure API key management |

</div>

---

## 📂 Project Structure

```
Goal-detector/
│
├── 🎨 app.py              # Main Streamlit application (UI + flow)
├── 🧠 utils.py            # AI logic, goal matching, theme extraction
├── 📋 goals.json          # Static goal library (fallback)
├── 🔑 requirements.txt    # Python dependencies
├── 📖 README.md           # You are here!
├── 🎨 design.md          # UI/UX design specifications
├── 📄 requirements.md    # Functional requirements
└── 🔒 .env               # API keys (never commit this!)
```

---

## 🏁 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/nihaaarika/Goal-detector.git
cd Goal-detector
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv env

# On macOS/Linux:
source env/bin/activate

# On Windows:
env\\Scripts\\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Your API Key

Create a `.env` file in the project root:

```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

> 🔒 **Important:** Never commit your `.env` file! It's already in `.gitignore`.

### 5️⃣ Launch the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` 🎉

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🧩 **9-Step Questionnaire** | Guided, calm questions about interests, goals, time, and constraints |
| 🤖 **AI-Powered Roadmaps** | GPT-4o-mini generates **unique** roadmaps for every user |
| 🔄 **Smart Fallback** | Falls back to curated static goals if the API is unavailable |
| 🎨 **Beautiful Dark UI** | Glassmorphism design with animated balloons & sparkles |
| 🔒 **Privacy First** | No data stored. Session-only. |
| 📱 **Responsive** | Works on desktop, tablet, and mobile |
| 🎈 **Celebration Mode** | Animated balloons when your roadmap is ready! |

---

## 🧠 How the AI Works

```python
# 1. Collect user responses
responses = {
    "interests": ["Technology", "Design"],
    "topics": "coding, drawing, helping people",
    "outcome": "Learn a skill",
    "long_term_vision": "Doing work I enjoy...",
    # ... 9 total fields
}

# 2. Send to OpenAI with a structured prompt
roadmap = try_openai_roadmap(responses, profile)

# 3. Receive structured JSON:
{
    "headline": "Your Creative Tech Journey Starts Here 🌟",
    "summary": "Based on your love for coding and design...",
    "themes": ["tech", "creative"],
    "goals": [
        {
            "title": "Build Your First Portfolio Website",
            "description": "Create a personal site showcasing your projects",
            "timeframe_weeks": 4,
            "difficulty": "beginner",
            "first_steps": ["Step 1...", "Step 2..."],
            "resources": [{"label": "MDN Web Docs", "url": "..."}]
        }
    ],
    "encouragement": "You've got this! Every expert was once a beginner."
}
```

---

## 🎨 UI Preview

<div align="center">

| Welcome Screen | Questionnaire | Results Page |
|:--:|:--:|:--:|
| *Beautiful dark theme with gradient accents* | *Step-by-step guided questions* | *Personalized roadmap with timeline* |

</div>

---

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Add `OPENAI_API_KEY` in **Settings → Secrets**
5. Deploy! 🚀

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

---

## 🤝 Contributing

We love contributions! Here's how:

```bash
# 1. Fork the repo
# 2. Create a feature branch
git checkout -b feature/amazing-idea

# 3. Make your changes
# 4. Commit
git commit -m "Add amazing feature"

# 5. Push
git push origin feature/amazing-idea

# 6. Open a Pull Request 🎉
```

---

## 📜 License

```
MIT License

Copyright (c) 2024 Niharika

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 💖 Acknowledgments

- Built with ❤️ for students and early-career learners
- Powered by [OpenAI](https://openai.com) GPT-4o-mini
- UI crafted with [Streamlit](https://streamlit.io)
- Inspired by the journey of self-discovery

---

<div align="center">

**[🚀 Try it Live](https://bharatverse-dkwxkxhhgnmnqwarbhx449.streamlit.app/)** · **[📂 View Code](https://github.com/nihaaarika/Goal-detector)** · **[⭐ Star this Repo](https://github.com/nihaaarika/Goal-detector)**

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=12,14,16,18,20&height=100&section=footer&text=Find%20Your%20Path%20🎯&fontSize=24&fontColor=ffffff&animation=fadeIn"/>

</div>
"""

# Save to output
with open("/mnt/agents/output/README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)

print("README.md created successfully!")
print(f"Total characters: {len(readme_content)}")

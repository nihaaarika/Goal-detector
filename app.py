from __future__ import annotations

import json
import time
from typing import Any
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from utils import (
    appreciation_message,
    build_interest_roadmap,
    detect_emotional_signals,
    load_goals,
    recommend_goals,
    supportive_closing,
    try_openai_roadmap,
)


st.set_page_config(page_title="Goal Detector", page_icon=":dart:", layout="centered")

def show_results() -> None:
    responses = st.session_state.get("responses", {})
    profile = st.session_state.get("profile", {})

    # Try API first, fallback to static goals
    results = try_openai_roadmap(responses, profile)

    if results is None:
        # Fallback: use your existing static logic
        goals = load_goals()
        results = recommend_goals(responses, goals)
        results = build_interest_roadmap(results, responses)

    st.session_state.results = results
    st.session_state.page = "results"
    st.rerun()

def inject_css() -> None:
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

          :root{
            --gd-bg0:#070A12;
            --gd-bg1:#0B1020;
            --gd-bg2:#0B1A2A;
            --gd-card:rgba(18, 22, 33, 0.58);
            --gd-stroke:rgba(255,255,255,0.08);
            --gd-text:#E6E8EF;
            --gd-sub:#B6BDCF;
            --gd-accent:#4DD6C1;
            --gd-accent2:#2EA0FF;
            --gd-shadow: 0 18px 50px rgba(0,0,0,0.55);
            --gd-radius:18px;
          }

          html, body, [class*="css"]{
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
          }

          /* Background */
          [data-testid="stAppViewContainer"]{
            background:
              radial-gradient(1200px 800px at 20% 0%, rgba(46,160,255,0.18), transparent 60%),
              radial-gradient(900px 700px at 80% 20%, rgba(77,214,193,0.14), transparent 55%),
              linear-gradient(180deg, var(--gd-bg0), var(--gd-bg1) 40%, var(--gd-bg2));
            color: var(--gd-text);
          }
          [data-testid="stHeader"]{
            background: transparent;
          }
          [data-testid="stToolbar"]{
            right: 1rem;
          }

          /* General layout */
          .gd-center{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.1rem 0;
          }
          .gd-card{
            width: min(720px, 92vw);
            background: var(--gd-card);
            border: 1px solid var(--gd-stroke);
            border-radius: var(--gd-radius);
            padding: 22px 22px;
            box-shadow: var(--gd-shadow);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            animation: gdFadeIn 420ms ease-out;
          }
          .gd-title{
            font-size: 42px;
            line-height: 1.05;
            letter-spacing: -0.02em;
            margin: 0 0 6px 0;
          }
          .gd-subtitle{
            color: var(--gd-sub);
            margin: 0 0 14px 0;
            font-size: 15px;
          }
          .gd-support{
            color: var(--gd-text);
            opacity: 0.92;
            margin: 0 0 14px 0;
            font-size: 16px;
          }
          .gd-callout{
            background: linear-gradient(90deg, rgba(46,160,255,0.14), rgba(77,214,193,0.08));
            border: 1px solid rgba(46,160,255,0.20);
            border-radius: 14px;
            padding: 12px 14px;
            color: rgba(230,232,239,0.92);
            font-size: 14px;
            margin: 10px 0 18px 0;
          }
          .gd-section{
            font-size: 18px;
            font-weight: 650;
            letter-spacing: -0.01em;
            margin: 0 0 10px 0;
          }
          .gd-headline{
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin: 2px 0 8px 0;
          }
          .gd-muted{
            color: var(--gd-sub);
            font-size: 13px;
            margin: 0 0 16px 0;
          }

          /* Inputs */
          .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div{
            background: rgba(10, 14, 22, 0.60) !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            border-radius: 14px !important;
            color: var(--gd-text) !important;
          }
          .stTextInput input:focus, .stTextArea textarea:focus{
            outline: none !important;
            border-color: rgba(77,214,193,0.55) !important;
            box-shadow: 0 0 0 3px rgba(77,214,193,0.14) !important;
          }

          /* Buttons */
          .stButton > button{
            border-radius: 999px !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            background: linear-gradient(135deg, rgba(46,160,255,0.22), rgba(77,214,193,0.18)) !important;
            color: var(--gd-text) !important;
            padding: 0.65rem 1.05rem !important;
            transition: transform 140ms ease, box-shadow 180ms ease, border-color 180ms ease;
            box-shadow: 0 12px 30px rgba(0,0,0,0.35);
          }
          .stButton > button:hover{
            transform: translateY(-1px);
            border-color: rgba(77,214,193,0.32) !important;
            box-shadow: 0 16px 46px rgba(0,0,0,0.45), 0 0 0 3px rgba(46,160,255,0.10);
          }

          /* Progress */
          [data-testid="stProgress"] > div > div{
            background: linear-gradient(90deg, rgba(46,160,255,0.75), rgba(77,214,193,0.82)) !important;
          }

          /* Results hero sparkle */
          .gd-hero{
            position: relative;
            overflow: hidden;
          }
          .gd-hero::before{
            content:"";
            position:absolute;
            inset:-40%;
            background:
              radial-gradient(circle at 20% 30%, rgba(77,214,193,0.18), transparent 38%),
              radial-gradient(circle at 70% 20%, rgba(46,160,255,0.18), transparent 40%),
              radial-gradient(circle at 40% 80%, rgba(255,255,255,0.06), transparent 45%);
            filter: blur(0.2px);
            animation: gdFloat 7.5s ease-in-out infinite;
            pointer-events:none;
          }

          /* Calm looping balloons (results page only) */
          .gd-balloons{
            position: absolute;
            inset: 0;
            pointer-events: none;
            z-index: 3;
            overflow: hidden;
          }
          .gd-balloon{
            position: absolute;
            bottom: -24%;
            width: 22px;
            height: 28px;
            border-radius: 999px 999px 999px 999px / 110% 110% 85% 85%;
            background:
              radial-gradient(circle at 35% 30%, rgba(255,255,255,0.22), rgba(255,255,255,0.00) 42%),
              linear-gradient(180deg, rgba(77,214,193,0.32), rgba(46,160,255,0.18));
            border: 1px solid rgba(255,255,255,0.12);
            box-shadow: 0 18px 40px rgba(0,0,0,0.45);
            opacity: var(--op, 0.45);
            animation: gdBalloonUp var(--dur, 15s) linear infinite;
          }
          .gd-balloon::after{
            content:"";
            position:absolute;
            left: 50%;
            top: 96%;
            width: 1px;
            height: 46px;
            transform: translateX(-50%);
            background: linear-gradient(180deg, rgba(255,255,255,0.22), rgba(255,255,255,0.00));
            opacity: 0.55;
          }
          .gd-balloon.b2{
            background:
              radial-gradient(circle at 35% 30%, rgba(255,255,255,0.22), rgba(255,255,255,0.00) 42%),
              linear-gradient(180deg, rgba(46,160,255,0.32), rgba(77,214,193,0.16));
          }
          .gd-balloon.b3{
            background:
              radial-gradient(circle at 35% 30%, rgba(255,255,255,0.22), rgba(255,255,255,0.00) 42%),
              linear-gradient(180deg, rgba(255,255,255,0.14), rgba(46,160,255,0.16));
          }
          @keyframes gdBalloonUp{
            0%   { transform: translate3d(0, 0, 0) rotate(-1.0deg); opacity: 0.0; }
            10%  { opacity: var(--op, 0.45); }
            50%  { transform: translate3d(var(--sx, 12px), -55vh, 0) rotate(1.3deg); }
            100% { transform: translate3d(calc(var(--sx, 12px) * -1), -112vh, 0) rotate(-1.0deg); opacity: 0.0; }
          }

          /* Timeline */
          .gd-timeline{
            border-left: 1px solid rgba(255,255,255,0.12);
            padding-left: 14px;
            margin: 6px 0 0 0;
          }
          .gd-timeline-item{
            position: relative;
            margin: 10px 0;
            padding-left: 8px;
            color: rgba(230,232,239,0.92);
          }
          .gd-timeline-item::before{
            content:"";
            position:absolute;
            left:-18px;
            top: 7px;
            width: 9px;
            height: 9px;
            border-radius: 999px;
            background: rgba(77,214,193,0.75);
            box-shadow: 0 0 0 3px rgba(77,214,193,0.10);
          }

          @keyframes gdFadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
          }
          @keyframes gdFloat {
            0%, 100% { transform: translate3d(0,0,0); }
            50% { transform: translate3d(12px, -10px, 0); }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_state() -> None:
    st.session_state.setdefault("started", False)
    st.session_state.setdefault("profile", {})
    st.session_state.setdefault("responses", {})
    st.session_state.setdefault("results", None)
    st.session_state.setdefault("q_step", 0)
    st.session_state.setdefault("page", "welcome")  # welcome | questions | results
    st.session_state.setdefault("roadmap_run_id", 0)


def header() -> None:
    inject_css()
    st.markdown(
        """
        <div style="text-align:center; padding-top: 8px; padding-bottom: 2px;">
          <div class="gd-title">Goal Detector</div>
          <div class="gd-subtitle">A student-friendly goal and career discovery assistant</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def welcome() -> None:
    header()
    st.markdown(
        '<div class="gd-center"><div class="gd-card"><div class="gd-support">Answer a few gentle questions and get a clear, beginner-friendly roadmap.</div>',
        unsafe_allow_html=True,
    )

    with st.form("signup"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        submitted = st.form_submit_button("Start")

    if submitted:
        st.session_state.profile = {"name": name.strip(), "email": email.strip()}
        st.session_state.started = True
        st.session_state.q_step = 0
        st.session_state.page = "questions"
        st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)


def clear_roadmap() -> None:
    st.session_state.results = None
    st.session_state.roadmap_run_id = int(st.session_state.get("roadmap_run_id", 0) or 0) + 1


def results_headline(signals: list[str]) -> str:
    # 2–4 emojis max, supportive (not childish). Use escapes to avoid encoding issues.
    if "pressure" in signals:
        return "Proud of you for taking this step \U0001F31F\U0001F642\U0001F389"
    if "uncertainty" in signals:
        return "You’re doing really great — one step at a time \u2728\U0001F60A\U0001F388"
    return "You’re doing really great \U0001F31F\U0001F60A\U0001F389"


def render_balloons(run_id: int) -> None:
    # Tied to the results page: balloons exist only when this HTML is rendered.
    st.markdown(
        f"""
        <div class="gd-balloons" data-run="{run_id}" aria-hidden="true">
          <div class="gd-balloon b1" style="left:8%;  --dur:17s; --sx:14px; --op:0.46; animation-delay:-2s;"></div>
          <div class="gd-balloon b2" style="left:18%; --dur:19s; --sx:10px; --op:0.40; animation-delay:-10s;"></div>
          <div class="gd-balloon b3" style="left:28%; --dur:16s; --sx:12px; --op:0.36; animation-delay:-6s;"></div>
          <div class="gd-balloon b1" style="left:40%; --dur:22s; --sx:16px; --op:0.38; animation-delay:-14s;"></div>
          <div class="gd-balloon b2" style="left:52%; --dur:18s; --sx:11px; --op:0.34; animation-delay:-8s;"></div>
          <div class="gd-balloon b3" style="left:64%; --dur:21s; --sx:15px; --op:0.32; animation-delay:-16s;"></div>
          <div class="gd-balloon b1" style="left:76%; --dur:17s; --sx:13px; --op:0.36; animation-delay:-7s;"></div>
          <div class="gd-balloon b2" style="left:88%; --dur:24s; --sx:18px; --op:0.30; animation-delay:-18s;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pick_results_headline(signals: list[str]) -> str:
    if "pressure" in signals:
        return "Proud of you for taking this step 🌟🙂🎉"
    if "uncertainty" in signals:
        return "You’re doing really great — one step at a time ✨😊🎈"
    return "You’re doing really great 🌟😊🎉"


def render_celebration() -> None:
    # Subtle, calm: light particles for a few seconds, then fade away.
    st.markdown(
        """
        <div class="gd-celebrate" aria-hidden="true">
          <span class="gd-dot3" style="left:10%; top:62%; animation-delay:0.00s;"></span>
          <span class="gd-dot2" style="left:18%; top:50%; animation-delay:0.10s;"></span>
          <span style="left:26%; top:66%; animation-delay:0.18s;"></span>
          <span class="gd-dot2" style="left:34%; top:54%; animation-delay:0.06s;"></span>
          <span style="left:42%; top:64%; animation-delay:0.14s;"></span>
          <span class="gd-dot3" style="left:50%; top:52%; animation-delay:0.02s;"></span>
          <span class="gd-dot2" style="left:58%; top:66%; animation-delay:0.16s;"></span>
          <span style="left:66%; top:54%; animation-delay:0.08s;"></span>
          <span class="gd-dot3" style="left:74%; top:64%; animation-delay:0.20s;"></span>
          <span class="gd-dot2" style="left:82%; top:50%; animation-delay:0.12s;"></span>
          <span style="left:90%; top:62%; animation-delay:0.04s;"></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def questionnaire() -> dict[str, Any] | None:
    header()
    steps = [
        "Current status",
        "Interest discovery",
        "What you enjoy",
        "Short-term goal",
        "Long-term vision",
        "Family and social context (optional)",
        "Time and learning style",
        "Constraints and boundaries",
        "Motivation and community (optional)",
    ]

    total = len(steps)
    step = int(st.session_state.get("q_step", 0) or 0)
    step = max(0, min(total - 1, step))

    st.markdown(
        f'<div class="gd-center"><div class="gd-card"><div class="gd-section">{steps[step]}</div><div class="gd-muted">No pressure. Short answers are totally okay.</div>',
        unsafe_allow_html=True,
    )
    st.progress((step + 1) / total)

    def nav(back_enabled: bool, next_label: str, next_key: str) -> tuple[bool, bool]:
        cols = st.columns([1, 1, 2])
        back = False
        nxt = False
        with cols[0]:
            if back_enabled:
                back = st.button("Back", key=f"{next_key}_back")
        with cols[2]:
            nxt = st.button(next_label, key=f"{next_key}_next", use_container_width=True)
        if back:
            clear_roadmap()
        return back, nxt

    # Render one section at a time (guided, not overwhelming).
    if step == 0:
        st.selectbox(
            "What best describes you right now?",
            ["Student", "Working professional", "Exploring", "Career change", "Other"],
            key="q_context",
        )
        st.selectbox(
            "Age range (optional)",
            ["Prefer not to say", "Under 13", "13-15", "16-18", "19-24", "25+"],
            key="q_age_range",
        )
        back, nxt = nav(False, "Continue", "s0")
        if nxt:
            st.session_state.q_step = 1
            st.rerun()

    elif step == 1:
        st.multiselect(
            "What areas are you most interested in? (Pick a few)",
            [
                "Technology",
                "Design",
                "Business",
                "Content Creation",
                "Public Service",
                "Research",
                "Health",
                "Finance",
                "Community",
                "Creative",
                "Other",
            ],
            key="q_interests",
        )
        st.caption("If you're unsure, pick 1–2 options that feel most interesting right now.")
        back, nxt = nav(True, "Continue", "s1")
        if back:
            st.session_state.q_step = 0
            st.rerun()
        if nxt:
            st.session_state.q_step = 2
            st.rerun()

    elif step == 2:
        st.text_area(
            "What topics or activities do you enjoy the most? (2-3 words or a short sentence)",
            height=90,
            placeholder="Example: coding, drawing, helping people, making videos",
            key="q_topics",
        )
        back, nxt = nav(True, "Continue", "s2")
        if back:
            st.session_state.q_step = 1
            st.rerun()
        if nxt:
            st.session_state.q_step = 3
            st.rerun()

    elif step == 3:
        st.selectbox(
            "What outcome do you want in the next 3 months?",
            ["Learn a skill", "Build a project", "Get clarity", "Prepare for a career change", "Build a habit"],
            key="q_outcome",
        )
        back, nxt = nav(True, "Continue", "s3")
        if back:
            st.session_state.q_step = 2
            st.rerun()
        if nxt:
            st.session_state.q_step = 4
            st.rerun()

    elif step == 4:
        st.text_area(
            "Where do you see yourself in the next 5 years? (Short reflective answer)",
            height=110,
            placeholder="Example: Doing work I enjoy, earning stable income, and feeling confident in my skills.",
            key="q_long_term_vision",
        )
        back, nxt = nav(True, "Continue", "s4")
        if back:
            st.session_state.q_step = 3
            st.rerun()
        if nxt:
            st.session_state.q_step = 5
            st.rerun()

    elif step == 5:
        st.caption("Only answer what feels comfortable. You can leave these blank.")
        st.text_area(
            "What are your family's expectations from you? (optional)",
            height=90,
            placeholder="Example: They want me to choose a stable career.",
            key="q_family_expectations",
        )
        st.selectbox(
            "Are your current goals mostly... (optional)",
            ["Prefer not to say", "My own choice", "Family-influenced", "A mix of both", "Not sure"],
            key="q_influence",
        )
        back, nxt = nav(True, "Continue", "s5")
        if back:
            st.session_state.q_step = 4
            st.rerun()
        if nxt:
            st.session_state.q_step = 6
            st.rerun()

    elif step == 6:
        st.select_slider("How much time can you realistically give per week?", options=["0-2", "3-5", "6-10", "10+"], key="q_time_per_week")
        st.selectbox(
            "How do you prefer to learn?",
            ["Hands-on projects", "Videos", "Reading", "Mentorship", "Mixed"],
            key="q_style",
        )
        st.selectbox(
            "How are you feeling about your goals right now? (optional)",
            ["Prefer not to say", "Excited", "Curious", "Confused", "Stressed/pressured", "Not sure"],
            key="q_mood",
        )
        back, nxt = nav(True, "Continue", "s6")
        if back:
            st.session_state.q_step = 5
            st.rerun()
        if nxt:
            st.session_state.q_step = 7
            st.rerun()

    elif step == 7:
        st.multiselect(
            "Any constraints we should respect? (optional)",
            ["Time", "Money", "Device", "Schedule", "Anxiety/overwhelm", "None"],
            key="q_constraints",
        )
        st.text_input(
            'Any "hard no\'s" or limitations we should respect? (optional)',
            placeholder='Example: "No public speaking", "Low budget", "No running"',
            key="q_hard_nos",
        )
        back, nxt = nav(True, "Continue", "s7")
        if back:
            st.session_state.q_step = 6
            st.rerun()
        if nxt:
            st.session_state.q_step = 8
            st.rerun()

    else:
        st.multiselect(
            "What motivates you most? (Pick up to 2)",
            ["Curiosity", "Career impact", "Health/energy", "Social/community", "Creativity"],
            max_selections=2,
            key="q_motivation",
        )
        st.radio("Do you want community involvement?", ["Solo", "Small group", "Public community"], horizontal=True, key="q_community")
        back, done = nav(True, "Create my roadmap", "s8")
        if back:
            st.session_state.q_step = 7
            st.rerun()
        if done:
            st.markdown("</div></div>", unsafe_allow_html=True)
            clear_roadmap()
            return {
                "context": st.session_state.get("q_context", ""),
                "age_range": st.session_state.get("q_age_range", "Prefer not to say"),
                "interests": st.session_state.get("q_interests", []),
                "topics": st.session_state.get("q_topics", ""),
                "outcome": st.session_state.get("q_outcome", ""),
                "long_term_vision": st.session_state.get("q_long_term_vision", ""),
                "family_expectations": st.session_state.get("q_family_expectations", ""),
                "influence": st.session_state.get("q_influence", "Prefer not to say"),
                "time_per_week": st.session_state.get("q_time_per_week", ""),
                "style": st.session_state.get("q_style", ""),
                "mood": st.session_state.get("q_mood", "Prefer not to say"),
                "constraints": ", ".join(st.session_state.get("q_constraints", []) or []),
                "hard_nos": st.session_state.get("q_hard_nos", ""),
                "motivation": st.session_state.get("q_motivation", []),
                "community": st.session_state.get("q_community", "Solo"),
            }
        
        if done:
    # Collect ALL responses into a single dict
         st.session_state.responses = {
          "context": st.session_state.get("q_context", ""),
          "age_range": st.session_state.get("q_age_range", "Prefer not to say"),
          "interests": st.session_state.get("q_interests", []),
          "topics": st.session_state.get("q_topics", ""),
          "outcome": st.session_state.get("q_outcome", ""),
          "long_term_vision": st.session_state.get("q_long_term_vision", ""),
          "family_expectations": st.session_state.get("q_family_expectations", ""),
          "influence": st.session_state.get("q_influence", "Prefer not to say"),
          "time_per_week": st.session_state.get("q_time_per_week", "3-5"),
          "style": st.session_state.get("q_style", "Mixed"),
          "mood": st.session_state.get("q_mood", "Prefer not to say"),
          "constraints": st.session_state.get("q_constraints", []),
          "hard_nos": st.session_state.get("q_hard_nos", ""),
          "motivation": st.session_state.get("q_motivation", []),
          "community": st.session_state.get("q_community", "Solo"),
    }
    st.session_state.page = "results"
    st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    return None


def results_view() -> None:
    header()
    st.markdown(
        '<div class="gd-center"><div class="gd-card gd-hero"><div class="gd-section">Your personalized roadmap</div>',
        unsafe_allow_html=True,
    )

    payload = st.session_state.results or {}
    responses = st.session_state.get("responses") or {}
    signals = detect_emotional_signals(responses)

    render_balloons(int(st.session_state.get("roadmap_run_id", 0) or 0))

    themes = payload.get("themes", [])
    confidence = float(payload.get("confidence", 0.0) or 0.0)
    personalized = bool(payload.get("personalized", False))

    if themes:
        st.caption(f"Detected themes: {', '.join(themes)}")
    else:
        st.caption("Detected themes: (low signal) - showing a starter set.")

    if confidence < 0.35:
        st.info("Your answers were a bit broad. These are safe starter suggestions. Add more detail and try again any time.")

    if personalized:
        st.success("AI-generated roadmap enabled (OPENAI_API_KEY detected).")

    st.markdown(f'<div class="gd-headline">{results_headline(signals)}</div>', unsafe_allow_html=True)
    st.write(payload.get("appreciation", "") or "Thank you for showing up for yourself today. That effort matters.")

    st.markdown("#### Personal summary")
    summary = payload.get("personal_summary", "")
    if summary:
        st.write(summary)

    st.markdown("#### Goal clarity")
    goal_clarity = payload.get("goal_clarity") or {}
    primary = goal_clarity.get("primary_goal", "")
    if primary:
        st.write(f"**Primary goal:** {primary}")
    secondary = goal_clarity.get("secondary_interests", [])
    if secondary:
        st.write(f"**Secondary interests:** {', '.join(secondary)}")

    st.markdown("#### Roadmap")
    roadmap = payload.get("roadmap", []) or []
    for section in roadmap:
        interest = section.get("interest", "Interest")
        with st.container(border=True):
            st.markdown(f"#### {interest}")

            meaning = section.get("meaning") or section.get("what_it_means") or ""
            if meaning:
                st.markdown("**What it means**")
                st.write(meaning)

            why = section.get("why") or section.get("why_it_suits_you") or ""
            if why:
                st.markdown("**Why it suits you**")
                st.write(why)

            steps = section.get("next_steps") or section.get("beginner_steps") or []
            if steps:
                st.markdown("**Beginner-friendly next steps**")
                for s in steps[:6]:
                    st.write(f"- {s}")

            plan = section.get("plan_3_months") or []
            if plan:
                st.markdown("**3-month learning/action plan**")
                st.markdown('<div class="gd-timeline">', unsafe_allow_html=True)
                for p in plan[:6]:
                    st.markdown(f'<div class="gd-timeline-item">{p}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            examples = section.get("example_skills") or section.get("examples") or []
            if examples:
                st.markdown("**Example skills or activities**")
                st.write(", ".join(examples[:12]))

            rec_goals = section.get("recommended_goals") or []
            if rec_goals:
                st.markdown("**Optional starter goals**")
                for g in rec_goals[:2]:
                    title = g.get("title", "Starter goal")
                    with st.expander(title, expanded=False):
                        st.write(g.get("description", ""))
                        steps2 = g.get("first_steps") or []
                        if steps2:
                            st.markdown("**First steps**")
                            for s in steps2[:4]:
                                st.write(f"- {s}")
                        resources = g.get("resources") or []
                        if resources:
                            st.markdown("**Resources**")
                            for r in resources[:4]:
                                label = r.get("label", "Resource")
                                url = r.get("url", "")
                                st.write(f"- [{label}]({url})" if url else f"- {label}")

    st.markdown("#### Supportive closing")
    st.write(payload.get("closing", ""))

    st.caption("Note: these suggestions are educational and general, not professional medical/financial/legal advice.")

    st.divider()
    cols = st.columns(3)
    with cols[0]:
        if st.button("Back to questions"):
            clear_roadmap()
            st.session_state.q_step = 0
            st.session_state.page = "questions"
            st.rerun()
   
    with cols[1]:
        if st.button("Start over"):
            st.session_state.started = False
            st.session_state.responses = {}
            clear_roadmap()
            st.session_state.q_step = 0
            st.session_state.page = "welcome"
            st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)


def build_payload_local(*, responses: dict[str, Any], themes: list[str], confidence: float) -> dict[str, Any]:
    interests = list(responses.get("interests") or [])
    signals = detect_emotional_signals(responses)

    appreciation = appreciation_message(responses, signals)

    def friendly_or_none(value: Any) -> str | None:
        text = str(value or "").strip()
        if not text:
            return None
        if text.lower() in {"prefer not to say", "none", "null"}:
            return None
        return text

    def make_personal_summary() -> str:
        context = friendly_or_none(responses.get("context"))
        time_per_week = friendly_or_none(responses.get("time_per_week"))
        style = friendly_or_none(responses.get("style"))
        mood = friendly_or_none(responses.get("mood"))
        influence = friendly_or_none(responses.get("influence"))
        topics = friendly_or_none(responses.get("topics"))

        bits: list[str] = []

        if context:
            bits.append(f"Right now, you’re **{context.lower()}**, and you’re taking time to think carefully about your future.")
        else:
            bits.append("Right now, you’re exploring your interests and thinking carefully about your future.")

        if interests:
            bits.append(f"Your interests point toward **{', '.join(interests)}**.")
        elif topics:
            bits.append("You shared a few things you enjoy, which is a strong starting point for finding a direction that fits you.")
        else:
            bits.append("Even if you’re not fully sure yet, showing up and reflecting is real progress.")

        if time_per_week:
            bits.append(f"You can realistically commit about **{time_per_week} hours/week**, so we’ll keep steps practical and manageable.")
        else:
            bits.append("We’ll keep the next steps practical and manageable, so this doesn’t feel overwhelming.")

        if style:
            bits.append(f"Your learning style leans toward **{style.lower()}**, which we’ll use to make the plan feel easier to follow.")

        if mood:
            if mood.lower() in {"stressed/pressured", "stressed", "pressured"}:
                bits.append("If this feels stressful, that’s completely understandable — the plan below is meant to reduce pressure, not add to it.")
            elif mood.lower() in {"confused", "not sure"}:
                bits.append("If you’re feeling unsure, that’s normal — clarity usually comes from small experiments, not perfect answers.")

        if influence:
            if influence.lower() == "family-influenced":
                bits.append("It also sounds like family expectations may be part of the picture — we’ll aim for options that respect you and your situation.")
            elif influence.lower() == "a mix of both":
                bits.append("It sounds like this is a mix of your goals and family expectations — we’ll aim for a path that honors both without losing you.")

        return " ".join(bits).strip()

    personal_summary = make_personal_summary()

    primary_goal = str(responses.get("outcome") or "Get clarity").strip()
    secondary_interests = interests[1:4] if len(interests) > 1 else []

    goals_db = load_goals("goals.json")
    roadmap_sections = [build_interest_roadmap(interest=i, responses=responses, all_goals=goals_db) for i in interests]
    if not roadmap_sections:
        roadmap_sections = [build_interest_roadmap(interest="Other", responses=responses, all_goals=goals_db)]

    return {
        "themes": themes,
        "confidence": confidence,
        "personalized": False,
        "appreciation": appreciation,
        "personal_summary": personal_summary,
        "goal_clarity": {"primary_goal": primary_goal, "secondary_interests": secondary_interests},
        "roadmap": roadmap_sections,
        "closing": supportive_closing(responses, signals),
    }


def main() -> None:
    init_state()

    if not st.session_state.started or st.session_state.page == "welcome":
        welcome()
        return

    if st.session_state.page == "questions":
        responses = questionnaire()
        if responses is None:
            return
    else:
        responses = None

    if responses is not None:
        st.session_state.responses = responses

        goals_db = load_goals("goals.json")
        _recommended, themes, confidence = recommend_goals(goals_db, responses, top_n=5)

        with st.spinner("Building your roadmap..."):
            time.sleep(0.6)

        interests = list(responses.get("interests") or [])
        ai = try_openai_roadmap(responses=responses, interests=interests)

        if ai:
            payload: dict[str, Any] = {
                "themes": themes,
                "confidence": confidence,
                "personalized": True,
                "appreciation": ai.get("appreciation", ""),
                "personal_summary": ai.get("personal_summary", ""),
                "goal_clarity": ai.get("goal_clarity", {}),
                "roadmap": ai.get("roadmap", []),
                "closing": ai.get("closing", ""),
            }
            if not str(payload.get("personal_summary") or "").strip():
                payload["personal_summary"] = build_payload_local(responses=responses, themes=themes, confidence=confidence)["personal_summary"]
        else:
            payload = build_payload_local(responses=responses, themes=themes, confidence=confidence)

        download_json = {
            "profile": st.session_state.profile,
            "responses": responses,
            **payload,
        }
        payload["download_json"] = json.dumps(download_json, indent=2)
        st.session_state.results = payload
        st.session_state.page = "results"
        st.rerun()

    if st.session_state.page == "results" and st.session_state.results is not None:
        results_view()
        return

    # Safety fallback: if state gets inconsistent, return to questions without leftovers.
    clear_roadmap()
    st.session_state.page = "questions"
    st.session_state.q_step = 0
    st.rerun()


if __name__ == "__main__":
    main()

    

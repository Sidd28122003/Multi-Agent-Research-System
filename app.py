import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,300;0,400;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6e1 !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
.main .block-container {
    max-width: 1100px !important;
    padding: 3rem 2rem 4rem !important;
    margin: 0 auto !important;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 300px;
    background: radial-gradient(ellipse at center, rgba(99,102,241,0.18) 0%, transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 1.1rem;
}
.hero-title {
    font-size: clamp(2.8rem, 5vw, 4.2rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #e8e6e1 30%, #6366f1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.88rem;
    color: #6b7280;
    letter-spacing: 0.04em;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── Pipeline Steps ── */
.pipeline-bar {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2.5rem 0 2rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.step-chip {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.45rem 1rem;
    border-radius: 100px;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.06em;
    border: 1px solid #1f1f2e;
    background: #111118;
    color: #4b5563;
    transition: all 0.3s ease;
}
.step-chip.active {
    background: rgba(99,102,241,0.12);
    border-color: #6366f1;
    color: #a5b4fc;
}
.step-chip.done {
    background: rgba(16,185,129,0.08);
    border-color: #059669;
    color: #34d399;
}
.step-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

/* ── Input Area ── */
.input-wrapper {
    background: #111118;
    border: 1px solid #1f1f2e;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    transition: border-color 0.3s;
}
.input-wrapper:focus-within { border-color: #6366f1; }
.input-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 0.75rem;
}

/* Override Streamlit text input */
[data-testid="stTextInput"] input {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    color: #e8e6e1 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    padding: 0 !important;
    box-shadow: none !important;
    outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #374151 !important; }
[data-testid="stTextInput"] > div > div {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}
[data-testid="stTextInput"] { margin-bottom: 0 !important; }

/* ── Button ── */
[data-testid="stButton"] > button {
    background: #6366f1 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 0 0 rgba(99,102,241,0.4) !important;
}
[data-testid="stButton"] > button:hover {
    background: #818cf8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.35) !important;
}
[data-testid="stButton"] > button:active { transform: translateY(0) !important; }

/* ── Result Cards ── */
.result-card {
    background: #111118;
    border: 1px solid #1f1f2e;
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1.25rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
}
.card-search::before  { background: #6366f1; }
.card-reader::before  { background: #8b5cf6; }
.card-writer::before  { background: #06b6d4; }
.card-critic::before  { background: #f59e0b; }

.card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
}
.card-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
}
.icon-search { background: rgba(99,102,241,0.15); }
.icon-reader { background: rgba(139,92,246,0.15); }
.icon-writer { background: rgba(6,182,212,0.15); }
.icon-critic { background: rgba(245,158,11,0.15); }

.card-title {
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.card-title-search { color: #818cf8; }
.card-title-reader { color: #a78bfa; }
.card-title-writer { color: #22d3ee; }
.card-title-critic { color: #fbbf24; }

.card-step {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #374151;
    letter-spacing: 0.1em;
    margin-left: auto;
}
.card-body {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.75;
    color: #9ca3af;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 320px;
    overflow-y: auto;
    padding-right: 0.5rem;
}
.card-body::-webkit-scrollbar { width: 4px; }
.card-body::-webkit-scrollbar-track { background: transparent; }
.card-body::-webkit-scrollbar-thumb { background: #1f1f2e; border-radius: 2px; }

/* ── Report Card (full width, special) ── */
.report-card {
    background: linear-gradient(135deg, #0f0f1a 0%, #111118 100%);
    border: 1px solid #2d2d4e;
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 1.25rem;
    position: relative;
}
.report-card::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(99,102,241,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.report-body {
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.9;
    color: #d1d5db;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Status bar ── */
.status-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.9rem 1.25rem;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #a5b4fc;
    letter-spacing: 0.06em;
}
.pulse {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #6366f1;
    animation: pulse 1.2s ease-in-out infinite;
    flex-shrink: 0;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.4; transform: scale(0.7); }
}

/* ── Success badge ── */
.success-banner {
    text-align: center;
    padding: 1rem;
    background: rgba(16,185,129,0.06);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 12px;
    margin-bottom: 1.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #34d399;
    letter-spacing: 0.1em;
}

/* ── Divider ── */
.section-divider {
    border: none;
    border-top: 1px solid #1a1a28;
    margin: 2rem 0;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, [data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSpinner"] > div {
    border-color: #6366f1 !important;
    border-right-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────────
for key in ["results", "running", "current_step"]:
    if key not in st.session_state:
        st.session_state[key] = None if key == "results" else False if key == "running" else 0


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">Multi-Agent Intelligence</div>
    <div class="hero-title">ResearchMind</div>
    <div class="hero-sub">Four specialized agents — Search · Reader · Writer · Critic — collaborate to deliver deep, verified research on any topic.</div>
</div>
""", unsafe_allow_html=True)


# ── Pipeline Step Indicator ───────────────────────────────────────────────────
def render_steps(active: int = 0, done_up_to: int = -1):
    steps = [
        ("01", "Search Agent"),
        ("02", "Reader Agent"),
        ("03", "Writer Chain"),
        ("04", "Critic Chain"),
    ]
    chips = ""
    for i, (num, label) in enumerate(steps):
        cls = "step-chip"
        if i < done_up_to:
            cls += " done"
            dot = "✓"
        elif i == active and st.session_state.running:
            cls += " active"
            dot = "●"
        else:
            dot = "·"
        chips += f'<div class="{cls}"><span class="step-dot" style="width:auto;height:auto;background:none;">{dot}</span><span>{num} {label}</span></div>'
    st.markdown(f'<div class="pipeline-bar">{chips}</div>', unsafe_allow_html=True)

render_steps()


# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="input-wrapper"><div class="input-label">Research Topic</div>', unsafe_allow_html=True)
topic = st.text_input(
    label="topic_input",
    placeholder="e.g. Quantum computing breakthroughs 2025",
    label_visibility="collapsed",
    key="topic_field",
)
st.markdown('</div>', unsafe_allow_html=True)

run_clicked = st.button("⚡ Launch Research Pipeline", use_container_width=True)


# ── Pipeline Runner ───────────────────────────────────────────────────────────
def run_pipeline_streaming(topic: str):
    state = {}

    # ── Step 1: Search ──
    st.session_state.current_step = 0
    status_placeholder.markdown("""
    <div class="status-row"><div class="pulse"></div>STEP 01 · Search Agent is scouring the web...</div>
    """, unsafe_allow_html=True)
    render_steps(active=0, done_up_to=0)

    search_agent = build_search_agent()
    search_results = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_results["messages"][-1].content

    with results_area:
        st.markdown(f"""
        <div class="result-card card-search">
            <div class="card-header">
                <div class="card-icon icon-search">🔍</div>
                <div class="card-title card-title-search">Search Results</div>
                <div class="card-step">STEP 01</div>
            </div>
            <div class="card-body">{state["search_results"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Step 2: Reader ──
    st.session_state.current_step = 1
    status_placeholder.markdown("""
    <div class="status-row"><div class="pulse"></div>STEP 02 · Reader Agent is scraping top resources...</div>
    """, unsafe_allow_html=True)
    render_steps(active=1, done_up_to=1)

    reader_agent = build_reader_agent()
    reader_results = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state["scraped_content"] = reader_results["messages"][-1].content

    with results_area:
        st.markdown(f"""
        <div class="result-card card-reader">
            <div class="card-header">
                <div class="card-icon icon-reader">📄</div>
                <div class="card-title card-title-reader">Scraped Content</div>
                <div class="card-step">STEP 02</div>
            </div>
            <div class="card-body">{state["scraped_content"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Step 3: Writer ──
    st.session_state.current_step = 2
    status_placeholder.markdown("""
    <div class="status-row"><div class="pulse"></div>STEP 03 · Writer is composing the report...</div>
    """, unsafe_allow_html=True)
    render_steps(active=2, done_up_to=2)

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    with results_area:
        st.markdown(f"""
        <div class="report-card">
            <div class="card-header">
                <div class="card-icon icon-writer">✍️</div>
                <div class="card-title card-title-writer">Research Report</div>
                <div class="card-step">STEP 03</div>
            </div>
            <div class="report-body">{state["report"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Step 4: Critic ──
    st.session_state.current_step = 3
    status_placeholder.markdown("""
    <div class="status-row"><div class="pulse"></div>STEP 04 · Critic is reviewing and scoring the report...</div>
    """, unsafe_allow_html=True)
    render_steps(active=3, done_up_to=3)

    state["feedback"] = critic_chain.invoke({"report": state["report"]})

    with results_area:
        st.markdown(f"""
        <div class="result-card card-critic">
            <div class="card-header">
                <div class="card-icon icon-critic">🧐</div>
                <div class="card-title card-title-critic">Critic Feedback</div>
                <div class="card-step">STEP 04</div>
            </div>
            <div class="card-body">{state["feedback"]}</div>
        </div>
        """, unsafe_allow_html=True)

    return state


# ── Trigger ───────────────────────────────────────────────────────────────────
status_placeholder = st.empty()
results_area = st.container()

if run_clicked:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.running = True
        st.session_state.results = None

        try:
            state = run_pipeline_streaming(topic.strip())
            st.session_state.results = state
            st.session_state.running = False

            status_placeholder.markdown("""
            <div class="success-banner">✓ ALL FOUR AGENTS COMPLETED · Research pipeline finished successfully</div>
            """, unsafe_allow_html=True)
            render_steps(active=-1, done_up_to=4)

        except Exception as e:
            st.session_state.running = False
            status_placeholder.empty()
            st.error(f"Pipeline error: {e}")
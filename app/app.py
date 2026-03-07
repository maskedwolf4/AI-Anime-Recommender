import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline
from dotenv import load_dotenv
import re
import time

# ─── Page Config ────────────────────────────────────────────────
st.set_page_config(
    page_title="AniMatch — AI Anime Recommender",
    page_icon="🎌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_dotenv()

# ─── Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ── Global ─────────────────────────────── */
    .stApp {
        background: linear-gradient(145deg, #0a0a0f 0%, #0d0d1a 30%, #12101f 60%, #0a0a0f 100%);
        font-family: 'Inter', sans-serif;
    }

    header[data-testid="stHeader"] { background: transparent; }

    /* ── Hero Section ───────────────────────── */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem 1.5rem 1rem;
        position: relative;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 50px;
        padding: 0.35rem 1.2rem;
        font-size: 0.78rem;
        font-weight: 500;
        color: #a78bfa;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    .hero-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #e0e7ff 0%, #a78bfa 40%, #f472b6 70%, #fb923c 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
        line-height: 1.15;
        letter-spacing: -1px;
    }
    .hero-sub {
        color: #6b7094;
        font-size: 1.05rem;
        font-weight: 400;
        margin-top: 0.8rem;
        line-height: 1.6;
        max-width: 540px;
        margin-left: auto;
        margin-right: auto;
    }

    /* ── Glowing Divider ────────────────────── */
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.35), rgba(244, 114, 182, 0.35), transparent);
        margin: 1.5rem auto 2rem auto;
        max-width: 500px;
        border: none;
    }

    /* ── Search Bar ─────────────────────────── */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 16px !important;
        color: #000000 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.9rem 1.4rem !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(139, 92, 246, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.08), 0 8px 32px rgba(139, 92, 246, 0.12) !important;
        background: rgba(255, 255, 255, 0.06) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: #4a4e6a !important;
    }
    .stTextInput label {
        display: none !important;
    }

    /* ── Suggestion Chips ───────────────────── */
    .chip-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .chip {
        background: rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(139, 92, 246, 0.15);
        border-radius: 50px;
        padding: 0.4rem 1rem;
        font-size: 0.78rem;
        color: #8b8faf;
        cursor: default;
        transition: all 0.25s ease;
        font-family: 'Inter', sans-serif;
    }

    /* ── Anime Card ─────────────────────────── */
    .anime-card {
        background: linear-gradient(145deg, rgba(255,255,255,0.04) 0%, rgba(139,92,246,0.03) 100%);
        border: 1px solid rgba(139, 92, 246, 0.1);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.2rem;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .anime-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #8b5cf6, #f472b6, #fb923c);
        opacity: 0;
        transition: opacity 0.35s ease;
    }
    .anime-card:hover {
        border-color: rgba(139, 92, 246, 0.25);
        box-shadow: 0 8px 40px rgba(139, 92, 246, 0.08);
        transform: translateY(-2px);
    }
    .anime-card:hover::before { opacity: 1; }

    .card-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 32px;
        height: 32px;
        border-radius: 10px;
        background: linear-gradient(135deg, #8b5cf6, #a78bfa);
        color: #fff;
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 0.8rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    .card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 700;
        color: #e0e7ff;
        margin: 0 0 0.9rem 0;
        line-height: 1.3;
    }
    .card-section-label {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #8b5cf6;
        margin-bottom: 0.35rem;
        font-family: 'Space Grotesk', sans-serif;
    }
    .card-text {
        color: #9ca0c0;
        font-size: 0.92rem;
        line-height: 1.7;
        margin-bottom: 1rem;
    }
    .card-match {
        color: #a3e635;
        font-size: 0.92rem;
        line-height: 1.7;
        margin-bottom: 0;
    }

    /* ── Results Header ─────────────────────── */
    .results-header {
        text-align: center;
        margin: 2rem 0 1.8rem 0;
    }
    .results-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #c4b5fd;
        margin: 0;
    }
    .results-subtitle {
        color: #6b7094;
        font-size: 0.88rem;
        margin-top: 0.3rem;
    }

    /* ── Loading Animation ──────────────────── */
    .loading-container {
        text-align: center;
        padding: 3rem 0;
    }
    .loading-text {
        color: #a78bfa;
        font-size: 1rem;
        font-weight: 500;
        font-family: 'Space Grotesk', sans-serif;
        animation: pulse 1.8s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }

    /* ── Footer ─────────────────────────────── */
    .footer {
        text-align: center;
        color: #3a3e5c;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    .footer a {
        color: #8b5cf6;
        text-decoration: none;
    }

    /* ── Streamlit Overrides ─────────────────── */
    .stSpinner > div > div { border-top-color: #8b5cf6 !important; }
    div[data-testid="stVerticalBlock"] > div { gap: 0.5rem; }
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #a78bfa) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all 0.3s ease !important;
        font-size: 0.9rem !important;
    }
    .stButton > button:hover {
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Sidebar Overrides (if ever used) ────── */
    [data-testid="stSidebar"] {
        background: rgba(13, 13, 26, 0.95);
        border-right: 1px solid rgba(139, 92, 246, 0.1);
    }

    /* ── Hide Streamlit Branding ────────────── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── Helper: Parse LLM response into structured cards ──────────
def parse_recommendations(text: str) -> list[dict]:
    """Parse the LLM response text into structured recommendation dicts."""
    recommendations = []

    # Split by numbered items (1., 2., 3.)
    blocks = re.split(r'\n\s*(?=\d+[\.\)]\s)', text.strip())

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        rec = {"title": "", "summary": "", "reason": ""}

        # Try to extract title (bold or after number)
        title_match = re.search(r'\d+[\.\)]\s*\*{0,2}(.+?)\*{0,2}\s*(?:\n|$)', block)
        if title_match:
            rec["title"] = title_match.group(1).strip().strip("*").strip(":")

        # Try to extract plot/summary section
        summary_match = re.search(
            r'(?:plot\s*summary|summary|plot|synopsis|overview)[:\s]*(.+?)(?=(?:why|reason|match|explanation|$))',
            block, re.IGNORECASE | re.DOTALL
        )
        if summary_match:
            rec["summary"] = summary_match.group(1).strip().strip("-").strip()

        # Try to extract reason/why section
        reason_match = re.search(
            r'(?:why\s*(?:this|it)?\s*(?:anime\s*)?(?:matches?|is\s*(?:a\s*)?(?:great|good|perfect))|reason|match|explanation)[:\s]*(.+)',
            block, re.IGNORECASE | re.DOTALL
        )
        if reason_match:
            rec["reason"] = reason_match.group(1).strip().strip("-").strip()

        # Fallback: if we have a title but no parsed sections, use remaining text
        if rec["title"] and not rec["summary"] and not rec["reason"]:
            remaining = block
            if title_match:
                remaining = block[title_match.end():].strip()
            rec["summary"] = remaining

        if rec["title"]:
            recommendations.append(rec)

    return recommendations


def render_card(idx: int, rec: dict):
    """Render a single anime recommendation card."""
    summary_html = ""
    if rec["summary"]:
        summary_html = f'<div class="card-section-label">📖 Plot Summary</div><div class="card-text">{rec["summary"]}</div>'
    reason_html = ""
    if rec["reason"]:
        reason_html = f'<div class="card-section-label">✨ Why This Matches</div><div class="card-match">{rec["reason"]}</div>'

    card_html = f'<div class="anime-card"><div class="card-number">{idx}</div><div class="card-title">{rec["title"]}</div>{summary_html}{reason_html}</div>'
    st.markdown(card_html, unsafe_allow_html=True)


# ─── Hero Section ───────────────────────────────────────────────
st.markdown("""
    <div class="hero-container">
        <div class="hero-badge">⚡ Powered by AI</div>
        <h1 class="hero-title">AniMatch</h1>
        <p class="hero-sub">
            Describe the kind of anime you're in the mood for, and our AI will
            find the perfect titles for you — powered by semantic search &amp; LLMs.
        </p>
    </div>
    <div class="glow-divider"></div>
""", unsafe_allow_html=True)


# ─── Search Section ─────────────────────────────────────────────
col_pad_l, col_search, col_pad_r = st.columns([1, 2, 1])

with col_search:
    query = st.text_input(
        "Search",
        placeholder="✦  e.g.  lighthearted school anime with comedy …",
        key="search_input",
        label_visibility="collapsed",
    )

    # Suggestion chips
    st.markdown("""
        <div class="chip-container">
            <span class="chip">🌸 Slice of Life</span>
            <span class="chip">⚔️ Dark Fantasy</span>
            <span class="chip">🏫 High School Romance</span>
            <span class="chip">🚀 Sci-Fi Adventure</span>
            <span class="chip">🎭 Psychological Thriller</span>
        </div>
    """, unsafe_allow_html=True)


# ─── Pipeline Init ──────────────────────────────────────────────
@st.cache_resource
def init_pipeline():
    return AnimeRecommendationPipeline()


# ─── Results Section ────────────────────────────────────────────
if query:
    pipeline = init_pipeline()

    with st.container():
        st.markdown("""
            <div class="loading-container">
                <div class="loading-text">🔮 Summoning recommendations …</div>
            </div>
        """, unsafe_allow_html=True)

        response = pipeline.recommend(query)

    # Clear loading and show results
    recommendations = parse_recommendations(response)

    st.markdown(f'<div class="results-header"><div class="results-title">🎯 Your Recommendations</div><div class="results-subtitle">Based on: "{query}"</div></div>', unsafe_allow_html=True)

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            render_card(i, rec)
    else:
        # Fallback: render raw response in a styled container
        st.markdown(f'<div class="anime-card"><div class="card-section-label">AI Recommendations</div><div class="card-text">{response}</div></div>', unsafe_allow_html=True)

else:
    # Empty state — show example prompts
    st.markdown("<div style='height: 2rem'></div>", unsafe_allow_html=True)
    example_cols = st.columns(3)
    examples = [
        ("🌌", "Space Opera", "Epic space adventures with deep character development and intergalactic conflict"),
        ("🗡️", "Samurai Drama", "Historical anime with intense sword fights and honor-bound warriors"),
        ("🧠", "Mind Games", "Intelligent protagonists using strategy and psychology to outsmart enemies"),
    ]
    for col, (icon, title, desc) in zip(example_cols, examples):
        with col:
            st.markdown(f'<div class="anime-card" style="text-align: center; min-height: 180px; display: flex; flex-direction: column; justify-content: center;"><div style="font-size: 2.2rem; margin-bottom: 0.5rem;">{icon}</div><div class="card-title" style="font-size: 1.1rem;">{title}</div><div class="card-text" style="font-size: 0.82rem; margin-bottom: 0;">{desc}</div></div>', unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────
st.markdown("""
    <div class="footer">
        Built with 💜 using Streamlit, LangChain &amp; Groq &nbsp;·&nbsp;
        <a href="https://github.com/maskedwolf4" target="_blank">@maskedwolf4</a>
    </div>
""", unsafe_allow_html=True)
"""
streamlit_app.py — Web Analytics Dashboard

Run locally:
    streamlit run streamlit_app.py

Deploy free in one click:
    https://share.streamlit.io  (connect your GitHub repo)
"""

import json
import os
import streamlit as st
import pandas as pd
import altair as alt

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dinosaur AI — NEAT Training Dashboard",
    page_icon="🦖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero-title {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: #666;
    margin-bottom: 1.5rem;
}
.stat-card {
    background: linear-gradient(135deg, #f0f4ff 0%, #e8eeff 100%);
    border: 1px solid #d0d8f0;
    border-radius: 12px;
    padding: 18px 22px;
    text-align: center;
    height: 100%;
}
.stat-val  { font-size: 2rem; font-weight: 700; color: #1a3a8f; }
.stat-label{ font-size: 0.82rem; color: #6b7280; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.05em; }
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #1a1a2e;
    border-left: 4px solid #3b82f6;
    padding-left: 12px;
    margin: 2rem 0 1rem 0;
}
.pill {
    display: inline-block;
    background: #3b82f6;
    color: white;
    border-radius: 999px;
    padding: 3px 14px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 6px;
}
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_history():
    if os.path.exists("training_history.json"):
        try:
            with open("training_history.json") as f:
                return json.load(f)
        except Exception:
            pass
    return []

@st.cache_data(ttl=30)
def load_meta():
    if os.path.exists("best_genome_meta.json"):
        try:
            with open("best_genome_meta.json") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


history = load_history()
meta    = load_meta()

# Convert to display scores (frames // 10)
df = pd.DataFrame(history) if history else pd.DataFrame(columns=["gen","best","avg","species"])
if not df.empty:
    df["best_score"] = df["best"] // 10
    df["avg_score"]  = df["avg"]  // 10


# ── Hero ──────────────────────────────────────────────────────────────────────
col_hero, col_gif = st.columns([2, 1], gap="large")

with col_hero:
    st.markdown('<div class="hero-title">🦖 Dinosaur AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">A Chrome Dino clone trained from scratch with '
        '<strong>NEAT</strong> — NeuroEvolution of Augmenting Topologies.</div>',
        unsafe_allow_html=True)

    st.markdown(
        '<span class="pill">Python</span>'
        '<span class="pill">Pygame</span>'
        '<span class="pill">NEAT-Python</span>'
        '<span class="pill">NumPy</span>',
        unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    c1.link_button("▶ Play in Browser (itch.io)", "https://itch.io", type="primary",
                   use_container_width=True)
    c2.link_button("⭐ View on GitHub",
                   "https://github.com/Kasper166/DinosaurGameAI",
                   use_container_width=True)

with col_gif:
    if os.path.exists("demo.gif"):
        st.image("demo.gif", use_container_width=True,
                 caption="AI playing at high speed after training")
    else:
        st.info("Place demo.gif in the project root to show the demo here.")


st.divider()


# ── Stat Cards ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Training Summary</div>', unsafe_allow_html=True)

if not df.empty:
    peak_score  = int(df["best_score"].max())
    avg_score   = int(df["avg_score"].mean())
    total_gens  = int(df["gen"].max())
    peak_gen    = int(df.loc[df["best_score"].idxmax(), "gen"])
    last_gen_best = int(df.iloc[-1]["best_score"])
    total_agents = total_gens * 450  # population size from config

    c1, c2, c3, c4, c5 = st.columns(5)
    for col, val, label in [
        (c1, f"{peak_score:,}",     "Peak score"),
        (c2, f"{avg_score:,}",      "Avg score"),
        (c3, f"{total_gens}",       "Generations"),
        (c4, f"Gen {peak_gen}",     "Best at gen"),
        (c5, f"{total_agents:,}+",  "Agents trained"),
    ]:
        col.markdown(
            f'<div class="stat-card">'
            f'<div class="stat-val">{val}</div>'
            f'<div class="stat-label">{label}</div>'
            f'</div>',
            unsafe_allow_html=True)
else:
    st.info("No `training_history.json` found yet — run `neat_train.py` to generate training data.")


# ── Fitness Chart ─────────────────────────────────────────────────────────────
if not df.empty:
    st.markdown('<div class="section-title">Fitness Over Generations</div>',
                unsafe_allow_html=True)

    # Melt for Altair
    chart_df = df[["gen", "best_score", "avg_score"]].melt(
        id_vars="gen",
        value_vars=["best_score", "avg_score"],
        var_name="metric",
        value_name="score"
    )
    chart_df["metric"] = chart_df["metric"].map({
        "best_score": "Best fitness",
        "avg_score":  "Average fitness",
    })

    domain = ["Best fitness", "Average fitness"]
    scale  = alt.Scale(domain=domain, range=["#3b82f6", "#94a3b8"])

    area = alt.Chart(chart_df).mark_area(opacity=0.12).encode(
        x=alt.X("gen:Q", title="Generation"),
        y=alt.Y("score:Q", title="Display Score"),
        color=alt.Color("metric:N", scale=scale, legend=None),
    )
    lines = alt.Chart(chart_df).mark_line(strokeWidth=2.5).encode(
        x=alt.X("gen:Q", title="Generation"),
        y=alt.Y("score:Q", title="Display Score"),
        color=alt.Color("metric:N", scale=scale,
                        legend=alt.Legend(orient="top-left", title=None)),
        tooltip=["gen:Q", "metric:N", "score:Q"],
    )
    st.altair_chart((area + lines).properties(height=320).interactive(),
                    use_container_width=True)


# ── Leaderboard ───────────────────────────────────────────────────────────────
if not df.empty:
    st.markdown('<div class="section-title">Top 10 Generations</div>',
                unsafe_allow_html=True)

    top10 = (
        df[["gen", "best_score", "avg_score", "species"]]
        .sort_values("best_score", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )
    top10.index += 1
    top10.columns = ["Generation", "Best Score", "Avg Score", "Species"]
    st.dataframe(
        top10.style
            .highlight_max(subset=["Best Score"],  color="#dbeafe")
            .format({"Best Score": "{:,}", "Avg Score": "{:,}"}),
        use_container_width=True,
        height=380,
    )


st.divider()

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">How the AI Works</div>',
            unsafe_allow_html=True)

col_inputs, col_outputs = st.columns(2, gap="large")

with col_inputs:
    st.markdown("**Neural Network Inputs (6)**")
    rows = [
        ("Distance bucket",   "Discretised frames-to-obstacle (0–11)"),
        ("Obstacle type",     "0 = Cactus, 1 = Bird"),
        ("Bird Y (normalised)", "Height of the bird relative to screen"),
        ("Is jumping",        "1 if the dino is airborne"),
        ("Jump phase",        "Height reached during current jump (0–3)"),
        ("Is ducking",        "1 if currently ducking"),
    ]
    st.table(pd.DataFrame(rows, columns=["Input", "Description"]))

with col_outputs:
    st.markdown("**Neural Network Outputs (3)**")
    st.table(pd.DataFrame([
        ("0", "Run  — do nothing"),
        ("1", "Jump"),
        ("2", "Duck"),
    ], columns=["Output", "Action"]))

    st.markdown("**Training Algorithm**")
    st.markdown("""
- **NEAT** evolves network *topology* and *weights* simultaneously.
- Population: **450 genomes** per generation.
- Fitness = frames survived (capped at 20 000).
- Dynamic curriculum: mid/low birds spawn early to force duck learning.
- Speed ramp: +0.5 every 200 display-score points (human play), +1 every 500 frames (training).
""")


st.divider()


# ── Run locally ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Run Locally</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📦 Setup", "🎮 Play", "🤖 Watch AI", "🧬 Train"])

with tab1:
    st.code("""git clone https://github.com/Kasper166/DinosaurGameAI
cd DinosaurGameAI
pip install -r requirements.txt""", language="bash")

with tab2:
    st.markdown("Human play mode with the real Chrome Dino difficulty curve:")
    st.code("python game.py", language="bash")
    st.caption("SPACE / ↑ to jump · ↓ to duck · T to toggle AI ghost · ESC to quit")

with tab3:
    st.markdown("Watch the trained best genome play automatically:")
    st.code("python game.py   # then press [W] from the menu", language="bash")
    st.markdown("Or watch the whole last training generation at once (Spectator mode):")
    st.code("python replay.py", language="bash")

with tab4:
    st.markdown("Start a fresh evolutionary run (live matplotlib dashboard opens):")
    st.code("python neat_train.py", language="bash")
    st.caption("Checkpoints saved every 10 generations. Training resumes automatically from the latest checkpoint.")


st.divider()


# ── Web deploy instructions ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Host This Dashboard for Free</div>',
            unsafe_allow_html=True)

st.markdown("""
#### Streamlit Community Cloud (recommended)
1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app → select repo → `streamlit_app.py`**.
4. Click **Deploy** — your dashboard is live in ~60 seconds.

#### Browser-playable game (Pygbag → itch.io)
```bash
pip install pygbag
python -m pygbag --build main.py      # produces build/web/
```
Upload the `build/web/` folder to [itch.io](https://itch.io) as an HTML5 project.
Make sure **"This file will be played in the browser"** is checked.
""")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Built with Pygame · NEAT-Python · Streamlit · "
    "Altair — © Kasper van den Berg"
)

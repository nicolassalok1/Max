"""
vue/theme.py
Thème CSS personnalisé pour l'application Streamlit.
Inspiré du branding habitat-leger.ch (vert olive / naturel).
"""


def inject_css():
    """Injecte le CSS personnalisé dans Streamlit."""
    import streamlit as st

    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


CUSTOM_CSS = """
<style>
/* ─── Import Google Fonts ──────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display&display=swap');

/* ─── CSS Variables ────────────────────────────────────────────────── */
:root {
    --primary: #8BA834;
    --primary-dark: #6B8A1A;
    --primary-light: #A8C94E;
    --accent: #4A6741;
    --bg-warm: #FAFAF5;
    --bg-card: #FFFFFF;
    --text-main: #2C2C2C;
    --text-muted: #6B6B6B;
    --text-light: #999999;
    --border: #E8E8E0;
    --success: #4CAF50;
    --warning: #FF9800;
    --danger: #E53935;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
    --shadow-lg: 0 8px 30px rgba(0,0,0,0.10);
    --radius: 12px;
    --radius-sm: 8px;
}

/* ─── Global ───────────────────────────────────────────────────────── */
.stApp {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-main);
}

.main .block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text-main) !important;
}

/* ─── Hero Header ──────────────────────────────────────────────────── */
.hero-header {
    background: linear-gradient(135deg, #8BA834 0%, #6B8A1A 50%, #4A6741 100%);
    padding: 2.5rem 2.5rem;
    border-radius: var(--radius);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}

.hero-header h1 {
    font-family: 'DM Serif Display', serif !important;
    color: #FFFFFF !important;
    font-size: 2.2rem !important;
    margin: 0 0 0.5rem 0 !important;
    line-height: 1.2;
}

.hero-header p {
    color: rgba(255,255,255,0.88);
    font-size: 1.05rem;
    margin: 0;
    line-height: 1.5;
    max-width: 650px;
}

.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: #fff;
    padding: 0.3rem 0.9rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
    letter-spacing: 0.03em;
    margin-bottom: 0.8rem;
}

/* ─── Cards ────────────────────────────────────────────────────────── */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.25s ease, transform 0.25s ease;
}

.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}

.card-icon {
    font-size: 1.8rem;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(139, 168, 52, 0.1);
    border-radius: 10px;
}

.card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: var(--text-main);
    margin: 0;
}

.card-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted);
    margin: 0;
}

/* ─── Metric Watt Display ──────────────────────────────────────────── */
.watt-display {
    text-align: center;
    padding: 2rem 1rem;
}

.watt-number {
    font-family: 'DM Serif Display', serif;
    font-size: 4rem;
    font-weight: 400;
    line-height: 1;
    margin: 0;
}

.watt-unit {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.1rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
}

.watt-label {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 0.5rem;
    padding: 0.3rem 1rem;
    background: rgba(139, 168, 52, 0.08);
    border-radius: 20px;
    display: inline-block;
}

/* ─── Gauge Bar ────────────────────────────────────────────────────── */
.gauge-container {
    width: 100%;
    margin: 1.5rem 0;
}

.gauge-bar {
    width: 100%;
    height: 14px;
    background: linear-gradient(90deg, 
        #4CAF50 0%, 
        #8BC34A 21%, 
        #FFC107 35%, 
        #FF9800 50%, 
        #FF5722 65%, 
        #E91E63 80%, 
        #B71C1C 100%
    );
    border-radius: 7px;
    position: relative;
}

.gauge-marker {
    position: absolute;
    top: -6px;
    width: 4px;
    height: 26px;
    background: var(--text-main);
    border-radius: 2px;
    transform: translateX(-50%);
}

.gauge-marker::after {
    content: attr(data-label);
    position: absolute;
    bottom: -22px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.7rem;
    color: var(--text-muted);
    white-space: nowrap;
}

.gauge-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 0.3rem;
    font-size: 0.72rem;
    color: var(--text-light);
}

/* ─── Data Table ───────────────────────────────────────────────────── */
.data-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid var(--border);
}

.data-row:last-child {
    border-bottom: none;
}

.data-label {
    font-size: 0.88rem;
    color: var(--text-muted);
}

.data-value {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-main);
}

/* ─── Material Badge ───────────────────────────────────────────────── */
.mat-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(139, 168, 52, 0.08);
    color: var(--primary-dark);
    padding: 0.35rem 0.8rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 0.2rem;
}

/* ─── Comparison Grid ──────────────────────────────────────────────── */
.compare-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin: 1rem 0;
}

.compare-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1.2rem;
    text-align: center;
    transition: all 0.2s;
}

.compare-item:hover {
    border-color: var(--primary);
}

.compare-item.selected {
    border-color: var(--primary);
    box-shadow: 0 0 0 2px rgba(139, 168, 52, 0.25);
}

/* ─── Tabs Styling ─────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    border-bottom: 2px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
    padding: 0.6rem 1.2rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: rgba(139, 168, 52, 0.08);
}

/* ─── Selectbox / Inputs ───────────────────────────────────────────── */
.stSelectbox label, .stNumberInput label, .stRadio label {
    font-weight: 500 !important;
    color: var(--text-main) !important;
}

/* ─── Section Title ────────────────────────────────────────────────── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--text-main);
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--primary);
    display: inline-block;
}

/* ─── Footer ───────────────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    margin-top: 3rem;
    border-top: 1px solid var(--border);
    color: var(--text-light);
    font-size: 0.82rem;
}

.footer a {
    color: var(--primary);
    text-decoration: none;
}

/* ─── Streamlit overrides ──────────────────────────────────────────── */
div[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1rem;
}

div[data-testid="stMetric"] label {
    font-family: 'DM Sans', sans-serif !important;
}

.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    padding: 0.5rem 1.5rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: var(--primary-dark) !important;
    box-shadow: var(--shadow-md) !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

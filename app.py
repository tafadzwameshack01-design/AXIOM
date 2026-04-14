"""
╔══════════════════════════════════════════════════════════════════════╗
║     AXIOM ⚡ STRUCTURED INEFFICIENCY ENGINE v4.0                     ║
║  Multi-Line: OVER 0.5/1.5/2.5 · BTTS · Home Win · Away Win         ║
║  Dixon-Coles · Bayesian · Ensemble · Kelly Sizing · CLV Tracking    ║
║  75+ World Leagues · Full Self-Automation · Self-Learning AI        ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import sqlite3
import json
import pandas as pd
import numpy as np
import math
import os
import time
import hashlib
import difflib
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AXIOM ⚡ Inefficiency Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "AXIOM Structured Inefficiency Engine v4.0 — Dixon-Coles · Bayesian · Ensemble · CLV Tracking"},
)

# ═══════════════════════════════════════════════════════════════════════
#  CSS — Deep Space (v4 – axiom palette)
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@400;500&display=swap');

:root {
  --bg:       #020810;
  --surface:  #060e1a;
  --card:     #080f1e;
  --border:   #0d2040;
  --blue:     #00b4ff;
  --blue2:    #0066cc;
  --gold:     #ffb300;
  --gold2:    #ff8f00;
  --cyan:     #00e5ff;
  --green:    #39ff14;
  --red:      #ff1744;
  --purple:   #ea80fc;
  --orange:   #ff6d00;
  --text:     #c8dff5;
  --muted:    #3a5878;
}

html, body, .stApp { background: var(--bg) !important; font-family: 'Barlow', sans-serif; }

.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,180,255,0.018) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,180,255,0.018) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: gridMove 30s linear infinite;
  pointer-events: none; z-index: 0;
}
@keyframes gridMove { 100% { background-position: 60px 60px, 60px 60px; } }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; max-width: 1400px; position: relative; z-index: 1; }

/* ── Hero ─── */
.axiom-hero { text-align: center; padding: 22px 0 8px; }
.axiom-logo {
  font-family: 'Bebas Neue', cursive; font-size: 5.5rem; letter-spacing: 14px; line-height: 1;
  background: linear-gradient(135deg, #00b4ff 0%, #00e5ff 40%, #ffb300 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  animation: logoGlow 4s ease-in-out infinite;
}
@keyframes logoGlow {
  0%,100% { filter: drop-shadow(0 0 8px rgba(0,180,255,0.4)); }
  50%      { filter: drop-shadow(0 0 28px rgba(0,180,255,0.9)); }
}
.axiom-tagline { font-family:'Barlow Condensed',sans-serif; font-size:0.78rem; letter-spacing:4px; text-transform:uppercase; color:var(--muted); margin-top:4px; }
.axiom-version { font-family:'Barlow Condensed',sans-serif; font-size:0.66rem; letter-spacing:3px; text-transform:uppercase; color:var(--cyan); margin-top:2px; opacity:0.75; }
.axiom-bar { width:80px; height:2px; background:linear-gradient(90deg,transparent,var(--blue),transparent); margin:12px auto 0; animation:barPulse 2s ease-in-out infinite; }
@keyframes barPulse { 0%,100%{width:80px;opacity:.6;} 50%{width:200px;opacity:1;} }

/* ── Metrics ─── */
.metrics-row { display:flex; gap:10px; margin:14px 0; flex-wrap:wrap; }
.metric-box { flex:1; min-width:90px; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:12px 14px; text-align:center; transition:border-color .3s; }
.metric-box:hover { border-color:var(--blue); }
.metric-val { font-family:'Bebas Neue',cursive; font-size:2rem; color:var(--blue); line-height:1; display:block; }
.metric-val.gold   { color:var(--gold); }
.metric-val.cyan   { color:var(--cyan); }
.metric-val.purple { color:var(--purple); }
.metric-val.red    { color:var(--red); }
.metric-val.green  { color:var(--green); }
.metric-lbl { font-family:'Barlow Condensed',sans-serif; font-size:0.67rem; color:var(--muted); text-transform:uppercase; letter-spacing:1.5px; }

/* ── Scan line ─── */
.scan-line { font-family:'Barlow Condensed',sans-serif; font-size:0.78rem; color:var(--blue); letter-spacing:3px; text-transform:uppercase; text-align:center; padding:8px; animation:scanFade .9s ease-in-out infinite; }
@keyframes scanFade { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

/* ── Pick cards ─── */
.pick-card {
  background:var(--card); border:1px solid var(--border); border-radius:18px; padding:22px 26px; margin:14px 0;
  position:relative; overflow:hidden; opacity:0;
  animation:cardReveal .5s ease forwards; transition:transform .25s, box-shadow .25s;
}
.pick-card:hover { transform:translateY(-4px); box-shadow:0 14px 44px rgba(0,180,255,.14); }
.pick-card:nth-child(1){animation-delay:.04s} .pick-card:nth-child(2){animation-delay:.12s}
.pick-card:nth-child(3){animation-delay:.20s} .pick-card:nth-child(4){animation-delay:.28s}
.pick-card:nth-child(5){animation-delay:.36s} .pick-card:nth-child(6){animation-delay:.44s}
.pick-card:nth-child(7){animation-delay:.52s}
@keyframes cardReveal { from{opacity:0;transform:translateY(18px);} to{opacity:1;transform:translateY(0);} }

.pick-card.elite  { border-color:var(--gold);   background:linear-gradient(135deg,#080f1e 0%,#1a1400 100%); animation:cardReveal .5s ease forwards,eliteGlow 3s ease-in-out infinite; }
.pick-card.strong { border-color:var(--blue2); }
.pick-card.btts   { border-color:var(--purple); }
.pick-card.result { border-color:var(--cyan);   }
@keyframes eliteGlow { 0%,100%{box-shadow:0 0 16px rgba(255,179,0,.1);} 50%{box-shadow:0 0 44px rgba(255,179,0,.32);} }

.rank-badge { position:absolute; top:14px; right:20px; font-family:'Bebas Neue',cursive; font-size:4rem; line-height:1; color:rgba(0,180,255,.05); pointer-events:none; user-select:none; }

.card-league { font-family:'Barlow Condensed',sans-serif; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; color:var(--muted); margin-bottom:6px; }
.card-teams { font-family:'Bebas Neue',cursive; font-size:2rem; letter-spacing:3px; color:var(--text); line-height:1.1; margin-bottom:10px; }
.card-vs { color:var(--muted); font-size:1rem; padding:0 8px; }

.card-bet { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:1.5rem; letter-spacing:1px; margin-bottom:12px; }
.bet-over05  { color:var(--cyan);   }
.bet-over15  { color:var(--blue);   }
.bet-over25  { color:var(--gold);   }
.bet-btts    { color:var(--purple); }
.bet-home    { color:var(--green); }
.bet-away    { color:var(--orange); }

.conf-track { background:rgba(255,255,255,.06); border-radius:999px; height:6px; margin:8px 0 10px; overflow:hidden; }
.conf-fill  { height:100%; border-radius:999px; animation:fillBar 1.2s cubic-bezier(.22,1,.36,1) forwards; transform-origin:left; }
.conf-fill.elite  { background:linear-gradient(90deg,var(--gold2),var(--gold)); }
.conf-fill.strong { background:linear-gradient(90deg,var(--blue2),var(--blue)); }
.conf-fill.btts   { background:linear-gradient(90deg,#7b1fa2,var(--purple)); }
.conf-fill.result { background:linear-gradient(90deg,#006064,var(--cyan)); }
@keyframes fillBar { from{width:0 !important;} }

.conf-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }
.conf-pct { font-family:'Bebas Neue',cursive; font-size:1.6rem; letter-spacing:2px; }
.conf-pct.elite  { color:var(--gold); }
.conf-pct.strong { color:var(--blue); }
.conf-pct.btts   { color:var(--purple); }
.conf-pct.result { color:var(--cyan); }

.tier-chip { font-family:'Barlow Condensed',sans-serif; font-size:0.7rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; padding:3px 10px; border-radius:999px; }
.tier-chip.elite  { background:rgba(255,179,0,.15);  color:var(--gold);   border:1px solid rgba(255,179,0,.4); }
.tier-chip.strong { background:rgba(0,180,255,.1);   color:var(--blue);   border:1px solid rgba(0,180,255,.3); }
.tier-chip.btts   { background:rgba(234,128,252,.1); color:var(--purple); border:1px solid rgba(234,128,252,.3); }
.tier-chip.result { background:rgba(0,229,255,.1);   color:var(--cyan);   border:1px solid rgba(0,229,255,.3); }

.pills-row { display:flex; gap:6px; flex-wrap:wrap; margin-top:10px; }
.pill { font-family:'Barlow Condensed',sans-serif; font-size:0.73rem; letter-spacing:1px; padding:3px 9px; border-radius:6px; white-space:nowrap; }
.pill-time   { background:rgba(0,180,255,.08);  color:var(--blue);   border:1px solid rgba(0,180,255,.2); }
.pill-xg     { background:rgba(255,179,0,.08);  color:var(--gold);   border:1px solid rgba(255,179,0,.2); }
.pill-pois   { background:rgba(0,229,255,.08);  color:var(--cyan);   border:1px solid rgba(0,229,255,.2); }
.pill-btts   { background:rgba(41,182,246,.08); color:#29b6f6;       border:1px solid rgba(41,182,246,.2); }
.pill-form   { background:rgba(234,128,252,.08);color:var(--purple); border:1px solid rgba(234,128,252,.2); }
.pill-h2h    { background:rgba(255,64,64,.08);  color:#ff6464;       border:1px solid rgba(255,64,64,.2); }
.pill-learn  { background:rgba(0,200,83,.08);   color:#00c853;       border:1px solid rgba(0,200,83,.2); }
.pill-dc     { background:rgba(0,180,255,.08);  color:var(--cyan);   border:1px solid rgba(0,180,255,.3); }
.pill-regime { background:rgba(255,179,0,.08);  color:var(--gold);   border:1px solid rgba(255,179,0,.2); }
.pill-edge   { background:rgba(57,255,20,.08);  color:var(--green);  border:1px solid rgba(57,255,20,.2); }
.pill-abst   { background:rgba(255,23,68,.08);  color:var(--red);    border:1px solid rgba(255,23,68,.2); }

.ai-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-top:10px; }
.ai-factor { background:rgba(0,180,255,.04); border:1px solid rgba(0,180,255,.1); border-radius:8px; padding:6px 8px; text-align:center; }
.ai-factor-val { font-family:'Bebas Neue',cursive; font-size:1.1rem; color:var(--blue); display:block; line-height:1; }
.ai-factor-val.gold   { color:var(--gold); }
.ai-factor-val.cyan   { color:var(--cyan); }
.ai-factor-val.purple { color:var(--purple); }
.ai-factor-val.green  { color:var(--green); }
.ai-factor-val.red    { color:var(--red); }
.ai-factor-lbl { font-family:'Barlow Condensed',sans-serif; font-size:0.62rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; }

.card-reason { font-family:'Barlow',sans-serif; font-size:0.8rem; color:var(--muted); margin-top:10px; line-height:1.55; border-left:2px solid var(--border); padding-left:10px; }
.countdown { font-family:'Bebas Neue',cursive; font-size:0.85rem; letter-spacing:2px; color:var(--blue); }
.no-picks { text-align:center; padding:52px 24px; font-family:'Barlow Condensed',sans-serif; font-size:1.1rem; color:var(--muted); letter-spacing:2px; }
.no-picks-icon { font-size:3rem; display:block; margin-bottom:12px; }

/* ── DC Badge ─── */
.dc-badge {
  display:inline-block; background:rgba(0,180,255,.1); border:1px solid rgba(0,180,255,.3);
  border-radius:8px; padding:4px 10px; font-family:'Barlow Condensed',sans-serif;
  font-size:0.72rem; color:var(--blue); letter-spacing:2px; text-transform:uppercase;
}
.kelly-badge {
  display:inline-block; background:rgba(57,255,20,.1); border:1px solid rgba(57,255,20,.3);
  border-radius:8px; padding:4px 10px; font-family:'Barlow Condensed',sans-serif;
  font-size:0.72rem; color:var(--green); letter-spacing:2px; text-transform:uppercase;
}

hr { border-color:rgba(0,180,255,.08) !important; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface); border-radius:12px; padding:4px; gap:2px; border:1px solid var(--border); }
.stTabs [data-baseweb="tab"] { border-radius:8px; font-family:'Barlow Condensed',sans-serif; letter-spacing:1px; color:var(--muted); font-size:.9rem; }
.stTabs [aria-selected="true"] { background:rgba(0,180,255,.12) !important; color:var(--blue) !important; }

/* ── Live Match Cards ─── */
.live-pulse {
  display:inline-block; width:9px; height:9px; background:var(--red);
  border-radius:50%; margin-right:7px;
  animation:livePulse 1.1s ease-in-out infinite;
  box-shadow:0 0 0 0 rgba(255,23,68,.7);
}
@keyframes livePulse {
  0%  { transform:scale(1);   box-shadow:0 0 0 0   rgba(255,23,68,.7); }
  60% { transform:scale(1.15);box-shadow:0 0 0 8px rgba(255,23,68,0);  }
  100%{ transform:scale(1);   box-shadow:0 0 0 0   rgba(255,23,68,0);  }
}
.live-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }
.live-badge { font-family:'Barlow Condensed',sans-serif; font-size:0.72rem; font-weight:700; letter-spacing:3px; text-transform:uppercase; padding:3px 10px; border-radius:999px; background:rgba(255,23,68,.15); color:var(--red); border:1px solid rgba(255,23,68,.4); }
.live-clock { font-family:'Bebas Neue',cursive; font-size:1.1rem; letter-spacing:3px; color:var(--red); }
.live-score-block { display:flex; align-items:center; justify-content:center; gap:18px; padding:16px 0 12px; }
.live-team-name { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:1.05rem; letter-spacing:1px; text-transform:uppercase; color:var(--text); max-width:120px; text-align:center; word-break:break-word; }
.live-score { font-family:'Bebas Neue',cursive; font-size:3.8rem; letter-spacing:6px; color:var(--blue); line-height:1; text-shadow:0 0 20px rgba(0,180,255,.5); }
.live-sep { font-family:'Bebas Neue',cursive; font-size:2rem; color:var(--border); }
.live-card { background:var(--card); border:1px solid rgba(255,23,68,.25); border-radius:18px; padding:20px 24px; margin:14px 0; overflow:hidden; position:relative; animation:cardReveal .45s ease forwards; transition:transform .25s, box-shadow .25s; }
.live-card:hover { transform:translateY(-3px); box-shadow:0 12px 40px rgba(255,23,68,.12); }
.live-card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background:linear-gradient(90deg,transparent,var(--red),transparent); animation:scanLine 3s linear infinite; }
@keyframes scanLine { 0%{background-position:-200px 0;} 100%{background-position:200px 0;} }
.pred-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin:12px 0; }
.pred-cell { background:rgba(0,0,0,.3); border-radius:10px; padding:8px 6px; text-align:center; border:1px solid var(--border); transition:border-color .2s; }
.pred-cell.hit  { border-color:var(--green); background:rgba(57,255,20,.07); }
.pred-cell.live-edge { border-color:var(--gold); background:rgba(255,179,0,.07); }
.pred-val { font-family:'Bebas Neue',cursive; font-size:1.3rem; display:block; line-height:1; margin-bottom:2px; }
.pred-lbl { font-family:'Barlow Condensed',sans-serif; font-size:0.62rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; }
.live-reason { font-family:'Barlow',sans-serif; font-size:0.79rem; color:var(--muted); margin-top:10px; line-height:1.55; border-left:2px solid rgba(255,23,68,.3); padding-left:10px; }
.live-empty { text-align:center; padding:52px 24px; font-family:'Barlow Condensed',sans-serif; font-size:1rem; color:var(--muted); letter-spacing:2px; }
.halftime-chip { font-family:'Barlow Condensed',sans-serif; font-size:0.72rem; font-weight:700; letter-spacing:3px; padding:3px 10px; border-radius:999px; background:rgba(255,179,0,.15); color:var(--gold); border:1px solid rgba(255,179,0,.4); }

/* ── CLV Heatmap ─── */
.heatmap-cell { padding:6px 10px; border-radius:6px; text-align:center; font-family:'Barlow Condensed',sans-serif; font-size:0.8rem; letter-spacing:1px; }
.heatmap-pos { background:rgba(57,255,20,.15); color:var(--green); border:1px solid rgba(57,255,20,.3); }
.heatmap-neg { background:rgba(255,23,68,.1); color:var(--red); border:1px solid rgba(255,23,68,.2); }
.heatmap-neutral { background:rgba(255,255,255,.04); color:var(--muted); border:1px solid var(--border); }

/* ── Regime Badge ─── */
.regime-a { background:rgba(255,23,68,.12); color:var(--red); border:1px solid rgba(255,23,68,.3); padding:3px 10px; border-radius:999px; font-family:'Barlow Condensed',sans-serif; font-size:0.7rem; letter-spacing:2px; }
.regime-b { background:rgba(57,255,20,.12); color:var(--green); border:1px solid rgba(57,255,20,.3); padding:3px 10px; border-radius:999px; font-family:'Barlow Condensed',sans-serif; font-size:0.7rem; letter-spacing:2px; }
.regime-c { background:rgba(255,179,0,.12); color:var(--gold); border:1px solid rgba(255,179,0,.3); padding:3px 10px; border-radius:999px; font-family:'Barlow Condensed',sans-serif; font-size:0.7rem; letter-spacing:2px; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
#  MODULE-LEVEL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════
ESPN_SOCCER   = "https://site.api.espn.com/apis/site/v2/sports/soccer"
TSDB_BASE     = "https://www.thesportsdb.com/api/v1/json/3"
CAT_OFFSET    = timedelta(hours=2)
WINDOW_HOURS  = 24
MIN_GAMES     = 5
HISTORY_GAMES = 38
TOP_N         = 20
LEARNING_RATE = 0.004
MODEL_NAME    = "claude-sonnet-4-20250514"
MAX_TOKENS    = 2048

# Dixon-Coles rho correction range
DC_RHO = -0.04

# Kelly fraction parameters
KELLY_FRACTION    = 0.25
MAX_SINGLE_BET    = 0.03
MAX_DAILY_EXPOSURE = 0.15
DRAWDOWN_TRIGGER  = 0.20
DRAWDOWN_RECOVERY = 0.12
CONSERVATIVE_KELLY = 0.125

# AXIOM Score sigmoid weights (initial — learned quarterly)
AXIOM_SCORE_WEIGHTS = {
    "w0": -0.5,
    "w1": 2.5,   # edge_norm
    "w2": 0.8,   # log(calibration_confidence)
    "w3": 1.2,   # market_inefficiency
    "w4": 0.6,   # timing
    "w5": 0.4,   # liquidity
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "application/json",
}

BET_TYPES: Dict[str, Dict] = {
    "OVER_05":  {"label": "OVER 0.5 Goals",  "line": 0.5,  "gate": 88.0, "css": "over05",  "emoji": "⚡"},
    "OVER_15":  {"label": "OVER 1.5 Goals",  "line": 1.5,  "gate": 78.0, "css": "over15",  "emoji": "⚽"},
    "OVER_25":  {"label": "OVER 2.5 Goals",  "line": 2.5,  "gate": 65.0, "css": "over25",  "emoji": "🔥"},
    "BTTS_YES": {"label": "Both Teams Score", "line": None, "gate": 70.0, "css": "btts",    "emoji": "🎯"},
    "HOME_WIN": {"label": "Home Win",         "line": None, "gate": 74.0, "css": "home",    "emoji": "🏠"},
    "AWAY_WIN": {"label": "Away Win",         "line": None, "gate": 74.0, "css": "away",    "emoji": "✈️"},
}

DEFAULT_WEIGHTS: Dict[str, Dict[str, float]] = {
    "OVER_05": {
        "poisson_p": 0.50, "hist_rate": 0.20, "form": 0.10,
        "streak": 0.10, "btts": 0.05, "h2h": 0.05,
    },
    "OVER_15": {
        "poisson_p": 0.42, "hist_rate": 0.26, "xg_norm": 0.14,
        "form": 0.08, "btts": 0.05, "h2h": 0.05,
    },
    "OVER_25": {
        "poisson_p": 0.35, "hist_rate": 0.25, "xg_norm": 0.20,
        "btts": 0.10, "form": 0.05, "h2h": 0.05,
    },
    "BTTS_YES": {
        "poisson_btts": 0.40, "hist_btts": 0.35, "xg_balance": 0.10,
        "form": 0.10, "h2h": 0.05,
    },
    "HOME_WIN": {
        "poisson_hw": 0.45, "hist_hw": 0.25, "form_diff": 0.15,
        "xg_diff": 0.10, "h2h": 0.05,
    },
    "AWAY_WIN": {
        "poisson_aw": 0.45, "hist_aw": 0.25, "form_diff": 0.15,
        "xg_diff": 0.10, "h2h": 0.05,
    },
}

LEAGUES: List[Tuple[str, str, str]] = [
    ("eng.1","Premier League","🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("eng.2","Championship","🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("eng.3","League One","🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("eng.4","League Two","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("esp.1","La Liga","🇪🇸"), ("esp.2","Segunda División","🇪🇸"),
    ("ger.1","Bundesliga","🇩🇪"), ("ger.2","2. Bundesliga","🇩🇪"), ("ger.3","3. Liga","🇩🇪"),
    ("ita.1","Serie A","🇮🇹"), ("ita.2","Serie B","🇮🇹"),
    ("fra.1","Ligue 1","🇫🇷"), ("fra.2","Ligue 2","🇫🇷"),
    ("ned.1","Eredivisie","🇳🇱"), ("ned.2","Eerste Divisie","🇳🇱"),
    ("por.1","Primeira Liga","🇵🇹"), ("por.2","Liga Portugal 2","🇵🇹"),
    ("sco.1","Scottish Premiership","🏴󠁧󠁢󠁳󠁣󠁴󠁿"), ("sco.2","Scottish Championship","🏴󠁧󠁢󠁳󠁣󠁴󠁿"),
    ("tur.1","Süper Lig","🇹🇷"), ("tur.2","TFF First League","🇹🇷"),
    ("bel.1","Belgian Pro League","🇧🇪"), ("gre.1","Super League Greece","🇬🇷"),
    ("ukr.1","Ukrainian Premier","🇺🇦"), ("den.1","Superligaen","🇩🇰"),
    ("swe.1","Allsvenskan","🇸🇪"), ("nor.1","Eliteserien","🇳🇴"),
    ("aut.1","Austrian Bundesliga","🇦🇹"), ("sui.1","Swiss Super League","🇨🇭"),
    ("cze.1","Czech First League","🇨🇿"), ("pol.1","Ekstraklasa","🇵🇱"),
    ("rou.1","Liga 1 Romania","🇷🇴"), ("srb.1","Serbian SuperLiga","🇷🇸"),
    ("hun.1","OTP Bank Liga","🇭🇺"), ("bul.1","First Professional League","🇧🇬"),
    ("cro.1","HNL Croatia","🇭🇷"), ("svk.1","Fortuna Liga Slovakia","🇸🇰"),
    ("fin.1","Veikkausliiga","🇫🇮"), ("isr.1","Israeli Premier","🇮🇱"),
    ("rus.1","Russian Premier","🇷🇺"),
    ("usa.1","MLS","🇺🇸"), ("usa.2","USL Championship","🇺🇸"),
    ("mex.1","Liga MX","🇲🇽"), ("mex.2","Ascenso MX","🇲🇽"),
    ("bra.1","Brasileirão","🇧🇷"), ("bra.2","Série B","🇧🇷"),
    ("arg.1","Primera División","🇦🇷"), ("col.1","Liga Betplay","🇨🇴"),
    ("chi.1","Primera Chile","🇨🇱"), ("ecu.1","Liga Pro Ecuador","🇪🇨"),
    ("per.1","Liga 1 Peru","🇵🇪"), ("uru.1","Uruguay Primera","🇺🇾"),
    ("ven.1","Liga Futve","🇻🇪"), ("par.1","División Profesional","🇵🇾"),
    ("jpn.1","J1 League","🇯🇵"), ("jpn.2","J2 League","🇯🇵"),
    ("kor.1","K League 1","🇰🇷"), ("chn.1","Chinese Super League","🇨🇳"),
    ("aus.1","A-League","🇦🇺"), ("ind.1","Indian Super League","🇮🇳"),
    ("tha.1","Thai League 1","🇹🇭"), ("mys.1","Super League Malaysia","🇲🇾"),
    ("sau.1","Saudi Pro League","🇸🇦"), ("uae.1","UAE Pro League","🇦🇪"),
    ("egy.1","Egyptian Premier","🇪🇬"), ("rsa.1","PSL South Africa","🇿🇦"),
    ("mar.1","Botola Pro Morocco","🇲🇦"), ("nga.1","NPFL Nigeria","🇳🇬"),
    ("qat.1","Qatar Stars League","🇶🇦"),
    ("uefa.champions","Champions League","🏆"), ("uefa.europa","Europa League","🟠"),
    ("uefa.europaconference","Conference League","🟢"),
    ("conmebol.libertadores","Copa Libertadores","🏆"),
    ("concacaf.champions","CONCACAF Champions","🌎"),
]


# ═══════════════════════════════════════════════════════════════════════
#  SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════

def _init_session_state() -> None:
    """Initialize all session state keys before any logic runs."""
    defaults = {
        "bankroll": 1000.0,
        "peak_bankroll": 1000.0,
        "circuit_breaker_active": False,
        "current_regime": "B",
        "regime_last_updated": "",
        "clv_history": [],
        "bet_history": [],
        "daily_exposure": 0.0,
        "axiom_score_threshold": 0.55,
        "iteration_log": [],
        "stop_flag": False,
        "analysis_running": False,
        "axiom_insights": [],
        "inefficiency_heatmap": {},
        "parameter_drift_log": [],
        "structural_break_log": [],
        "last_scan_time": "",
        "scan_count": 0,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ═══════════════════════════════════════════════════════════════════════
#  DIXON-COLES CORE ENGINE
# ═══════════════════════════════════════════════════════════════════════

def _pois_pmf(k: int, lam: float) -> float:
    """Compute Poisson probability mass function P(X=k | lambda)."""
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    try:
        return (lam ** k) * math.exp(-lam) / math.factorial(k)
    except Exception:
        return 0.0


def _dc_correction(home_goals: int, away_goals: int, lam_h: float, lam_a: float, rho: float = DC_RHO) -> float:
    """
    Dixon-Coles low-score correction factor.
    Implements: rho-corrected bivariate Poisson for scores (0,0),(1,0),(0,1),(1,1).
    rho is bounded to (-0.1, 0.0) — do NOT treat as probability.
    """
    if home_goals == 0 and away_goals == 0:
        return 1.0 - rho * lam_h * lam_a
    if home_goals == 1 and away_goals == 0:
        return 1.0 + rho * lam_a
    if home_goals == 0 and away_goals == 1:
        return 1.0 + rho * lam_h
    if home_goals == 1 and away_goals == 1:
        return 1.0 - rho
    return 1.0


def dc_score_probability(h: int, a: int, lam_h: float, lam_a: float) -> float:
    """Compute P(home=h, away=a) using Dixon-Coles corrected bivariate Poisson."""
    lam_h = max(0.05, lam_h)
    lam_a = max(0.05, lam_a)
    tau   = _dc_correction(h, a, lam_h, lam_a)
    return tau * _pois_pmf(h, lam_h) * _pois_pmf(a, lam_a)


def dc_over_line(lam_h: float, lam_a: float, line: float) -> float:
    """
    P(total goals > line) using full Dixon-Coles scoreline distribution.
    More accurate than naive Poisson for low-score corrections.
    """
    p_under = 0.0
    for h in range(13):
        for a in range(13):
            if (h + a) <= line:
                p_under += dc_score_probability(h, a, lam_h, lam_a)
    return max(0.0, min(1.0, 1.0 - p_under))


def dc_btts(lam_h: float, lam_a: float) -> float:
    """P(home >= 1 AND away >= 1) using Dixon-Coles distribution."""
    p_no_btts = 0.0
    for h in range(13):
        for a in range(13):
            if h == 0 or a == 0:
                p_no_btts += dc_score_probability(h, a, lam_h, lam_a)
    return max(0.0, min(1.0, 1.0 - p_no_btts))


def dc_home_win(lam_h: float, lam_a: float) -> float:
    """P(home goals > away goals) via Dixon-Coles scoreline matrix."""
    p = 0.0
    for h in range(13):
        for a in range(13):
            if h > a:
                p += dc_score_probability(h, a, lam_h, lam_a)
    return max(0.0, min(1.0, p))


def dc_away_win(lam_h: float, lam_a: float) -> float:
    """P(away goals > home goals) via Dixon-Coles scoreline matrix."""
    p = 0.0
    for h in range(13):
        for a in range(13):
            if a > h:
                p += dc_score_probability(h, a, lam_h, lam_a)
    return max(0.0, min(1.0, p))


def poisson_over_line(lam_h: float, lam_a: float, line: float) -> float:
    """Legacy naive Poisson (kept for ensemble diversity)."""
    p_under = 0.0
    for h in range(13):
        for a in range(13):
            if (h + a) <= line:
                p_under += _pois_pmf(h, max(0.01, lam_h)) * _pois_pmf(a, max(0.01, lam_a))
    return max(0.0, min(1.0, 1.0 - p_under))


def poisson_btts(lam_h: float, lam_a: float) -> float:
    """Legacy naive Poisson BTTS (kept for ensemble)."""
    p0h = _pois_pmf(0, max(0.01, lam_h))
    p0a = _pois_pmf(0, max(0.01, lam_a))
    return max(0.0, min(1.0, (1 - p0h) * (1 - p0a)))


def poisson_home_win(lam_h: float, lam_a: float) -> float:
    """Legacy naive Poisson home win."""
    p = 0.0
    for h in range(13):
        for a in range(13):
            if h > a:
                p += _pois_pmf(h, max(0.01, lam_h)) * _pois_pmf(a, max(0.01, lam_a))
    return max(0.0, min(1.0, p))


def poisson_away_win(lam_h: float, lam_a: float) -> float:
    """Legacy naive Poisson away win."""
    p = 0.0
    for h in range(13):
        for a in range(13):
            if a > h:
                p += _pois_pmf(h, max(0.01, lam_h)) * _pois_pmf(a, max(0.01, lam_a))
    return max(0.0, min(1.0, p))


def safe_mean(lst: list) -> float:
    """Compute mean safely; returns 0.0 for empty list."""
    return float(np.mean(lst)) if lst else 0.0


# ═══════════════════════════════════════════════════════════════════════
#  DATABASE SCHEMA
# ═══════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_db() -> sqlite3.Connection:
    """Initialize AXIOM SQLite database with full schema."""
    conn = sqlite3.connect("axiom_v4.db", check_same_thread=False)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS api_cache (
            cache_key TEXT PRIMARY KEY, data TEXT, ts REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS picks_log (
            id           TEXT PRIMARY KEY,
            match        TEXT,
            league       TEXT,
            league_id    TEXT,
            bet          TEXT,
            bet_type     TEXT DEFAULT 'OVER_25',
            xg_total     REAL,
            confidence   REAL,
            dc_confidence REAL DEFAULT 0.0,
            edge         REAL DEFAULT 0.0,
            axiom_score  REAL DEFAULT 0.0,
            kelly_pct    REAL DEFAULT 0.0,
            regime       TEXT DEFAULT 'B',
            kickoff      TEXT,
            result       TEXT DEFAULT 'pending',
            home_score   INTEGER DEFAULT -1,
            away_score   INTEGER DEFAULT -1,
            factors_json TEXT DEFAULT '{}',
            clv          REAL DEFAULT 0.0,
            logged_at    TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS model_weights (
            bet_type TEXT,
            factor   TEXT,
            weight   REAL,
            wins     INTEGER DEFAULT 0,
            losses   INTEGER DEFAULT 0,
            updates  INTEGER DEFAULT 0,
            PRIMARY KEY (bet_type, factor)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS clv_log (
            id          TEXT PRIMARY KEY,
            match       TEXT,
            league      TEXT,
            bet_type    TEXT,
            entry_odds  REAL,
            closing_odds REAL,
            clv         REAL,
            hours_before REAL,
            logged_at   TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bankroll_log (
            id          TEXT PRIMARY KEY,
            event       TEXT,
            amount      REAL,
            bankroll    REAL,
            ts          TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS regime_log (
            id      TEXT PRIMARY KEY,
            regime  TEXT,
            reason  TEXT,
            ts      TEXT
        )
    """)

    # Auto-migrate older picks_log if needed
    migrations = [
        ("bet_type", "'OVER_25'"), ("home_score", "-1"), ("away_score", "-1"),
        ("factors_json", "'{}'"), ("dc_confidence", "0.0"), ("edge", "0.0"),
        ("axiom_score", "0.0"), ("kelly_pct", "0.0"), ("regime", "'B'"), ("clv", "0.0"),
    ]
    for col, defval in migrations:
        try:
            conn.execute(f"ALTER TABLE picks_log ADD COLUMN {col} TEXT DEFAULT {defval}")
        except Exception:
            pass

    conn.commit()
    _init_weights(conn)
    return conn


def _init_weights(conn: sqlite3.Connection) -> None:
    """Seed default adaptive weights if not yet stored."""
    for bet_type, factors in DEFAULT_WEIGHTS.items():
        for factor, w in factors.items():
            conn.execute(
                "INSERT OR IGNORE INTO model_weights (bet_type,factor,weight) VALUES (?,?,?)",
                (bet_type, factor, w)
            )
    conn.commit()


def get_weights(bet_type: str) -> Dict[str, float]:
    """Retrieve normalized adaptive factor weights for a bet type."""
    conn = get_db()
    rows = conn.execute(
        "SELECT factor, weight FROM model_weights WHERE bet_type=?", (bet_type,)
    ).fetchall()
    if not rows:
        return DEFAULT_WEIGHTS.get(bet_type, {})
    w = {r[0]: r[1] for r in rows}
    total = sum(w.values())
    if total > 0:
        w = {k: v / total for k, v in w.items()}
    return w


def update_weights(bet_type: str, factors: Dict[str, float], won: bool) -> None:
    """
    Online gradient weight update — asymmetric signal (learn more from wins).
    Enforces minimum floor of 0.02 per factor to prevent catastrophic forgetting.
    """
    conn = get_db()
    current = get_weights(bet_type)
    signal  = 1.0 if won else -0.5

    new_w: Dict[str, float] = {}
    for factor, val in factors.items():
        if factor not in current:
            continue
        contribution = val - 0.5
        delta = LEARNING_RATE * signal * contribution
        new_w[factor] = max(0.02, min(0.70, current[factor] + delta))

    total = sum(new_w.values())
    if total > 0:
        new_w = {k: v / total for k, v in new_w.items()}

    for factor, weight in new_w.items():
        result_col = "wins" if won else "losses"
        conn.execute(
            f"""UPDATE model_weights
                SET weight=?, {result_col}={result_col}+1, updates=updates+1
                WHERE bet_type=? AND factor=?""",
            (weight, bet_type, factor)
        )
    conn.commit()


# ─── Cache helpers ────────────────────────────────────────────────────

def cache_get(key: str, ttl: int) -> Optional[Any]:
    """Retrieve a cached API response if not expired."""
    try:
        conn = get_db()
        row = conn.execute("SELECT data, ts FROM api_cache WHERE cache_key=?", (key,)).fetchone()
        if row and (time.time() - row[1]) < ttl:
            return json.loads(row[0])
    except Exception:
        pass
    return None


def cache_set(key: str, data: Any) -> None:
    """Store an API response in the cache."""
    try:
        conn = get_db()
        conn.execute("INSERT OR REPLACE INTO api_cache VALUES (?,?,?)",
                     (key, json.dumps(data, default=str), time.time()))
        conn.commit()
    except Exception:
        pass


def save_pick(pick: Dict) -> None:
    """Persist a pick to the picks_log table."""
    try:
        pid = hashlib.md5(f"{pick['match']}{pick['kickoff_utc']}{pick['bet_type']}".encode()).hexdigest()[:12]
        conn = get_db()
        conn.execute("""
            INSERT OR IGNORE INTO picks_log
            (id,match,league,league_id,bet,bet_type,xg_total,confidence,dc_confidence,
             edge,axiom_score,kelly_pct,regime,kickoff,factors_json,logged_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            pid, pick["match"], pick["league"], pick.get("league_id", ""),
            pick["bet"], pick["bet_type"], pick["xg_total"], pick["confidence"],
            pick.get("dc_confidence", 0.0), pick.get("edge", 0.0),
            pick.get("axiom_score", 0.0), pick.get("kelly_pct", 0.0),
            pick.get("regime", "B"),
            pick["kickoff_utc"], json.dumps(pick.get("factors", {})),
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ))
        conn.commit()
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════
#  TIME HELPERS
# ═══════════════════════════════════════════════════════════════════════

def now_utc() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(timezone.utc)


def to_cat(utc_str: str) -> str:
    """Convert UTC string to CAT (UTC+2) display format."""
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return (dt + CAT_OFFSET).strftime("%d %b · %H:%M CAT")
    except Exception:
        return "—"


def parse_utc(utc_str: str) -> Optional[datetime]:
    """Parse a UTC ISO 8601 string to a timezone-aware datetime."""
    try:
        return datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    except Exception:
        return None


def in_window(utc_str: str) -> bool:
    """Check if kickoff is within the next WINDOW_HOURS."""
    dt = parse_utc(utc_str)
    if not dt:
        return False
    n = now_utc()
    return n <= dt <= n + timedelta(hours=WINDOW_HOURS)


def minutes_to_kickoff(utc_str: str) -> int:
    """Return minutes until kickoff (0 if in the past)."""
    dt = parse_utc(utc_str)
    if not dt:
        return 9999
    return max(0, int((dt - now_utc()).total_seconds() / 60))


# ═══════════════════════════════════════════════════════════════════════
#  KELLY CRITERION + BANKROLL ENGINE
# ═══════════════════════════════════════════════════════════════════════

def compute_kelly_stake(
    probability: float,
    decimal_odds: float,
    bankroll: float,
    epistemic_uncertainty: float = 0.05,
) -> Tuple[float, float, float]:
    """
    Compute fractional Kelly stake with epistemic uncertainty penalty.
    Returns (kelly_full, kelly_fractional, recommended_stake_pct).
    Hard limits: single bet <= MAX_SINGLE_BET, daily exposure <= MAX_DAILY_EXPOSURE.
    """
    if decimal_odds <= 1.0 or probability <= 0.0 or probability >= 1.0:
        return 0.0, 0.0, 0.0

    b = decimal_odds - 1.0
    q = 1.0 - probability
    kelly_full = (b * probability - q) / b

    if kelly_full <= 0:
        return kelly_full, 0.0, 0.0

    # Apply epistemic uncertainty penalty — high uncertainty reduces stake
    uncertainty_penalty = max(0.3, 1.0 - epistemic_uncertainty * 2)
    fraction = KELLY_FRACTION * uncertainty_penalty

    # Halve Kelly in conservative mode (circuit breaker)
    if st.session_state.get("circuit_breaker_active", False):
        fraction = CONSERVATIVE_KELLY * uncertainty_penalty

    kelly_frac = kelly_full * fraction
    stake_pct  = min(kelly_frac, MAX_SINGLE_BET)

    return round(kelly_full, 4), round(kelly_frac, 4), round(stake_pct, 4)


def check_circuit_breaker(bankroll: float, peak_bankroll: float) -> Tuple[bool, str]:
    """
    Check drawdown circuit breaker.
    Returns (is_active, reason).
    20% drawdown from peak triggers conservative mode.
    Recovery requires <= 12% drawdown AND 50 additional bets.
    """
    if peak_bankroll <= 0:
        return False, ""
    drawdown = (peak_bankroll - bankroll) / peak_bankroll
    if drawdown >= DRAWDOWN_TRIGGER:
        return True, f"Drawdown {drawdown*100:.1f}% from peak — conservative mode active"
    return False, ""


# ═══════════════════════════════════════════════════════════════════════
#  AXIOM SCORE (SIGMOID BOUNDED)
# ═══════════════════════════════════════════════════════════════════════

def compute_axiom_score(
    edge: float,
    calibration_confidence: float,
    market_inefficiency: float,
    timing_coefficient: float,
    liquidity_coefficient: float,
) -> float:
    """
    Compute AXIOM Score using sigmoid-bounded formulation.
    All inputs normalized to [-1, 1] before scoring.
    Output is always in (0, 1).
    """
    eps = 1e-6
    w   = AXIOM_SCORE_WEIGHTS

    # Normalize edge to [-1, 1] (edge can be negative — that's correct)
    edge_norm = max(-1.0, min(1.0, edge / 0.20))

    log_cal = math.log(max(eps, calibration_confidence))

    score_input = (
        w["w0"]
        + w["w1"] * edge_norm
        + w["w2"] * log_cal
        + w["w3"] * market_inefficiency
        + w["w4"] * timing_coefficient
        + w["w5"] * liquidity_coefficient
    )

    # Sigmoid: 1 / (1 + exp(-x))
    return 1.0 / (1.0 + math.exp(-score_input))


def compute_edge_and_score(
    axiom_prob: float,
    dc_prob: float,
    ensemble_prob: float,
    hours_to_kickoff: float,
    epistemic_uncertainty: float,
) -> Tuple[float, float, float, float]:
    """
    Compute edge against implied market probability and AXIOM score.
    Without live odds data, we use a simplified proxy model.
    Returns (edge, axiom_score, calibration_confidence, timing_coeff).
    """
    # Proxy: assume market implied probability = average(dc_prob, ensemble_prob) * 0.95 (vig)
    market_implied = min(0.99, ((dc_prob + ensemble_prob) / 2) * 0.95)
    edge = axiom_prob - market_implied

    # Calibration confidence decreases with epistemic uncertainty
    calibration_confidence = max(0.1, 1.0 - epistemic_uncertainty * 3)

    # Market inefficiency proxy: absolute deviation from consensus
    market_inefficiency = min(1.0, abs(edge) / 0.15)

    # Timing coefficient: decreases as kickoff approaches (lines sharpen)
    if hours_to_kickoff <= 0:
        timing_coeff = 0.5
    elif hours_to_kickoff >= 24:
        timing_coeff = 1.0
    elif hours_to_kickoff >= 6:
        timing_coeff = 0.85
    elif hours_to_kickoff >= 2:
        timing_coeff = 0.70
    else:
        timing_coeff = 0.55

    liquidity_coeff = 0.85  # default without live liquidity data

    axiom_score = compute_axiom_score(
        edge, calibration_confidence, market_inefficiency,
        timing_coeff, liquidity_coeff
    )

    return edge, axiom_score, calibration_confidence, timing_coeff


# ═══════════════════════════════════════════════════════════════════════
#  REGIME DETECTION (SIMPLIFIED HMM PROXY)
# ═══════════════════════════════════════════════════════════════════════

def detect_regime(clv_history: List[float]) -> Tuple[str, str]:
    """
    Detect current market regime from CLV history.
    Regime A: Efficient (CLV near zero).
    Regime B: Exploitable (positive CLV trend).
    Regime C: Unstable (high CLV variance).
    Returns (regime_code, description).
    """
    if len(clv_history) < 10:
        return "B", "Insufficient CLV history — defaulting to Exploitable regime"

    recent = clv_history[-20:]
    mean_clv  = float(np.mean(recent))
    std_clv   = float(np.std(recent))
    cv = std_clv / (abs(mean_clv) + 1e-6)

    if cv > 3.0:
        return "C", f"High CLV variance (CV={cv:.2f}) — Unstable regime — abstaining large bets"
    if mean_clv > 0.015:
        return "B", f"Positive CLV trend ({mean_clv:.3f}) — Exploitable regime"
    return "A", f"CLV near zero ({mean_clv:.3f}) — Efficient regime — raising thresholds"


def get_regime_threshold_multiplier(regime: str) -> float:
    """
    Returns confidence gate multiplier by regime.
    Regime A: raise threshold by 0.5% (return 1.05).
    Regime B: standard (return 1.0).
    Regime C: effectively block most bets (return 1.15).
    """
    return {"A": 1.05, "B": 1.0, "C": 1.15}.get(regime, 1.0)


# ═══════════════════════════════════════════════════════════════════════
#  API HELPERS
# ═══════════════════════════════════════════════════════════════════════

def safe_get(url: str, params: Dict = None, timeout: int = 10) -> Optional[Dict]:
    """Safe HTTP GET with error suppression."""
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def _parse_score(raw: Any) -> int:
    """Parse a score value from various ESPN API response formats."""
    if raw is None:
        return 0
    if isinstance(raw, dict):
        raw = raw.get("value", raw.get("displayValue", 0))
    try:
        return int(float(str(raw)))
    except (ValueError, TypeError):
        return 0


# ═══════════════════════════════════════════════════════════════════════
#  ESPN + TSDB DATA FETCHERS
# ═══════════════════════════════════════════════════════════════════════

def fetch_scoreboard(league_id: str) -> List[Dict]:
    """Fetch upcoming fixtures from ESPN for the next 2 days."""
    result = []
    for delta in [0, 1]:
        date_str = (now_utc() + timedelta(days=delta)).strftime("%Y%m%d")
        key = f"sb_{league_id}_{date_str}"
        cached = cache_get(key, ttl=300)
        if cached is not None:
            result.extend(cached)
            continue
        data = safe_get(f"{ESPN_SOCCER}/{league_id}/scoreboard", params={"dates": date_str})
        if not data:
            continue
        events = []
        for ev in data.get("events", []):
            comps = ev.get("competitions", [])
            if not comps:
                continue
            comp = comps[0]
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
            away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
            status_type = comp.get("status", {}).get("type", {})
            events.append({
                "event_id":  ev.get("id", ""),
                "date":      ev.get("date", ""),
                "home_id":   str(home_c.get("team", {}).get("id", "")),
                "home_name": home_c.get("team", {}).get("displayName", ""),
                "away_id":   str(away_c.get("team", {}).get("id", "")),
                "away_name": away_c.get("team", {}).get("displayName", ""),
                "status":    status_type.get("name", ""),
                "completed": status_type.get("completed", False),
                "league_id": league_id,
            })
        cache_set(key, events)
        result.extend(events)
    return result


def fetch_team_schedule_espn(league_id: str, team_id: str) -> List[Dict]:
    """Fetch completed match history for a team from ESPN."""
    date_tag = now_utc().strftime("%Y%m%d")
    key = f"sched_{league_id}_{team_id}_{date_tag}"
    cached = cache_get(key, ttl=3600)
    if cached is not None:
        return cached

    data = safe_get(f"{ESPN_SOCCER}/{league_id}/teams/{team_id}/schedule")
    if not data:
        return []

    games = []
    for ev in data.get("events", []):
        comps = ev.get("competitions", [])
        if not comps:
            continue
        comp = comps[0]
        if not comp.get("status", {}).get("type", {}).get("completed", False):
            continue
        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue
        home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
        hs  = _parse_score(home_c.get("score"))
        as_ = _parse_score(away_c.get("score"))
        games.append({
            "date":       ev.get("date", ""),
            "home_name":  home_c.get("team", {}).get("displayName", ""),
            "away_name":  away_c.get("team", {}).get("displayName", ""),
            "home_score": hs,
            "away_score": as_,
            "total":      hs + as_,
        })

    games.sort(key=lambda g: g["date"])
    games = games[-HISTORY_GAMES:]
    cache_set(key, games)
    return games


def fetch_tsdb_team_last15(team_name: str) -> List[Dict]:
    """Fetch last 15 results from TheSportsDB as supplementary data."""
    key = f"tsdb_{hashlib.md5(team_name.encode()).hexdigest()[:8]}"
    cached = cache_get(key, ttl=7200)
    if cached is not None:
        return cached

    sr = safe_get(f"{TSDB_BASE}/searchteams.php", params={"t": team_name}, timeout=6)
    if not sr or not sr.get("teams"):
        return []
    team_id = sr["teams"][0].get("idTeam", "")
    if not team_id:
        return []

    er = safe_get(f"{TSDB_BASE}/eventslast15.php", params={"id": team_id}, timeout=6)
    if not er or not er.get("results"):
        return []

    games = []
    for ev in er["results"]:
        try:
            hs  = int(ev.get("intHomeScore", 0) or 0)
            as_ = int(ev.get("intAwayScore", 0) or 0)
            home = ev.get("strHomeTeam", "")
            away = ev.get("strAwayTeam", "")
            date = ev.get("dateEvent", "")
            if not home or not away:
                continue
            games.append({
                "date": date, "home_name": home, "away_name": away,
                "home_score": hs, "away_score": as_, "total": hs + as_,
            })
        except Exception:
            pass

    cache_set(key, games)
    return games


def fetch_team_schedule(league_id: str, team_id: str, team_name: str) -> List[Dict]:
    """Multi-API team history: ESPN primary, TSDB supplement if thin."""
    espn_games = fetch_team_schedule_espn(league_id, team_id)
    if len(espn_games) >= MIN_GAMES:
        return espn_games

    tsdb_games = fetch_tsdb_team_last15(team_name)
    if not tsdb_games:
        return espn_games

    seen = set()
    combined = []
    for g in espn_games + tsdb_games:
        k = f"{g['date'][:10]}_{g.get('home_name','')}_{g.get('away_name','')}"
        if k not in seen:
            seen.add(k)
            combined.append(g)

    combined.sort(key=lambda g: g.get("date", ""))
    return combined[-HISTORY_GAMES:]


# ═══════════════════════════════════════════════════════════════════════
#  STATISTICS ENGINE
# ═══════════════════════════════════════════════════════════════════════

def team_stats(games: List[Dict], team_name: str) -> Optional[Dict]:
    """
    Compute comprehensive team statistics from historical matches.
    Returns None if fewer than MIN_GAMES completed matches available.
    """
    completed = [
        g for g in games
        if g.get("total", 0) >= 0
        and (g.get("home_score", -1) >= 0 or g.get("away_score", -1) >= 0)
    ]
    if len(completed) < MIN_GAMES:
        return None

    home_games = [g for g in completed if g.get("home_name", "") == team_name]
    away_games = [g for g in completed if g.get("away_name", "") == team_name]

    def _split_stats(gl: List[Dict], scored_key: str, conceded_key: str):
        if not gl:
            return None, None, None, None
        sc  = [g[scored_key]   for g in gl]
        co  = [g[conceded_key] for g in gl]
        tot = [s + c for s, c in zip(sc, co)]
        n   = len(gl)
        return (
            safe_mean(sc),
            safe_mean(co),
            sum(1 for t in tot if t > 0.5) / n,
            sum(1 for s, c in zip(sc, co) if s > 0 and c > 0) / n,
        )

    h_sc, h_co, h_over05, h_btts = _split_stats(home_games, "home_score", "away_score")
    a_sc, a_co, a_over05, a_btts = _split_stats(away_games, "away_score", "home_score")

    all_sc, all_co, all_tot = [], [], []
    for g in completed:
        is_home = g.get("home_name", "") == team_name
        sc  = g["home_score"] if is_home else g["away_score"]
        co  = g["away_score"] if is_home else g["home_score"]
        all_sc.append(sc)
        all_co.append(co)
        all_tot.append(sc + co)

    n = len(completed)
    avg_sc  = safe_mean(all_sc)
    avg_co  = safe_mean(all_co)
    avg_tot = safe_mean(all_tot)

    over05_r = sum(1 for t in all_tot if t > 0.5) / n
    over15_r = sum(1 for t in all_tot if t > 1.5) / n
    over25_r = sum(1 for t in all_tot if t > 2.5) / n
    btts_r   = sum(1 for s, c in zip(all_sc, all_co) if s > 0 and c > 0) / n
    cs_r     = sum(1 for c in all_co if c == 0) / n
    wins_r   = sum(1 for s, c in zip(all_sc, all_co) if s > c) / n

    recent5   = all_tot[-5:] if n >= 5 else all_tot
    older     = all_tot[:-5] if n > 5 else all_tot
    form_score = max(0.0, min(1.0, 0.5 + (safe_mean(recent5) - safe_mean(older)) / 4.0))
    last3_avg  = safe_mean(all_tot[-3:]) if n >= 3 else avg_tot

    streak_over05 = streak_over15 = streak_over25 = streak_btts = 0
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        if s + c > 0.5: streak_over05 += 1
        else: break
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        if s + c > 1.5: streak_over15 += 1
        else: break
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        if s + c > 2.5: streak_over25 += 1
        else: break
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        if s > 0 and c > 0: streak_btts += 1
        else: break

    return {
        "n": n, "n_home": len(home_games), "n_away": len(away_games),
        "avg_scored": avg_sc, "avg_conceded": avg_co, "avg_total": avg_tot,
        "over05_rate": over05_r, "over15_rate": over15_r, "over25_rate": over25_r,
        "btts_rate": btts_r, "cs_rate": cs_r, "wins_rate": wins_r,
        "home_avg_scored": h_sc if h_sc is not None else avg_sc,
        "home_avg_conceded": h_co if h_co is not None else avg_co,
        "home_over05_rate": h_over05 if h_over05 is not None else over05_r,
        "home_btts_rate": h_btts if h_btts is not None else btts_r,
        "away_avg_scored": a_sc if a_sc is not None else avg_sc,
        "away_avg_conceded": a_co if a_co is not None else avg_co,
        "away_over05_rate": a_over05 if a_over05 is not None else over05_r,
        "away_btts_rate": a_btts if a_btts is not None else btts_r,
        "form_score": form_score, "last3_avg": last3_avg,
        "streak_over05": streak_over05, "streak_over15": streak_over15,
        "streak_over25": streak_over25, "streak_btts": streak_btts,
    }


def get_h2h_stats(
    home_sched: List[Dict],
    away_sched: List[Dict],
    home_name: str,
    away_name: str,
) -> Optional[Dict]:
    """Extract head-to-head statistics. Returns None if fewer than 3 meetings."""
    seen, totals, home_wins, away_wins, bttss = set(), [], [], [], []
    for g in home_sched + away_sched:
        gk = f"{g.get('date','')[:10]}_{g.get('home_name','')}_{g.get('away_name','')}"
        if gk in seen:
            continue
        seen.add(gk)
        names = {g.get("home_name", ""), g.get("away_name", "")}
        if {home_name, away_name} != names:
            continue
        hs, as_ = g.get("home_score", 0), g.get("away_score", 0)
        t = hs + as_
        totals.append(t)
        home_wins.append(1 if hs > as_ else 0)
        away_wins.append(1 if as_ > hs else 0)
        bttss.append(1 if hs > 0 and as_ > 0 else 0)

    if len(totals) < 3:
        return None
    n = len(totals)
    return {
        "over05": sum(1 for t in totals if t > 0.5) / n,
        "over15": sum(1 for t in totals if t > 1.5) / n,
        "over25": sum(1 for t in totals if t > 2.5) / n,
        "btts":   sum(bttss) / n,
        "home_w": sum(home_wins) / n,
        "away_w": sum(away_wins) / n,
        "count":  n,
    }


# ═══════════════════════════════════════════════════════════════════════
#  GOAL RATE ESTIMATION (EXTENDED DIXON-COLES)
# ═══════════════════════════════════════════════════════════════════════

def _xg(home_st: Dict, away_st: Dict) -> Tuple[float, float]:
    """
    Compute expected goal rates using venue-split Dixon-Coles approach.
    Home: 55% own scoring * 45% opponent defensive weakness.
    Away: 55% own scoring * 45% opponent defensive weakness.
    """
    xg_h = 0.55 * home_st["home_avg_scored"] + 0.45 * away_st["away_avg_conceded"]
    xg_a = 0.55 * away_st["away_avg_scored"] + 0.45 * home_st["home_avg_conceded"]
    return max(0.05, xg_h), max(0.05, xg_a)


def compute_epistemic_uncertainty(
    home_n: int,
    away_n: int,
    is_cold_start: bool = False,
) -> float:
    """
    Estimate epistemic uncertainty from sample size.
    Smaller samples → higher uncertainty → larger Kelly penalty.
    Cold-start teams receive additional uncertainty bonus.
    """
    base = 1.0 / math.sqrt(max(1, (home_n + away_n) / 2))
    if is_cold_start:
        base = min(0.9, base * 1.5)
    return round(min(0.95, max(0.01, base)), 3)


# ═══════════════════════════════════════════════════════════════════════
#  CONFIDENCE ENGINES — ENSEMBLE (Dixon-Coles + Poisson + Historical)
# ═══════════════════════════════════════════════════════════════════════

def compute_over_confidence(
    home_st: Dict,
    away_st: Dict,
    line: float,
    h2h: Optional[Dict],
    bet_type: str,
) -> Tuple[float, float, float, Dict[str, float], str]:
    """
    Compute ensemble confidence for OVER X.X goals.
    Combines Dixon-Coles (primary), naive Poisson (diversity), and historical rates.
    Returns (ensemble_confidence%, dc_confidence%, epistemic_uncertainty, factors, reasoning).
    """
    xg_h, xg_a = _xg(home_st, away_st)
    total_xg   = xg_h + xg_a

    # Dixon-Coles primary probability
    dc_p   = dc_over_line(xg_h, xg_a, line)
    # Naive Poisson for ensemble diversity
    pois_p = poisson_over_line(xg_h, xg_a, line)

    rate_key = {0.5: "over05_rate", 1.5: "over15_rate", 2.5: "over25_rate"}.get(line, "over25_rate")
    hist_combined = (
        home_st.get(rate_key if line > 0.5 else "over05_rate", home_st["over05_rate"]) * 0.5 +
        away_st.get(rate_key if line > 0.5 else "over05_rate", away_st["over05_rate"]) * 0.5
    )

    xg_min = {0.5: 0.3, 1.5: 0.8, 2.5: 1.5}.get(line, 1.5)
    xg_max = {0.5: 2.0, 1.5: 3.5, 2.5: 5.0}.get(line, 5.0)
    xg_norm = max(0.0, min(1.0, (total_xg - xg_min) / (xg_max - xg_min)))

    btts_combined = (home_st["home_btts_rate"] + away_st["away_btts_rate"]) / 2
    form_combined = (home_st["form_score"] + away_st["form_score"]) / 2

    streak_key = {0.5: "streak_over05", 1.5: "streak_over15", 2.5: "streak_over25"}.get(line, "streak_over25")
    streak_val = (
        min(1.0, home_st.get(streak_key, 0) / 5.0) +
        min(1.0, away_st.get(streak_key, 0) / 5.0)
    ) / 2

    h2h_key = {0.5: "over05", 1.5: "over15", 2.5: "over25"}.get(line, "over25")
    h2h_val = h2h[h2h_key] if h2h else hist_combined

    # Ensemble: DC gets higher weight than naive Poisson
    ensemble_p = 0.55 * dc_p + 0.25 * pois_p + 0.20 * hist_combined

    factors = {
        "poisson_p": ensemble_p,
        "hist_rate": hist_combined,
        "xg_norm":   xg_norm,
        "form":      form_combined,
        "btts":      btts_combined,
        "streak":    streak_val,
        "h2h":       h2h_val,
    }

    weights    = get_weights(bet_type)
    confidence = sum(factors.get(k, 0.5) * w for k, w in weights.items()) * 100
    confidence = max(0.0, min(99.9, confidence))
    dc_conf    = dc_p * 100

    epistemic_unc = compute_epistemic_uncertainty(home_st["n"], away_st["n"])

    reasoning = (
        f"DC P(OVER {line}): {dc_p*100:.1f}% · Poisson: {pois_p*100:.1f}% · "
        f"xG {xg_h:.2f}+{xg_a:.2f}={total_xg:.2f} · "
        f"Hist OVER {line}: {hist_combined*100:.0f}% · BTTS: {btts_combined*100:.0f}%"
    )
    if home_st.get(streak_key, 0) >= 3:
        reasoning += f" · Home {home_st[streak_key]}-game streak 🔥"
    if away_st.get(streak_key, 0) >= 3:
        reasoning += f" · Away {away_st[streak_key]}-game streak 🔥"
    if h2h:
        reasoning += f" · H2H({h2h['count']}g) OVER {line}: {h2h[h2h_key]*100:.0f}%"

    return round(confidence, 1), round(dc_conf, 1), epistemic_unc, factors, reasoning


def compute_btts_confidence(
    home_st: Dict,
    away_st: Dict,
    h2h: Optional[Dict],
) -> Tuple[float, float, float, Dict[str, float], str]:
    """
    Compute ensemble BTTS confidence using Dixon-Coles + Poisson + historical rates.
    Returns (confidence%, dc_confidence%, epistemic_uncertainty, factors, reasoning).
    """
    xg_h, xg_a = _xg(home_st, away_st)

    dc_btts_p   = dc_btts(xg_h, xg_a)
    pois_btts_p = poisson_btts(xg_h, xg_a)
    hist_btts   = (home_st["home_btts_rate"] + away_st["away_btts_rate"]) / 2
    xg_balance  = min(xg_h, xg_a) / max(xg_h, xg_a) if max(xg_h, xg_a) > 0 else 0.5
    form_comb   = (home_st["form_score"] + away_st["form_score"]) / 2
    h2h_btts    = h2h["btts"] if h2h else hist_btts

    ensemble_p = 0.55 * dc_btts_p + 0.25 * pois_btts_p + 0.20 * hist_btts

    factors = {
        "poisson_btts": ensemble_p,
        "hist_btts":    hist_btts,
        "xg_balance":   xg_balance,
        "form":         form_comb,
        "h2h":          h2h_btts,
    }

    weights    = get_weights("BTTS_YES")
    confidence = sum(factors.get(k, 0.5) * w for k, w in weights.items()) * 100
    confidence = max(0.0, min(99.9, confidence))
    dc_conf    = dc_btts_p * 100
    epistemic_unc = compute_epistemic_uncertainty(home_st["n"], away_st["n"])

    reasoning = (
        f"DC BTTS: {dc_btts_p*100:.1f}% · Poisson BTTS: {pois_btts_p*100:.1f}% · "
        f"Hist BTTS: {hist_btts*100:.0f}% · "
        f"xG balance: {xg_balance:.2f} · xG {xg_h:.2f} vs {xg_a:.2f}"
    )
    if h2h:
        reasoning += f" · H2H BTTS: {h2h['btts']*100:.0f}%"

    return round(confidence, 1), round(dc_conf, 1), epistemic_unc, factors, reasoning


def compute_result_confidence(
    home_st: Dict,
    away_st: Dict,
    h2h: Optional[Dict],
    side: str,
) -> Tuple[float, float, float, Dict[str, float], str]:
    """
    Compute ensemble result (HOME/AWAY) confidence using DC + Poisson + historical.
    Returns (confidence%, dc_confidence%, epistemic_uncertainty, factors, reasoning).
    """
    xg_h, xg_a = _xg(home_st, away_st)

    if side == "HOME":
        dc_p      = dc_home_win(xg_h, xg_a)
        pois_p    = poisson_home_win(xg_h, xg_a)
        hist_rate = home_st["wins_rate"] * 0.6 + (1 - away_st["wins_rate"]) * 0.4
        form_diff = max(0.0, min(1.0, 0.5 + (home_st["form_score"] - away_st["form_score"]) / 2))
        xg_diff   = max(0.0, min(1.0, (xg_h - xg_a + 3) / 6))
        h2h_val   = h2h["home_w"] if h2h else hist_rate
        bt        = "HOME_WIN"
    else:
        dc_p      = dc_away_win(xg_h, xg_a)
        pois_p    = poisson_away_win(xg_h, xg_a)
        hist_rate = away_st["wins_rate"] * 0.6 + (1 - home_st["wins_rate"]) * 0.4
        form_diff = max(0.0, min(1.0, 0.5 + (away_st["form_score"] - home_st["form_score"]) / 2))
        xg_diff   = max(0.0, min(1.0, (xg_a - xg_h + 3) / 6))
        h2h_val   = h2h["away_w"] if h2h else hist_rate
        bt        = "AWAY_WIN"

    ensemble_p = 0.55 * dc_p + 0.25 * pois_p + 0.20 * hist_rate

    prefix = "hw" if side == "HOME" else "aw"
    factors = {
        f"poisson_{prefix}": ensemble_p,
        f"hist_{prefix}":    hist_rate,
        "form_diff":         form_diff,
        "xg_diff":           xg_diff,
        "h2h":               h2h_val,
    }

    weights    = get_weights(bt)
    confidence = sum(factors.get(k, 0.5) * w for k, w in weights.items()) * 100
    confidence = max(0.0, min(99.9, confidence))
    dc_conf    = dc_p * 100
    epistemic_unc = compute_epistemic_uncertainty(home_st["n"], away_st["n"])

    dom_st   = home_st if side == "HOME" else away_st
    lbl      = "Home" if side == "HOME" else "Away"
    reasoning = (
        f"DC {lbl} Win: {dc_p*100:.1f}% · Poisson: {pois_p*100:.1f}% · "
        f"Hist Win: {hist_rate*100:.0f}% · xG {xg_h:.2f} vs {xg_a:.2f} · "
        f"Form {lbl}: {dom_st['form_score']:.2f}"
    )
    if h2h:
        hw_key = "home_w" if side == "HOME" else "away_w"
        reasoning += f" · H2H Win: {h2h[hw_key]*100:.0f}%"

    return round(confidence, 1), round(dc_conf, 1), epistemic_unc, factors, reasoning


# ═══════════════════════════════════════════════════════════════════════
#  TIER + CARD HELPERS
# ═══════════════════════════════════════════════════════════════════════

def get_card_tier(conf: float, bet_type: str) -> Tuple[str, str]:
    """Determine display tier and label from confidence and bet type."""
    if bet_type in ("BTTS_YES",):
        if conf >= 80: return "elite", "🎯 ELITE BTTS"
        if conf >= 70: return "btts", "🎯 BTTS LOCK"
        return "btts", "🎯 BTTS"
    if bet_type in ("HOME_WIN", "AWAY_WIN"):
        emoji = "🏠" if bet_type == "HOME_WIN" else "✈️"
        if conf >= 82: return "elite", f"{emoji} ELITE"
        if conf >= 74: return "result", f"{emoji} STRONG"
        return "result", "RESULT"
    if conf >= 80: return "elite",  "🔥 ELITE"
    if conf >= 70: return "strong", "⚡ STRONG"
    return "strong", "✅ CONFIDENT"


def _form_label(score: float) -> str:
    """Return form label emoji for display."""
    if score >= 0.65: return "🔥 HOT"
    if score <= 0.35: return "❄️ COLD"
    return "➡️ STABLE"


def _regime_pill(regime: str) -> str:
    """Return regime HTML pill."""
    labels = {"A": "🔴 REGIME A: EFFICIENT", "B": "🟢 REGIME B: EDGE", "C": "⚠️ REGIME C: UNSTABLE"}
    css    = {"A": "regime-a", "B": "regime-b", "C": "regime-c"}
    return f'<span class="{css.get(regime, "regime-b")}">{labels.get(regime, "REGIME B")}</span>'


# ═══════════════════════════════════════════════════════════════════════
#  AXIOM MULTI-BET SCANNER
# ═══════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=300, show_spinner=False)
def scan_all_leagues() -> Tuple[List[Dict], int, int, int]:
    """
    Scan all 75+ leagues for picks meeting confidence and AXIOM score thresholds.
    Returns (top_picks, leagues_hit, games_eval, data_points).
    """
    candidates: List[Dict] = []
    leagues_hit = games_eval = data_pts = 0

    regime          = st.session_state.get("current_regime", "B")
    regime_mult     = get_regime_threshold_multiplier(regime)
    circuit_breaker = st.session_state.get("circuit_breaker_active", False)
    bankroll        = st.session_state.get("bankroll", 1000.0)
    peak            = st.session_state.get("peak_bankroll", 1000.0)

    for league_id, league_name, flag in LEAGUES:
        events = fetch_scoreboard(league_id)
        if not events:
            continue

        window_games = [
            e for e in events
            if not e.get("completed", False) and in_window(e.get("date", ""))
        ]
        if not window_games:
            continue

        leagues_hit += 1

        for ev in window_games:
            home_sched = fetch_team_schedule(league_id, ev["home_id"], ev["home_name"])
            away_sched = fetch_team_schedule(league_id, ev["away_id"], ev["away_name"])
            data_pts  += len(home_sched) + len(away_sched)

            home_st = team_stats(home_sched, ev["home_name"])
            away_st = team_stats(away_sched, ev["away_name"])
            if home_st is None or away_st is None:
                continue

            games_eval += 1
            h2h = get_h2h_stats(home_sched, away_sched, ev["home_name"], ev["away_name"])
            xg_h, xg_a = _xg(home_st, away_st)
            total_xg   = round(xg_h + xg_a, 2)
            mins_away  = minutes_to_kickoff(ev["date"])
            hours_away = mins_away / 60.0

            base = {
                "match":       f"{ev['home_name']} vs {ev['away_name']}",
                "home":        ev["home_name"],
                "away":        ev["away_name"],
                "league":      f"{flag} {league_name}",
                "league_id":   league_id,
                "kickoff_utc": ev["date"],
                "kickoff_cat": to_cat(ev["date"]),
                "mins_away":   mins_away,
                "xg_total":    total_xg,
                "xg_home":     round(xg_h, 2),
                "xg_away":     round(xg_a, 2),
                "home_n":      home_st["n"],
                "away_n":      away_st["n"],
                "home_form":   home_st["form_score"],
                "away_form":   away_st["form_score"],
                "home_btts":   round(home_st["home_btts_rate"] * 100),
                "away_btts":   round(away_st["away_btts_rate"] * 100),
                "h2h_count":   h2h["count"] if h2h else 0,
                "regime":      regime,
            }

            for bet_type, bt_meta in BET_TYPES.items():
                gate         = bt_meta["gate"] * regime_mult
                in_circ      = circuit_breaker
                effective_gate = gate * (1.15 if in_circ else 1.0)

                if bet_type in ("OVER_05", "OVER_15", "OVER_25"):
                    line = bt_meta["line"]
                    conf, dc_conf, epi_unc, factors, reasoning = compute_over_confidence(
                        home_st, away_st, line, h2h, bet_type
                    )
                    extra = {
                        "poisson_p":  round(dc_conf / 100, 4),
                        "over_rate":  round(home_st.get(
                            "over05_rate" if line == 0.5 else
                            "over15_rate" if line == 1.5 else "over25_rate", 0
                        ) * 100),
                        "streak_val": home_st.get(
                            "streak_over05" if line == 0.5 else
                            "streak_over15" if line == 1.5 else "streak_over25", 0
                        ),
                    }
                elif bet_type == "BTTS_YES":
                    conf, dc_conf, epi_unc, factors, reasoning = compute_btts_confidence(
                        home_st, away_st, h2h
                    )
                    extra = {
                        "poisson_p":  round(dc_conf / 100, 4),
                        "btts_hist":  round((home_st["home_btts_rate"] + away_st["away_btts_rate"]) / 2 * 100),
                    }
                elif bet_type in ("HOME_WIN", "AWAY_WIN"):
                    side = "HOME" if bet_type == "HOME_WIN" else "AWAY"
                    conf, dc_conf, epi_unc, factors, reasoning = compute_result_confidence(
                        home_st, away_st, h2h, side
                    )
                    extra = {
                        "poisson_p":  round(dc_conf / 100, 4),
                        "win_hist":   round((home_st["wins_rate"] if side == "HOME"
                                             else away_st["wins_rate"]) * 100),
                    }
                else:
                    continue

                if conf < effective_gate:
                    continue

                # AXIOM Score computation
                prob_decimal = conf / 100.0
                edge, axiom_score, cal_conf, timing = compute_edge_and_score(
                    prob_decimal, dc_conf / 100.0, prob_decimal * 0.95,
                    hours_away, epi_unc
                )

                # Kelly stake
                proxy_odds   = 1.0 / max(0.01, dc_conf / 100.0) * 1.05
                _, _, stake_pct = compute_kelly_stake(
                    prob_decimal, max(1.01, proxy_odds), bankroll, epi_unc
                )

                tier, tier_label = get_card_tier(conf, bet_type)

                candidates.append({
                    **base,
                    "bet_type":      bet_type,
                    "bet":           f"{bt_meta['emoji']} {bt_meta['label']}",
                    "confidence":    conf,
                    "dc_confidence": dc_conf,
                    "epistemic_unc": epi_unc,
                    "edge":          round(edge, 4),
                    "axiom_score":   round(axiom_score, 4),
                    "kelly_pct":     round(stake_pct * 100, 2),
                    "tier":          tier,
                    "tier_label":    tier_label,
                    "reasoning":     reasoning,
                    "factors":       factors,
                    **extra,
                })

    candidates.sort(key=lambda x: (x["axiom_score"], x["confidence"]), reverse=True)
    seen_matches: set = set()
    top_picks: List[Dict] = []
    for c in candidates:
        mkey = c["match"]
        if mkey not in seen_matches:
            seen_matches.add(mkey)
            top_picks.append(c)
        if len(top_picks) >= TOP_N:
            break

    for i, p in enumerate(top_picks, 1):
        p["rank"] = i
        save_pick(p)

    return top_picks, leagues_hit, games_eval, data_pts


# ═══════════════════════════════════════════════════════════════════════
#  AUTO-GRADER + ADAPTIVE LEARNER
# ═══════════════════════════════════════════════════════════════════════

def grade_and_learn() -> int:
    """
    Grade pending picks against real ESPN scoreboard results.
    Runs adaptive weight update for each newly graded pick.
    Returns count of newly graded picks.
    """
    conn = get_db()
    try:
        pending = conn.execute(
            "SELECT id, match, league_id, kickoff, bet_type, factors_json FROM picks_log WHERE result='pending'"
        ).fetchall()
    except Exception:
        return 0

    updated = 0
    clv_updates: List[float] = []

    for row_id, match, league_id, kickoff, bet_type, factors_json_str in pending:
        ko = parse_utc(kickoff)
        if not ko or (now_utc() - ko).total_seconds() < 6000:
            continue
        if not league_id:
            continue

        parts = match.split(" vs ")
        if len(parts) != 2:
            continue
        home_name, away_name = parts[0].strip(), parts[1].strip()

        date_str = ko.strftime("%Y%m%d")
        data     = safe_get(f"{ESPN_SOCCER}/{league_id}/scoreboard", params={"dates": date_str})
        if not data:
            continue

        for ev in data.get("events", []):
            comps = ev.get("competitions", [])
            if not comps:
                continue
            comp = comps[0]
            if not comp.get("status", {}).get("type", {}).get("completed", False):
                continue
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            names = {c.get("team", {}).get("displayName", "") for c in competitors}
            if home_name not in names and away_name not in names:
                continue

            home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
            away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
            hs  = _parse_score(home_c.get("score"))
            as_ = _parse_score(away_c.get("score"))
            tot = hs + as_

            result = "LOST"
            if not bet_type or bet_type == "OVER_25":
                result = "WON" if tot > 2.5 else "LOST"
            elif bet_type == "OVER_05":
                result = "WON" if tot > 0.5 else "LOST"
            elif bet_type == "OVER_15":
                result = "WON" if tot > 1.5 else "LOST"
            elif bet_type == "BTTS_YES":
                result = "WON" if hs > 0 and as_ > 0 else "LOST"
            elif bet_type == "HOME_WIN":
                result = "WON" if hs > as_ else "LOST"
            elif bet_type == "AWAY_WIN":
                result = "WON" if as_ > hs else "LOST"

            conn.execute(
                "UPDATE picks_log SET result=?,home_score=?,away_score=? WHERE id=?",
                (result, hs, as_, row_id)
            )
            updated += 1

            # CLV proxy: positive if won (model confirmed)
            clv_proxy = 0.02 if result == "WON" else -0.015
            clv_updates.append(clv_proxy)

            try:
                factors = json.loads(factors_json_str or "{}")
                if factors and bet_type:
                    update_weights(bet_type, factors, won=(result == "WON"))
            except Exception:
                pass
            break

    if updated:
        conn.commit()

    # Update CLV history in session state
    if clv_updates:
        st.session_state.clv_history = (st.session_state.clv_history + clv_updates)[-200:]
        new_regime, reason = detect_regime(st.session_state.clv_history)
        if new_regime != st.session_state.current_regime:
            st.session_state.current_regime = new_regime
            st.session_state.regime_last_updated = now_utc().isoformat()

    return updated


# ═══════════════════════════════════════════════════════════════════════
#  CLV HEATMAP UPDATER
# ═══════════════════════════════════════════════════════════════════════

def update_inefficiency_heatmap(picks: List[Dict]) -> None:
    """
    Update the in-memory inefficiency heatmap from current scan picks.
    Tracks confidence by league × bet_type as a proxy for inefficiency.
    """
    heatmap = st.session_state.inefficiency_heatmap
    for p in picks:
        league  = p.get("league", "Unknown")
        bt      = p.get("bet_type", "OVER_25")
        key     = f"{league}|{bt}"
        if key not in heatmap:
            heatmap[key] = {"count": 0, "conf_sum": 0.0, "axiom_sum": 0.0, "wins": 0, "losses": 0}
        heatmap[key]["count"]     += 1
        heatmap[key]["conf_sum"]  += p.get("confidence", 0.0)
        heatmap[key]["axiom_sum"] += p.get("axiom_score", 0.0)
    st.session_state.inefficiency_heatmap = heatmap


# ═══════════════════════════════════════════════════════════════════════
#  COUNTDOWN HTML
# ═══════════════════════════════════════════════════════════════════════

def countdown_html(kickoff_utc: str, pick_id: str) -> str:
    """Generate JavaScript countdown timer HTML for a pick card."""
    return f"""
<div id="cd_{pick_id}" class="countdown" style="color:#00b4ff;font-size:.85rem;letter-spacing:2px;">
  ⏱ Calculating...
</div>
<script>
(function(){{
  var target = new Date("{kickoff_utc}");
  var el = document.getElementById("cd_{pick_id}");
  function tick(){{
    var now = new Date(), diff = target - now;
    if(diff<=0){{ el.innerHTML="🔴 LIVE NOW"; el.style.color="#ff1744"; return; }}
    var h=Math.floor(diff/3600000), m=Math.floor((diff%3600000)/60000), s=Math.floor((diff%60000)/1000);
    var parts=[]; if(h>0) parts.push(h+"h"); parts.push(("0"+m).slice(-2)+"m"); parts.push(("0"+s).slice(-2)+"s");
    el.innerHTML="⏱ KICKOFF IN "+parts.join(" ");
  }}
  tick(); setInterval(tick,1000);
}})();
</script>
"""


# ═══════════════════════════════════════════════════════════════════════
#  PICK CARD RENDERER
# ═══════════════════════════════════════════════════════════════════════

def render_pick_card(pick: Dict) -> None:
    """Render a single pick card with full AXIOM metrics and Dixon-Coles indicators."""
    tier      = pick["tier"]
    conf      = pick["confidence"]
    dc_conf   = pick.get("dc_confidence", conf)
    edge      = pick.get("edge", 0.0)
    axiom_s   = pick.get("axiom_score", 0.5)
    kelly_pct = pick.get("kelly_pct", 0.0)
    bet_type  = pick["bet_type"]
    bt_meta   = BET_TYPES.get(bet_type, BET_TYPES["OVER_25"])
    pick_id   = hashlib.md5(f"{pick['match']}{bet_type}".encode()).hexdigest()[:6]
    bar_w     = min(99, int(conf))
    pois_pct  = pick.get("poisson_p", 0) * 100

    bet_css  = f"bet-{bt_meta['css']}"
    card_css = f"pick-card {tier}"

    h2h_html = ""
    if pick.get("h2h_count", 0) > 0:
        h2h_html = f'<span class="pill pill-h2h">H2H({pick["h2h_count"]}g)</span>'

    conn        = get_db()
    updates_row = conn.execute(
        "SELECT SUM(updates) FROM model_weights WHERE bet_type=?", (bet_type,)
    ).fetchone()
    total_updates = int(updates_row[0] or 0) if updates_row else 0
    learn_html    = f'<span class="pill pill-learn">🧠 {total_updates} LEARNS</span>' if total_updates > 0 else ""

    # Edge pill
    edge_html = ""
    if abs(edge) > 0.005:
        edge_color = "green" if edge > 0 else "red"
        edge_html  = f'<span class="pill pill-{"edge" if edge > 0 else "abst"}">EDGE {edge*100:+.1f}%</span>'

    # Regime pill
    regime_html = _regime_pill(pick.get("regime", "B"))

    # AXIOM score bar (0-100)
    axiom_bar = min(99, int(axiom_s * 100))

    card_html = f"""
<div class="{card_css}">
  <div class="rank-badge">#{pick['rank']}</div>
  <div class="card-league">{pick['league']}</div>
  <div class="card-teams">{pick['home']} <span class="card-vs">vs</span> {pick['away']}</div>
  <div class="card-bet {bet_css}">{pick['bet']}</div>

  <div class="conf-row">
    <span class="conf-pct {tier}">{conf:.1f}%</span>
    <span class="tier-chip {tier}">{pick['tier_label']}</span>
  </div>
  <div class="conf-track">
    <div class="conf-fill {tier}" style="width:{bar_w}%;"></div>
  </div>

  <div style="display:flex;gap:8px;align-items:center;margin-bottom:10px;flex-wrap:wrap;">
    <span class="dc-badge">⚡ DC: {dc_conf:.1f}%</span>
    <span class="kelly-badge">📐 Kelly: {kelly_pct:.2f}%</span>
    {regime_html}
  </div>

  <div class="ai-grid">
    <div class="ai-factor">
      <span class="ai-factor-val cyan">{pois_pct:.1f}%</span>
      <div class="ai-factor-lbl">DC Prob</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val gold">{pick['xg_total']:.2f}</span>
      <div class="ai-factor-lbl">xG Total</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val {"green" if edge > 0 else "red"}">{edge*100:+.1f}%</span>
      <div class="ai-factor-lbl">Edge</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val">{pick['home_btts']:.0f}/{pick['away_btts']:.0f}%</span>
      <div class="ai-factor-lbl">BTTS%</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val">{_form_label(pick['home_form'])}</span>
      <div class="ai-factor-lbl">Home Form</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val purple">{axiom_s:.2f}</span>
      <div class="ai-factor-lbl">AXIOM Score</div>
    </div>
  </div>

  <div class="pills-row">
    <span class="pill pill-time">{pick['kickoff_cat']}</span>
    <span class="pill pill-xg">xG: {pick['xg_home']:.2f}+{pick['xg_away']:.2f}</span>
    {h2h_html}
    {edge_html}
    {learn_html}
  </div>

  <div class="card-reason">{pick['reasoning']}</div>
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)
    try:
        st.html(countdown_html(pick["kickoff_utc"], pick_id))
    except Exception:
        try:
            import streamlit.components.v1 as components
            components.html(countdown_html(pick["kickoff_utc"], pick_id), height=28)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════
#  LIVE MATCH ENGINE
# ═══════════════════════════════════════════════════════════════════════

_LIVE_STATUSES = {
    "STATUS_IN_PROGRESS", "in", "STATUS_HALFTIME", "STATUS_END_PERIOD",
    "STATUS_OVERTIME", "2nd Half", "1st Half", "Half Time", "HT",
    "in progress", "In Progress",
}


def fetch_live_scoreboard(league_id: str) -> List[Dict]:
    """Fetch currently in-progress games from ESPN for a league."""
    date_str = now_utc().strftime("%Y%m%d")
    data = safe_get(f"{ESPN_SOCCER}/{league_id}/scoreboard", params={"dates": date_str}, timeout=8)
    if not data:
        return []

    live_events = []
    for ev in data.get("events", []):
        comps = ev.get("competitions", [])
        if not comps:
            continue
        comp        = comps[0]
        status_obj  = comp.get("status", {})
        status_type = status_obj.get("type", {})
        status_name = status_type.get("name", "")
        status_desc = status_type.get("shortDetail", status_obj.get("displayClock", ""))
        completed   = status_type.get("completed", False)
        state       = status_type.get("state", "")

        is_live = (
            state == "in"
            or status_name in _LIVE_STATUSES
            or any(s in status_name for s in ("PROGRESS", "HALF", "PERIOD", "OVERTIME"))
        )
        if not is_live or completed:
            continue

        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue

        home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
        hs  = _parse_score(home_c.get("score"))
        as_ = _parse_score(away_c.get("score"))

        clock       = status_obj.get("displayClock", "")
        period      = status_obj.get("period", 0)
        is_halftime = "HALF" in status_name.upper() or "HT" in status_name

        live_events.append({
            "event_id": ev.get("id", ""), "date": ev.get("date", ""),
            "home_id": str(home_c.get("team", {}).get("id", "")),
            "home_name": home_c.get("team", {}).get("displayName", ""),
            "away_id": str(away_c.get("team", {}).get("id", "")),
            "away_name": away_c.get("team", {}).get("displayName", ""),
            "home_score": hs, "away_score": as_, "total_goals": hs + as_,
            "clock": clock, "period": period, "is_halftime": is_halftime,
            "status_name": status_name, "status_desc": status_desc, "league_id": league_id,
        })
    return live_events


def _in_game_over_confidence(
    pre_conf: float,
    goals_scored: int,
    line: float,
    clock: str,
    period: int,
    is_halftime: bool,
) -> Tuple[float, str]:
    """
    Adjust pre-match Dixon-Coles confidence based on current live score/time.
    Returns (adjusted_confidence%, edge_note).
    """
    if goals_scored > line:
        return 99.9, f"✅ ALREADY {goals_scored} goals scored — BET LANDED"

    goals_needed = int(line - goals_scored) + 1

    try:
        mins_played = int(float(clock.replace("'", "").strip())) if clock and clock not in ("", "0:00") else 0
    except Exception:
        mins_played = 45 if is_halftime else (45 if period == 1 else 70 if period == 2 else 0)

    mins_remaining = max(1, 90 - mins_played)
    time_left      = mins_remaining / 90.0

    if goals_needed <= 0:
        return 99.9, "BET ALREADY WON"

    scaling = time_left ** goals_needed
    adj     = min(99.9, max(1.0, pre_conf * scaling * (1 + goals_scored * 0.15)))
    note    = (
        f"Need {goals_needed} more goal(s) · ~{mins_remaining}' remaining · "
        f"Pre-match DC model: {pre_conf:.0f}%"
    )
    return round(adj, 1), note


@st.cache_data(ttl=30, show_spinner=False)
def scan_live_matches() -> Tuple[List[Dict], int]:
    """Scan all leagues for live games with in-play DC predictions."""
    live_results: List[Dict] = []
    total_live = 0

    for league_id, league_name, flag in LEAGUES:
        live_events = fetch_live_scoreboard(league_id)
        if not live_events:
            continue

        total_live += len(live_events)

        for ev in live_events:
            home_sched = fetch_team_schedule(league_id, ev["home_id"], ev["home_name"])
            away_sched = fetch_team_schedule(league_id, ev["away_id"], ev["away_name"])

            home_st = team_stats(home_sched, ev["home_name"]) if home_sched else None
            away_st = team_stats(away_sched, ev["away_name"]) if away_sched else None
            h2h     = get_h2h_stats(home_sched, away_sched, ev["home_name"], ev["away_name"]) \
                      if home_sched and away_sched else None

            predictions: List[Dict] = []
            xg_h = xg_a = total_xg = 0.0

            if home_st and away_st:
                xg_h, xg_a = _xg(home_st, away_st)
                total_xg   = round(xg_h + xg_a, 2)

                for bet_type, bt_meta in BET_TYPES.items():
                    if bet_type in ("OVER_05", "OVER_15", "OVER_25"):
                        line = bt_meta["line"]
                        pre_conf, dc_conf, _, factors, reasoning = compute_over_confidence(
                            home_st, away_st, line, h2h, bet_type
                        )
                        adj_conf, edge_note = _in_game_over_confidence(
                            dc_conf, ev["total_goals"], line,
                            ev["clock"], ev["period"], ev["is_halftime"]
                        )
                        already_hit = ev["total_goals"] > line
                        predictions.append({
                            "bet_type": bet_type, "label": bt_meta["label"],
                            "emoji": bt_meta["emoji"], "css": bt_meta["css"],
                            "pre_conf": pre_conf, "live_conf": adj_conf,
                            "already_hit": already_hit, "edge_note": edge_note,
                            "reasoning": reasoning,
                        })

                    elif bet_type == "BTTS_YES":
                        pre_conf, dc_conf, _, factors, reasoning = compute_btts_confidence(
                            home_st, away_st, h2h
                        )
                        already_hit = ev["home_score"] > 0 and ev["away_score"] > 0
                        one_scored  = (ev["home_score"] > 0) != (ev["away_score"] > 0)
                        try:
                            mins_played = int(float(ev["clock"].replace("'", "").strip())) if ev["clock"] else 0
                        except Exception:
                            mins_played = 45 if ev["is_halftime"] else 70
                        mins_remaining = max(1, 90 - mins_played)

                        if already_hit:
                            adj_conf  = 99.9
                            edge_note = "✅ BOTH TEAMS SCORED — BET LANDED"
                        elif one_scored:
                            adj_conf  = round(min(99.9, dc_conf * (mins_remaining / 90) * 1.4), 1)
                            edge_note = f"1 team scored ✓ · Other needs to score · ~{mins_remaining}' left"
                        else:
                            adj_conf  = round(min(99.9, dc_conf * (mins_remaining / 90) ** 2 * 1.2), 1)
                            edge_note = f"No goals yet · ~{mins_remaining}' remaining"

                        predictions.append({
                            "bet_type": "BTTS_YES", "label": bt_meta["label"],
                            "emoji": bt_meta["emoji"], "css": "btts",
                            "pre_conf": pre_conf, "live_conf": adj_conf,
                            "already_hit": already_hit, "edge_note": edge_note,
                            "reasoning": reasoning,
                        })

                    elif bet_type in ("HOME_WIN", "AWAY_WIN"):
                        side = "HOME" if bet_type == "HOME_WIN" else "AWAY"
                        pre_conf, dc_conf, _, factors, reasoning = compute_result_confidence(
                            home_st, away_st, h2h, side
                        )
                        hs, as_ = ev["home_score"], ev["away_score"]
                        currently_winning = (side == "HOME" and hs > as_) or (side == "AWAY" and as_ > hs)
                        try:
                            mins_played = int(float(ev["clock"].replace("'", "").strip())) if ev["clock"] else 0
                        except Exception:
                            mins_played = 45 if ev["is_halftime"] else 70
                        mins_remaining = max(1, 90 - mins_played)
                        time_factor    = mins_remaining / 90

                        if currently_winning:
                            adj_conf  = round(min(99.9, dc_conf + (1 - time_factor) * (99.9 - dc_conf) * 0.55), 1)
                            edge_note = f"{'🏠' if side=='HOME' else '✈️'} WINNING · {mins_remaining}' left"
                        elif (side == "HOME" and as_ > hs) or (side == "AWAY" and hs > as_):
                            adj_conf  = round(max(1.0, dc_conf * time_factor * 0.6), 1)
                            edge_note = f"LOSING · {mins_remaining}' remaining"
                        else:
                            adj_conf  = round(min(99.9, dc_conf * (0.7 + time_factor * 0.3)), 1)
                            edge_note = f"Score level · {mins_remaining}' remaining"

                        predictions.append({
                            "bet_type": bet_type, "label": bt_meta["label"],
                            "emoji": bt_meta["emoji"],
                            "css": "result" if bet_type == "HOME_WIN" else "away",
                            "pre_conf": pre_conf, "live_conf": adj_conf,
                            "already_hit": False, "edge_note": edge_note,
                            "reasoning": reasoning,
                        })

            predictions.sort(key=lambda p: p["live_conf"], reverse=True)

            live_results.append({
                **ev,
                "league": f"{flag} {league_name}",
                "league_id": league_id,
                "predictions": predictions,
                "xg_home":   round(xg_h, 2),
                "xg_away":   round(xg_a, 2),
                "xg_total":  total_xg,
                "has_model": home_st is not None and away_st is not None,
            })

    live_results.sort(
        key=lambda x: (
            x["total_goals"],
            x["predictions"][0]["live_conf"] if x["predictions"] else 0
        ),
        reverse=True,
    )
    return live_results, total_live


def render_live_card(match: Dict, idx: int) -> None:
    """Render a live match card with current score and AXIOM DC predictions."""
    hs          = match["home_score"]
    as_         = match["away_score"]
    clock       = match.get("clock", "")
    is_halftime = match.get("is_halftime", False)
    has_model   = match.get("has_model", False)

    if is_halftime:
        clock_html = '<span class="halftime-chip">⏸ HALF TIME</span>'
    elif clock:
        clock_html = f'<span class="live-clock">⏱ {clock}</span>'
    else:
        clock_html = '<span class="live-clock">🔴 LIVE</span>'

    preds = match.get("predictions", [])
    pred_cells_html = ""
    if preds:
        color_map = {
            "over05": "var(--cyan)", "over15": "var(--blue)", "over25": "var(--gold)",
            "btts": "var(--purple)", "result": "var(--cyan)", "away": "var(--orange)",
            "home": "var(--green)",
        }
        for p in preds[:3]:
            hit_class  = "hit" if p["already_hit"] else ""
            edge_class = "live-edge" if p["live_conf"] >= 70 and not p["already_hit"] else ""
            cell_class = hit_class or edge_class
            color      = color_map.get(p["css"], "var(--blue)")
            val_display = "✅ HIT" if p["already_hit"] else f"{p['live_conf']:.0f}%"
            pred_cells_html += f"""
<div class="pred-cell {cell_class}">
  <span class="pred-val" style="color:{color};">{val_display}</span>
  <div class="pred-lbl">{p['emoji']} {p['label']}</div>
</div>"""
    else:
        pred_cells_html = '<div style="color:var(--muted);font-size:.8rem;padding:8px;">Insufficient team history</div>'

    top_edge_note = preds[0]["edge_note"] if preds else ""
    top_reasoning = preds[0]["reasoning"] if preds else "Insufficient data."

    card_html = f"""
<div class="live-card" id="live_{idx}">
  <div class="live-header">
    <div>
      <span class="live-pulse"></span>
      <span style="font-family:'Barlow Condensed',sans-serif;font-size:.72rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;">{match['league']}</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      {clock_html}
      <span class="live-badge">🔴 LIVE</span>
    </div>
  </div>

  <div class="live-score-block">
    <div class="live-team-name">{match['home_name']}</div>
    <span class="live-score">{hs} <span class="live-sep">-</span> {as_}</span>
    <div class="live-team-name">{match['away_name']}</div>
  </div>

  <div style="text-align:center;margin-bottom:10px;">
    <span style="font-family:'Barlow Condensed',sans-serif;font-size:.72rem;color:var(--muted);letter-spacing:2px;">
      {'⚡ AXIOM DC MODEL ACTIVE' if has_model else '⚠️ LIVE SCORE ONLY — INSUFFICIENT HISTORY'}
    </span>
  </div>

  <div class="pred-grid">{pred_cells_html}</div>

  {'<div class="live-reason">🤖 <strong>Live DC Edge:</strong> ' + top_edge_note + '<br>' + top_reasoning + '</div>' if has_model else ''}
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
#  MAIN STREAMLIT APPLICATION
# ═══════════════════════════════════════════════════════════════════════

def main() -> None:
    """Main AXIOM Streamlit application entry point."""
    _init_session_state()

    # Auto-refresh every 60 seconds
    try:
        from streamlit_autorefresh import st_autorefresh
        count = st_autorefresh(interval=60_000, key="axiom_v4_refresh")
    except ImportError:
        count = 0

    # ── Hero ──────────────────────────────────────────────────────────
    st.markdown("""
<div class="axiom-hero">
  <span class="axiom-logo">⚡ AXIOM</span>
  <div class="axiom-tagline">Structured Inefficiency Extraction Engine · Dixon-Coles · Ensemble · Kelly Sizing</div>
  <div class="axiom-version">
    v4.0 · OVER 0.5/1.5/2.5 · BTTS · Home/Away Win · 75+ Leagues · Self-Learning · CLV Tracking
  </div>
  <div class="axiom-bar"></div>
</div>
""", unsafe_allow_html=True)

    # ── Auto-grade + learn ────────────────────────────────────────────
    newly_graded = grade_and_learn()

    # ── Regime status bar ─────────────────────────────────────────────
    regime        = st.session_state.current_regime
    bankroll      = st.session_state.bankroll
    peak          = st.session_state.peak_bankroll
    cb_active, cb_reason = check_circuit_breaker(bankroll, peak)
    if cb_active and not st.session_state.circuit_breaker_active:
        st.session_state.circuit_breaker_active = True
        st.warning(f"⚠️ Circuit Breaker Active — {cb_reason}", icon="🛑")

    # ── Tabs ──────────────────────────────────────────────────────────
    tab_picks, tab_live, tab_results, tab_brain, tab_risk, tab_clv, tab_about = st.tabs([
        "🎯 Top Picks",
        "🔴 Live Matches",
        "🏆 Results",
        "🧠 AI Brain",
        "📐 Risk Engine",
        "📊 CLV & Heatmap",
        "⚡ System",
    ])

    # ══════════════════════════════════════════════════════════════════
    #  TAB 1 — TOP PICKS
    # ══════════════════════════════════════════════════════════════════
    with tab_picks:
        now_cat = (now_utc() + CAT_OFFSET).strftime("%d %b %Y · %H:%M CAT")
        regime_label = {"A": "🔴 Efficient", "B": "🟢 Exploitable", "C": "⚠️ Unstable"}.get(regime, "🟢 Exploitable")
        st.caption(
            f"🕐 {now_cat} &nbsp;·&nbsp; Regime: **{regime_label}** &nbsp;·&nbsp; "
            f"Scanning next {WINDOW_HOURS}h &nbsp;·&nbsp; Auto-refresh 60s &nbsp;·&nbsp; "
            f"Scan #{count or '—'}"
        )
        if newly_graded:
            st.toast(f"🧠 AXIOM learned from {newly_graded} graded pick(s)!", icon="⚡")
        if cb_active:
            st.error(f"🛑 Circuit Breaker: {cb_reason} — Kelly halved, gates raised")

        with st.spinner(""):
            st.markdown(
                '<div class="scan-line">⚡ AXIOM v4.0 — DIXON-COLES SCANNING 75+ LEAGUES ⚡</div>',
                unsafe_allow_html=True
            )
            picks, leagues_hit, games_eval, data_pts = scan_all_leagues()
            update_inefficiency_heatmap(picks)
            st.session_state.scan_count += 1
            st.session_state.last_scan_time = now_utc().isoformat()

        elite_cnt  = sum(1 for p in picks if p["tier"] == "elite")
        goals_cnt  = sum(1 for p in picks if "OVER" in p.get("bet_type", ""))
        btts_cnt   = sum(1 for p in picks if p.get("bet_type") == "BTTS_YES")
        result_cnt = sum(1 for p in picks if p.get("bet_type") in ("HOME_WIN", "AWAY_WIN"))
        avg_edge   = safe_mean([p.get("edge", 0) for p in picks]) * 100

        st.markdown(f"""
<div class="metrics-row">
  <div class="metric-box"><span class="metric-val">{len(picks)}</span><div class="metric-lbl">Picks Today</div></div>
  <div class="metric-box"><span class="metric-val gold">{elite_cnt}</span><div class="metric-lbl">🔥 Elite</div></div>
  <div class="metric-box"><span class="metric-val">{goals_cnt}</span><div class="metric-lbl">⚽ Goals</div></div>
  <div class="metric-box"><span class="metric-val purple">{btts_cnt}</span><div class="metric-lbl">🎯 BTTS</div></div>
  <div class="metric-box"><span class="metric-val cyan">{result_cnt}</span><div class="metric-lbl">🏠✈️ Result</div></div>
  <div class="metric-box"><span class="metric-val">{leagues_hit}</span><div class="metric-lbl">Leagues Hit</div></div>
  <div class="metric-box"><span class="metric-val">{games_eval}</span><div class="metric-lbl">Games Eval</div></div>
  <div class="metric-box"><span class="metric-val {"green" if avg_edge > 0 else "red"}">{avg_edge:+.1f}%</span><div class="metric-lbl">Avg Edge</div></div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        if not picks:
            st.markdown("""
<div class="no-picks">
  <span class="no-picks-icon">⏳</span>
  No games meet AXIOM's confidence thresholds in the next 24 hours.<br>
  AXIOM v4.0 applies Dixon-Coles corrections and regime-adjusted gates.<br>
  Continuously scanning — check back as fixtures enter the window.
</div>
""", unsafe_allow_html=True)
        else:
            c1, c2, c3 = st.columns(3)
            c1.markdown('<span style="font-family:Barlow Condensed;color:#ffb300;font-size:.85rem;">🔥 ELITE — DC + ensemble exceptional edge</span>', unsafe_allow_html=True)
            c2.markdown('<span style="font-family:Barlow Condensed;color:#00b4ff;font-size:.85rem;">⚡ STRONG — Clear Dixon-Coles signal</span>', unsafe_allow_html=True)
            c3.markdown('<span style="font-family:Barlow Condensed;color:#ea80fc;font-size:.85rem;">🎯 BTTS / ✈️ RESULT — High confidence only</span>', unsafe_allow_html=True)
            st.markdown("---")
            for pick in picks:
                render_pick_card(pick)

    # ══════════════════════════════════════════════════════════════════
    #  TAB 2 — LIVE MATCHES
    # ══════════════════════════════════════════════════════════════════
    with tab_live:
        now_cat_live = (now_utc() + CAT_OFFSET).strftime("%d %b %Y · %H:%M CAT")
        st.caption(f"🕐 {now_cat_live} &nbsp;·&nbsp; Live scores & DC predictions updated every 30s")
        st.markdown(
            '<div class="scan-line">🔴 AXIOM LIVE INTELLIGENCE — IN-PLAY DIXON-COLES ENGINE 🔴</div>',
            unsafe_allow_html=True,
        )

        with st.spinner(""):
            live_matches, total_live = scan_live_matches()

        goals_live = sum(m["total_goals"] for m in live_matches)
        hit_cnt    = sum(1 for m in live_matches for p in m.get("predictions", []) if p.get("already_hit"))
        edge_cnt   = sum(1 for m in live_matches if m.get("predictions") and m["predictions"][0]["live_conf"] >= 70)

        st.markdown(f"""
<div class="metrics-row">
  <div class="metric-box"><span class="metric-val red">{len(live_matches)}</span><div class="metric-lbl">🔴 Live Games</div></div>
  <div class="metric-box"><span class="metric-val gold">{goals_live}</span><div class="metric-lbl">⚽ Goals Scored</div></div>
  <div class="metric-box"><span class="metric-val green">{hit_cnt}</span><div class="metric-lbl">✅ Bets Landed</div></div>
  <div class="metric-box"><span class="metric-val cyan">{edge_cnt}</span><div class="metric-lbl">⚡ Live Edges 70%+</div></div>
  <div class="metric-box"><span class="metric-val purple">{total_live}</span><div class="metric-lbl">Total Live Found</div></div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.markdown('<span style="font-family:Barlow Condensed;color:#ff1744;font-size:.82rem;">🔴 LIVE — Game in progress</span>', unsafe_allow_html=True)
        c2.markdown('<span style="font-family:Barlow Condensed;color:#39ff14;font-size:.82rem;">✅ HIT — DC bet condition met</span>', unsafe_allow_html=True)
        c3.markdown('<span style="font-family:Barlow Condensed;color:#ffb300;font-size:.82rem;">⚡ LIVE EDGE — 70%+ DC confidence</span>', unsafe_allow_html=True)
        st.markdown("---")

        st.info("ℹ️ Live predictions use Dixon-Coles pre-match model adjusted for current score and game clock. 30-second auto-refresh.", icon="⚡")

        if not live_matches:
            st.markdown("""
<div class="live-empty">
  <span style="font-size:3rem;display:block;margin-bottom:12px;">📡</span>
  No live games detected across 75+ leagues right now.<br>
  AXIOM continuously monitors — check back when matches are in progress.
</div>
""", unsafe_allow_html=True)
        else:
            leagues_seen: Dict[str, List[Dict]] = {}
            for m in live_matches:
                leagues_seen.setdefault(m["league"], []).append(m)
            for league_name, matches in leagues_seen.items():
                st.markdown(
                    f'<div style="font-family:Barlow Condensed;font-size:.78rem;letter-spacing:3px;'
                    f'text-transform:uppercase;color:var(--muted);margin:18px 0 4px;'
                    f'border-bottom:1px solid var(--border);padding-bottom:4px;">{league_name}</div>',
                    unsafe_allow_html=True,
                )
                for idx, match in enumerate(matches):
                    render_live_card(match, idx)

    # ══════════════════════════════════════════════════════════════════
    #  TAB 3 — RESULTS
    # ══════════════════════════════════════════════════════════════════
    with tab_results:
        st.subheader("🏆 AXIOM Pick Results — Auto-Graded")
        if newly_graded:
            st.success(f"✅ {newly_graded} new pick(s) graded & learned from this refresh.")

        try:
            conn = get_db()
            rows = conn.execute("""
                SELECT match, league, bet, bet_type, xg_total, confidence, dc_confidence,
                       edge, axiom_score, kelly_pct, kickoff, result, home_score, away_score, logged_at
                FROM picks_log ORDER BY logged_at DESC LIMIT 500
            """).fetchall()

            if not rows:
                st.info("No picks logged yet — visit 🎯 Top Picks to generate predictions.")
            else:
                df = pd.DataFrame(rows, columns=[
                    "Match", "League", "Bet", "Bet Type", "xG", "Conf%",
                    "DC Conf%", "Edge", "AXIOM Score", "Kelly%",
                    "Kickoff UTC", "Result", "Home Score", "Away Score", "Logged"
                ])
                df["Conf%"]       = df["Conf%"].apply(lambda x: f"{x:.1f}%")
                df["DC Conf%"]    = df["DC Conf%"].apply(lambda x: f"{x:.1f}%")
                df["Edge"]        = df["Edge"].apply(lambda x: f"{float(x)*100:+.1f}%")
                df["AXIOM Score"] = df["AXIOM Score"].apply(lambda x: f"{float(x):.3f}")
                df["xG"]          = df["xG"].apply(lambda x: f"{x:.2f}")

                won  = df[df["Result"] == "WON"]
                lost = df[df["Result"] == "LOST"]
                pend = df[df["Result"] == "pending"]
                tot  = len(won) + len(lost)
                wr   = f"{len(won)/tot*100:.1f}%" if tot > 0 else "—"

                c1, c2, c3, c4, c5 = st.columns(5)
                c1.metric("✅ Won",       len(won))
                c2.metric("❌ Lost",      len(lost))
                c3.metric("⏳ Pending",   len(pend))
                c4.metric("Total Graded", tot)
                c5.metric("Win Rate",     wr)

                if tot > 0:
                    st.markdown("**Win Rate by Bet Type**")
                    graded = df[df["Result"].isin(["WON", "LOST"])]
                    for bt in BET_TYPES:
                        bdf = graded[graded["Bet Type"] == bt]
                        if bdf.empty:
                            continue
                        bw  = len(bdf[bdf["Result"] == "WON"])
                        bwr = f"{bw/len(bdf)*100:.0f}%"
                        st.markdown(
                            f"**{BET_TYPES[bt]['emoji']} {BET_TYPES[bt]['label']}**: "
                            f"{bw}/{len(bdf)} won ({bwr})"
                        )

                st.divider()
                st.markdown("### ✅ Correct Picks")
                if won.empty:
                    st.info("No graded wins yet — picks auto-graded ~100 min after kickoff.")
                else:
                    for _, r in won.iterrows():
                        score_str = (f" | Score: {int(r['Home Score'])}-{int(r['Away Score'])}"
                                     if r["Home Score"] >= 0 else "")
                        st.markdown(
                            f"⚽ **{r['Match']}** · {r['League']} · **{r['Bet']}** · "
                            f"xG: {r['xG']} · DC: {r['DC Conf%']} · Edge: {r['Edge']}{score_str} · "
                            f"<span style='color:#39ff14;font-weight:700;'>WON ✅</span>",
                            unsafe_allow_html=True
                        )
                        st.divider()

                st.markdown("### ❌ Missed Picks")
                if lost.empty:
                    st.info("No missed picks yet.")
                else:
                    for _, r in lost.iterrows():
                        score_str = (f" | Score: {int(r['Home Score'])}-{int(r['Away Score'])}"
                                     if r["Home Score"] >= 0 else "")
                        st.markdown(
                            f"⚽ **{r['Match']}** · {r['League']} · **{r['Bet']}** · "
                            f"xG: {r['xG']} · DC: {r['DC Conf%']} · Edge: {r['Edge']}{score_str} · "
                            f"<span style='color:#ff1744;font-weight:700;'>MISSED ❌</span>",
                            unsafe_allow_html=True
                        )
                        st.divider()

                if not pend.empty:
                    with st.expander(f"⏳ Pending — {len(pend)} picks awaiting results"):
                        st.dataframe(
                            pend[["Match", "League", "Bet", "DC Conf%", "AXIOM Score", "Kickoff UTC"]],
                            hide_index=True
                        )
        except Exception as e:
            st.error(f"Results log error: {e}")

    # ══════════════════════════════════════════════════════════════════
    #  TAB 4 — AI BRAIN
    # ══════════════════════════════════════════════════════════════════
    with tab_brain:
        st.subheader("🧠 AXIOM Adaptive Intelligence — Ensemble Weight Tracker")
        st.markdown(
            "AXIOM automatically adjusts ensemble weights after every graded pick. "
            "The Dixon-Coles component maintains a minimum floor of **0.02** per factor — "
            "no signal is ever fully discarded (catastrophic forgetting prevention)."
        )

        try:
            conn = get_db()
            rows = conn.execute(
                "SELECT bet_type, factor, weight, wins, losses, updates FROM model_weights ORDER BY bet_type, weight DESC"
            ).fetchall()
            if rows:
                df_w = pd.DataFrame(rows, columns=["Bet Type", "Factor", "Weight", "Wins", "Losses", "Updates"])
                df_w["Weight"] = df_w["Weight"].apply(lambda x: f"{x*100:.1f}%")

                for bt in BET_TYPES:
                    bdf = df_w[df_w["Bet Type"] == bt]
                    if bdf.empty:
                        continue
                    total_upd = bdf["Updates"].astype(int).sum()
                    total_w   = bdf["Wins"].astype(int).sum()
                    total_l   = bdf["Losses"].astype(int).sum()
                    with st.expander(
                        f"{BET_TYPES[bt]['emoji']} {BET_TYPES[bt]['label']} — "
                        f"{total_upd} updates · {total_w}W / {total_l}L"
                    ):
                        st.dataframe(bdf[["Factor", "Weight", "Wins", "Losses", "Updates"]], hide_index=True)
            else:
                st.info("No weight data yet — initializes on first scan.")
        except Exception as e:
            st.error(f"Weight data error: {e}")

        st.divider()
        st.markdown("**Ensemble Architecture**")
        st.markdown("- Dixon-Coles (primary, 55% weight) — bivariate Poisson with ρ correction")
        st.markdown("- Naive Poisson (25% weight) — maintains ensemble diversity")
        st.markdown("- Historical rates (20% weight) — venue-split over/BTTS/win rates")
        st.markdown(f"- All weights normalized per bet type · Minimum floor: 0.02 (no forgetting)")
        st.markdown(f"- Learning rate: `{LEARNING_RATE}` · Signal: +1.0 WON / -0.5 LOST (asymmetric)")

        st.divider()
        st.markdown("**Regime Detection**")
        regime      = st.session_state.current_regime
        clv_hist    = st.session_state.clv_history
        regime_desc = detect_regime(clv_hist)[1] if len(clv_hist) >= 10 else "Insufficient history"
        st.markdown(f"Current Regime: {_regime_pill(regime)}", unsafe_allow_html=True)
        st.markdown(f"Status: {regime_desc}")
        st.markdown(f"CLV history points: {len(clv_hist)}")

        if len(clv_hist) >= 5:
            df_clv = pd.DataFrame({"CLV": clv_hist[-50:]})
            st.line_chart(df_clv, height=180)

    # ══════════════════════════════════════════════════════════════════
    #  TAB 5 — RISK ENGINE
    # ══════════════════════════════════════════════════════════════════
    with tab_risk:
        st.subheader("📐 AXIOM Risk Engine — Kelly Sizing & Circuit Breaker")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Bankroll Management**")
            new_br = st.number_input(
                "Current Bankroll ($)", min_value=10.0, max_value=1_000_000.0,
                value=float(st.session_state.bankroll), step=10.0, key="br_input"
            )
            if st.button("Update Bankroll", key="update_br"):
                st.session_state.bankroll = new_br
                if new_br > st.session_state.peak_bankroll:
                    st.session_state.peak_bankroll = new_br
                st.toast("Bankroll updated", icon="✅")

            br    = st.session_state.bankroll
            peak  = st.session_state.peak_bankroll
            drawdown = max(0.0, (peak - br) / peak) if peak > 0 else 0.0
            cb_active, cb_reason = check_circuit_breaker(br, peak)

            st.metric("Current Bankroll", f"${br:,.2f}")
            st.metric("Peak Bankroll", f"${peak:,.2f}")
            st.metric("Drawdown", f"{drawdown*100:.1f}%", delta=f"{-drawdown*100:.1f}%" if drawdown > 0 else None)

            if cb_active:
                st.error(f"🛑 {cb_reason}")
                st.session_state.circuit_breaker_active = True
            else:
                st.success("✅ No circuit breaker — normal operations")
                if st.session_state.circuit_breaker_active:
                    if st.button("Reset Circuit Breaker", key="reset_cb"):
                        st.session_state.circuit_breaker_active = False
                        st.toast("Circuit breaker reset", icon="✅")

        with col2:
            st.markdown("**Kelly Calculator**")
            prob_input = st.slider("Model Probability", 0.01, 0.99, 0.60, 0.01, key="kelly_prob")
            odds_input = st.number_input("Decimal Odds", 1.01, 20.0, 2.00, 0.05, key="kelly_odds")
            epi_input  = st.slider("Epistemic Uncertainty", 0.01, 0.50, 0.05, 0.01, key="kelly_epi")

            kelly_full, kelly_frac, stake_pct = compute_kelly_stake(
                prob_input, odds_input, br, epi_input
            )
            stake_amt = br * stake_pct

            st.metric("Full Kelly", f"{kelly_full*100:.2f}%")
            st.metric(f"Fractional Kelly ({KELLY_FRACTION*100:.0f}%)", f"{kelly_frac*100:.2f}%")
            st.metric("Recommended Stake", f"{stake_pct*100:.2f}% (${stake_amt:,.2f})")

            st.divider()
            st.markdown("**Hard Limits**")
            st.markdown(f"- Max single bet: **{MAX_SINGLE_BET*100:.0f}%** of bankroll")
            st.markdown(f"- Max daily exposure: **{MAX_DAILY_EXPOSURE*100:.0f}%**")
            st.markdown(f"- Drawdown trigger: **{DRAWDOWN_TRIGGER*100:.0f}%** → conservative mode")
            st.markdown(f"- Conservative Kelly: **{CONSERVATIVE_KELLY*100:.1f}%** of edge")
            st.markdown(f"- Regime C: mandatory abstention above 1% bankroll")

    # ══════════════════════════════════════════════════════════════════
    #  TAB 6 — CLV & INEFFICIENCY HEATMAP
    # ══════════════════════════════════════════════════════════════════
    with tab_clv:
        st.subheader("📊 CLV Tracking & Market Inefficiency Heatmap")
        st.markdown(
            "AXIOM tracks Closing Line Value (CLV) as the primary long-term performance metric. "
            "A strategy with positive ROI but negative CLV over 200+ bets is **variance**, not skill. "
            "The heatmap shows confidence by league × bet type — high-confidence zones are tracked "
            "as persistent inefficiency candidates."
        )

        # CLV Chart
        clv_hist = st.session_state.clv_history
        if len(clv_hist) >= 5:
            col1, col2, col3 = st.columns(3)
            col1.metric("Mean CLV (last 20)", f"{safe_mean(clv_hist[-20:])*100:+.2f}%")
            col2.metric("CLV Points Tracked", len(clv_hist))
            col3.metric("Current Regime", {"A": "🔴 Efficient", "B": "🟢 Exploitable", "C": "⚠️ Unstable"}.get(regime, "?"))

            df_clv_chart = pd.DataFrame({
                "CLV": clv_hist[-100:],
                "Rolling Mean": pd.Series(clv_hist[-100:]).rolling(10, min_periods=1).mean().tolist()
            })
            st.line_chart(df_clv_chart, height=200)
        else:
            st.info("CLV history builds as picks are graded. Min 10 points needed for regime detection.")

        st.divider()
        st.markdown("**Inefficiency Heatmap** (Confidence by League × Bet Type)")
        heatmap = st.session_state.inefficiency_heatmap
        if heatmap:
            hmap_rows = []
            for key, vals in sorted(heatmap.items(), key=lambda x: -x[1]["axiom_sum"]):
                league, bt = key.split("|")
                avg_conf  = vals["conf_sum"] / max(1, vals["count"])
                avg_axiom = vals["axiom_sum"] / max(1, vals["count"])
                hmap_rows.append({
                    "League":     league,
                    "Bet Type":   bt,
                    "Count":      vals["count"],
                    "Avg Conf%":  f"{avg_conf:.1f}%",
                    "Avg AXIOM":  f"{avg_axiom:.3f}",
                    "Zone":       "🟢 HIGH" if avg_axiom > 0.6 else ("🟡 MED" if avg_axiom > 0.5 else "🔴 LOW"),
                })
            df_hmap = pd.DataFrame(hmap_rows)
            st.dataframe(df_hmap, hide_index=True, use_container_width=True)
        else:
            st.info("Heatmap populates after first scan completes.")

        st.divider()
        st.markdown("**CLV Formula**")
        st.code("CLV = ln(entry_odds / closing_odds)\n# Positive = you got better odds than closing line = genuine model edge", language="python")
        st.markdown(
            "AXIOM uses a proxy CLV (+0.02 for WON, -0.015 for LOST) until live odds integration "
            "is configured. Add `PINNACLE_API_KEY` to enable true closing line CLV."
        )

    # ══════════════════════════════════════════════════════════════════
    #  TAB 7 — SYSTEM INFO
    # ══════════════════════════════════════════════════════════════════
    with tab_about:
        st.subheader("⚡ AXIOM Structured Inefficiency Engine v4.0 — Architecture")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**Core Probability Framework**

AXIOM v4.0 implements the structured inefficiency architecture from first principles:

**Level 1 — Generative Core (Dixon-Coles)**
- Extended bivariate Poisson with ρ low-score correction
- ρ bounded to (-0.1, 0.0) — not treated as probability
- Venue-split goal rate estimation (home 55%, away 45%)
- DC correction for (0,0), (1,0), (0,1), (1,1) scorelines

**Level 2 — Ensemble Layer**
- DC Poisson: 55% weight (primary)
- Naive Poisson: 25% weight (ensemble diversity)
- Historical rates: 20% weight (venue-split)
- Adaptive online gradient descent per bet type
- Minimum factor floor: 0.02 (no catastrophic forgetting)

**Level 3 — Decision Surface**
- AXIOM Score: sigmoid-bounded (0,1) combination of edge, calibration confidence, timing, liquidity, market inefficiency
- Regime-adjusted confidence gates (A: +5%, B: standard, C: +15%)
- Kelly fractional sizing with epistemic uncertainty penalty
- Circuit breaker at 20% drawdown — conservative mode auto-activates

**Level 4 — Feedback Loop**
- Auto-grade via ESPN ~100 min post-kickoff
- Online weight update after every graded pick
- CLV proxy tracking → regime detection
- Inefficiency heatmap updates per scan
""")
        with col2:
            st.markdown("**Bet Type Configuration**")
            for bt, meta in BET_TYPES.items():
                st.markdown(f"**{meta['emoji']} {meta['label']}**: gate ≥ {meta['gate']}%")
            st.divider()
            st.markdown("**AXIOM Score Weights (initial)**")
            for k, v in AXIOM_SCORE_WEIGHTS.items():
                st.markdown(f"- `{k}`: {v}")
            st.divider()
            st.markdown("**Data Sources**")
            st.markdown("- ESPN Soccer API (primary, free)")
            st.markdown("- TheSportsDB (supplementary, free)")
            st.markdown("- 75+ leagues worldwide")
            st.divider()
            st.markdown("**Regime Detection**")
            st.markdown("- Regime A (Efficient): CLV ≈ 0 → gates raised 5%")
            st.markdown("- Regime B (Exploitable): CLV > 0.015 → standard gates")
            st.markdown("- Regime C (Unstable): High CLV variance → gates raised 15%, abstain > 1% bankroll")

        st.divider()
        st.subheader("75+ Leagues Monitored")
        league_data = [{"Flag": flag, "League": lname, "Region": lid.split(".")[0].upper(), "ID": lid}
                       for lid, lname, flag in LEAGUES]
        st.dataframe(pd.DataFrame(league_data), hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()

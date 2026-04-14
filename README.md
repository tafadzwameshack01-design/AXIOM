# AXIOM ⚡ Structured Inefficiency Engine v4.0

**AXIOM measures mispricing under uncertainty. It does not discover new mathematics.**

Upgraded from ZEUS v3.0. Implements the full structured inefficiency architecture:
Dixon-Coles bivariate Poisson · Ensemble learning · AXIOM Score · Kelly sizing · CLV tracking · Regime detection.

---

## Architecture

| Layer | Component | Description |
|---|---|---|
| Level 1 | Dixon-Coles Generative Core | Extended bivariate Poisson with ρ low-score correction |
| Level 2 | Ensemble + Adaptive Weights | DC (55%) + Poisson (25%) + Historical (20%), online gradient descent |
| Level 3 | AXIOM Score | Sigmoid-bounded (0,1) decision surface combining edge, confidence, timing, liquidity |
| Level 4 | Feedback Loop | Auto-grade → weight update → CLV tracking → regime detection |

---

## Setup

### Local

```bash
# 1. Clone / unzip
cd axiom_inefficiency_engine

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment (all optional — core runs with no keys)
cp .env.example .env
# Edit .env if you have API keys

# 4. Run
streamlit run app.py
```

### Streamlit Cloud

1. Push this folder to a GitHub repo
2. Connect at https://share.streamlit.io
3. Set `Main file path` to `app.py`
4. Add any API keys under **Settings → Secrets**

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Optional | AI-assisted analysis |
| `PINNACLE_API_KEY` | Optional | True CLV computation |
| `THE_ODDS_API_KEY` | Optional | Live market odds + real edge |
| `BETFAIR_API_KEY` | Optional | Exchange liquidity data |
| `FOOTBALL_DATA_API_KEY` | Optional | Squad/lineup/injury data |

No keys are required to run. Core functionality uses ESPN and TheSportsDB (both free, no registration).

---

## What's New in v4.0 (vs ZEUS v3.0)

- **Dixon-Coles engine** replaces naive Poisson as primary probability model (ρ correction for 0-0/1-0/0-1/1-1 scorelines)
- **Ensemble architecture** — DC (55%) + Poisson (25%) + Historical (20%) with adaptive weights
- **AXIOM Score** — sigmoid-bounded decision surface replacing raw confidence gates
- **Kelly sizing** — fractional Kelly with epistemic uncertainty penalty and circuit breaker
- **Regime detection** — CLV-based HMM proxy (Efficient / Exploitable / Unstable)
- **CLV tracking** — proxy CLV per graded pick, heatmap by league × bet type
- **Bankroll engine** — drawdown circuit breaker auto-activates at 20% from peak
- **Renamed ZEUS → AXIOM** throughout

---

## Key Constraints (Non-Overridable)

- No prediction exits AXIOM without a calibration confidence estimate
- No model weight drops below 0.02 (catastrophic forgetting prevention)
- Circuit breaker triggers at 20% drawdown — Kelly halved, gates raised
- Regime C triggers abstention above 1% bankroll
- All thresholds are parameters with update rules, not hardcoded constants
- CLV is the primary long-term metric — not raw win rate

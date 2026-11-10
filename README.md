# 💿 Dollars & Devices: Neon Edition

### A business analyst's executive decision-intelligence case study

**Live Streamlit demo:** _Add your deployment link here once published._

A distinctive Miami-neon editorial take on the executive dashboard: financial efficiency meets responsible IT device retirement. This is an **original educational portfolio project** with transparent, **fully fictional Canadian bank-labelled sample data**. It is not real-world bank reporting, an investment tool, or a brand-affiliated product.

## Why this is a business analyst project

The challenge is wider than banking. Leaders in many industries need to connect money spent, outcomes achieved, and operational sustainability to measurable actions. The business analysis workflow is:

1. Define the business problem and KPI requirements.
2. Validate source data and reconcile metrics.
3. Track targets and exceptions with balanced scorecards.
4. Compare performance without making causal claims.
5. Translate evidence into stakeholder-specific decisions.
6. Use scenarios to surface assumptions for investigation.

## Explore the seven sections

| Section | Business question | Feature |
| --- | --- | --- |
| Executive pulse | How are operations performing? | KPI cards, 100-cent graphic, weighted portfolio performance |
| Neon Newsroom | What changed and why should we care? | Rule-based, verifiable captions |
| Dual scorecards | Are we meeting defined targets? | Finance and circularity perspectives, editable thresholds |
| Benchmark | How do institutions compare? | Lean & Green quadrant and raw data table |
| Scenario lab | What happens if assumptions change? | Expense and recycling sensitivities |
| Stakeholders | Who needs what information? | Engagement lens and power–interest grid |
| Analyst guide | How were measures created? | KPI definitions, assumptions, reuse guide |

## Visual identity

The project draws on vintage neon editorial layouts, halftone dots, original CSS art, cyan/pink gradients, and bank-specific accent colours. It **does not use official GTA, Marvel, or Rockstar artwork**, and is intended to maintain accessible readability rather than sacrifice it for visual effects.

## Run locally

Python 3.11+ recommended.

### Windows PowerShell

~~~powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
~~~

### macOS or Linux

~~~bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
~~~

Run tests:

~~~bash
python -m unittest discover -s tests -v
~~~

> If a previous virtual environment exists, activate it rather than creating a new one. The legacy day01–day11 files remain untouched as a record of learning.

## Repository layout

~~~text
app.py                 # the current portfolio app
analytics.py           # validated financial & recovery calculations
theme.py               # original editorial neon CSS
config/targets.json    # editable hypothetical scorecard targets
data/raw/              # fictional input finance and e-waste tables
data/processed/        # existing practice outputs from the learning phase
tests/test_analytics.py # metric and edge-case regression checks
day01_hello.py ...     # preserved learning scripts
requirements.txt       # Python dependencies
~~~

## Data dictionary

| Field | Unit | Purpose |
| --- | --- | --- |
| bank | category | Fictional institutional entity |
| quarter | YYYY-QN | Time grain (two illustrative 2026 quarters) |
| revenue | CAD millions | Modelled revenue for the period |
| expenses | CAD millions | Modelled expenses |
| net_income | CAD millions | Modelled net income |
| desktops_kg | kg | Retired desktop hardware |
| laptops_kg | kg | Retired laptops |
| atm_terminals_kg | kg | Retired ATM terminal hardware |
| recycled_kg | kg | Reported-as-recycled weight within the fictional case |
| retired_kg | kg | Sum of three retired hardware classes |
| efficiency_ratio | % | 100 × expenses ÷ revenue (lower generally better) |
| net_margin | % | 100 × net_income ÷ revenue (higher generally better) |
| recycling_rate | % | 100 × recycled_kg ÷ retired_kg (higher generally better) |
| unrecycled_kg | kg | retired_kg − recycled_kg |
| *_growth_pct | % | Quarter-over-quarter relative change |
| *_pp_change | percentage points | Difference between quarter rates |

### Analytical safeguards

- The source data is validated for missing fields, empty cells, duplicate institution–quarter keys, negative quantities, zero denominators, and recycled mass above retired mass.
- Portfolio ratios are **calculated from aggregate numerators and denominators**, not averaged across bank rates.
- Quarter comparisons for ratio metrics use **percentage points**. Growth metrics use **percent change**.
- A first quarter without baseline receives **No baseline** rather than a misleading status.
- Targets and watch bands are **illustrative assumptions**, stored separately in JSON.
- The 100-cent display is a simplified metaphor; the residual is not an accounting line item.
- What-if sliders do not establish causation. Revenue and retired material mass are held constant; expense savings do **not** automatically increase net income.

## Design of the business-analysis workflow

**Example requirement:** As an executive sponsor, I want to compare unit cost efficiency with technology recovery rates so that I can prioritize deeper operational investigation.

**Acceptance criteria:** Select any institution and period; see recomputed ratios, labelled units, scorecard statuses, supporting raw figures, a scenario sensitivity, and clear sample-data disclaimers.

**Potential next iteration:** Replace synthetic CSVs with permissioned operational datasets, document ownership and quality rules, consult subject-matter experts on target setting, and conduct stakeholder acceptance testing.

## Deploy on Streamlit Community Cloud

1. Push the project to GitHub.
2. Visit https://share.streamlit.io and sign in with GitHub.
3. Select repository **AbhinavKarir/Dollars-and-Devices**, branch **main**, and entrypoint **app.py**.
4. Deploy, test the public URL, and put it above as the Live Streamlit demo.
5. Capture screenshots for recruiters only after verifying metrics, visuals, and mobile usability.

## Resume-friendly description (after testing and publishing)

> Built Dollars & Devices, a Streamlit/Plotly business intelligence portfolio project comparing six fictional institutional profiles across financial and device-recovery KPIs, with validated metric calculations, configurable scorecards, scenario analysis, rule-based insights, and stakeholder views.

**Important:** The figures are educational examples and should never be presented as authentic company performance. Do not make unsupported claims about business impact.

## Credit

Built as a portfolio project for Abhinav Karir, with AI-assisted implementation and review.

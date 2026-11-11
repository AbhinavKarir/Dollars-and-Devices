# Learning exercises

Historical Python, pandas, Plotly and Streamlit practice. These files are separate from the current dashboard and use earlier examples and business rules.

Run from the repository root, for example:

```sh
python exercises/day04_csv.py
python exercises/day11_ewaste.py
streamlit run exercises/day09_app.py
```

Data paths are resolved from each script, so another working directory also works. Days 04 and 11 regenerate legacy files in `data/processed/`; the main dashboard reads `data/raw/` directly and does not depend on those generated files. Days 05 and 07 open chart windows. Days 08 and 09 are historical Streamlit apps; use `streamlit run app.py` for the current dashboard.

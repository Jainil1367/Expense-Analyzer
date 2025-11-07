# Python Backend

This folder contains the analysis script `analyze.py` that reads `shared-data/expenses.csv` and generates charts into `static/`.

Quick setup

1. Create a virtual environment and install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\requirements.txt
```

2. Run the analyzer:

```powershell
python .\analyze.py
```

Notes
- `requirements.txt` already contains pandas, matplotlib and numpy. Pin versions if you need reproducible installs.
- The script expects `../shared-data/expenses.csv` relative to this folder; ensure the CSV exists.

# NASA Near-Earth Object Close-Approach Analysis

A data science project exploring 51,122 recorded close approaches of near-Earth objects (NEOs) to Earth, using NASA/JPL's public Small-Body Database API. The project follows a curiosity-driven exploratory data analysis process — asking questions, checking them against the data, and testing assumptions rather than accepting them at face value.

Full write-up of findings: [`reports/final_report.md`](reports/final_report.md)

## What's in this project

- Fetching close-approach data directly from NASA/JPL's public API (no key required)
- Cleaning and preparing the raw data for analysis
- Exploratory data analysis across four themes: distance & speed, object size, tracking uncertainty, and detection frequency over time
- Interactive Plotly visualizations, alongside static matplotlib charts used during exploration

## Project structure

```
nasa-neo-analysis/
├── data/
│   ├── raw/              # raw data fetched from the NASA API (not committed)
│   └── processed/        # cleaned dataset (not committed)
├── interactive_plots/    # exported interactive Plotly charts (HTML)
├── notebooks/
│   ├── 01_api_testing.ipynb
│   ├── 02_data_exploration.ipynb
│   ├── 03_data_cleaning.ipynb
│   └── 04_eda.ipynb
├── reports/
│   ├── final_report.md   # full write-up of findings
│   └── images/
├── src/
│   ├── api/               # data fetching
│   ├── processing/        # cleaning logic
│   └── visualization/     # plotting
├── utils/
├── .gitignore
├── requirements.txt
├── LICENSE
└── README.md
```

## Setup

Requires Python 3.12.3.

```bash
git clone https://github.com/lashvv/nasa-neo-analysis.git
cd nasa-neo-analysis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Fetch the raw dataset:
   ```bash
   cd src/api
   python3 nasa-api.py
   ```
   This saves the raw data to `data/raw/`.

2. Run the notebooks in order (`01` through `04`) to reproduce the cleaning and analysis.

## Data source

Data comes from NASA/JPL's Close-Approach Data API: https://ssd-api.jpl.nasa.gov/doc/cad.html — no API key required. Query covers close approaches within 0.05 AU of Earth, from 1900 to 2200 (past detections combined with future projections for currently known objects).

## Web app (in progress)

A companion web app is being built with Laravel, to present this research in a more accessible format and let visitors view the interactive charts, read the findings, and leave comments and share their own opinions on the analysis.

## License

MIT License

## Author

Lasha Jincharadze — [github.com/lashvv](https://github.com/lashvv)
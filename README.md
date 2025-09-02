# Excel-Dashboard

A Streamlit application for visualizing weekly data from an Excel file.

## Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Add your weekly-updated Excel file at `data/weekly_data.xlsx`. The file should contain at least a `Date` column and optional `Value` column.
3. Launch the dashboard:
   ```bash
   streamlit run app.py
   ```

Update the Excel file each week to refresh the dashboard.

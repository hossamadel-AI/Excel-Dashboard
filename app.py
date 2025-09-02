import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date, timedelta

DATA_PATH = Path("data/weekly_data.xlsx")

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load data from an Excel file if it exists."""
    if path.exists():
        return pd.read_excel(path)
    return pd.DataFrame()

def main() -> None:
    st.title("Weekly Excel Dashboard")
    df = load_data(DATA_PATH)
    if df.empty:
        st.info("Add an Excel file at data/weekly_data.xlsx with 'Date' and 'Value' columns.")
        return

    df["Date"] = pd.to_datetime(df["Date"])  # ensure datetime
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)
    mask = (df["Date"] >= pd.Timestamp(start_week)) & (df["Date"] <= pd.Timestamp(end_week))
    weekly_df = df.loc[mask]

    st.subheader(f"Data for week starting {start_week}")
    st.dataframe(weekly_df)
    if "Value" in weekly_df.columns:
        st.line_chart(weekly_df.set_index("Date")["Value"])

if __name__ == "__main__":
    main()

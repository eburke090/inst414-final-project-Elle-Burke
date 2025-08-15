import pandas as pd
import os
import logging

def evaluate_data(processed_path: str):
    logger = logging.getLogger(__name__)
    out_dir = os.path.join("data", "outputs")
    os.makedirs(out_dir, exist_ok=True)

    try:
        df = pd.read_csv(processed_path)
        df['Incident_Date'] = pd.to_datetime(df['Incident_Date'], errors='coerce')

        # Monthly trends
        monthly = df.groupby(df['Incident_Date'].dt.to_period('M')).size().reset_index(name='crime_count')
        monthly['month'] = monthly['Incident_Date'].astype(str)
        monthly = monthly[['month', 'crime_count']]
        monthly.to_csv(os.path.join(out_dir, "monthly_trends.csv"), index=False)

        # Hourly trends
        hour = pd.to_datetime(df['TIME'], format='%H:%M:%S', errors='coerce')
        if hour.isna().all():
            hour = pd.to_datetime(df['TIME'], format='%H:%M', errors='coerce')
        df['hour'] = hour.dt.hour
        hourly = df.groupby('hour', dropna=True).size().reset_index(name='crime_count')
        hourly.to_csv(os.path.join(out_dir, "hourly_trends.csv"), index=False)

        logger.info(f"Evaluation reports saved to {out_dir}")
        return out_dir
    except Exception as e:
        logger.exception("Evaluation failed.")
        raise
import pandas as pd
import os
import matplotlib.pyplot as plt
import logging

def plot_monthly_trends():
    
    """
    Generates a line plot of monthly crime trends.
    Output:
    - Saves the plot to data/analyzed/monthly_trends_plot.png
    """
     
    logger = logging.getLogger(__name__)
    out_dir = os.path.join("data", "outputs")
    figs_dir = os.path.join(out_dir, "figures")
    os.makedirs(figs_dir, exist_ok=True)
    try:
        df = pd.read_csv(os.path.join(out_dir, "monthly_trends.csv"))
        df['month'] = pd.to_datetime(df['month'].astype(str), errors='coerce')

        plt.figure(figsize=(10, 5))
        plt.plot(df['month'], df['crime_count'], marker='o')
        plt.title("Monthly Crime Trends")
        plt.xlabel("Month")
        plt.ylabel("Crime Count")
        plt.grid(True)
        path = os.path.join(figs_dir, "monthly_trends_plot.png")
        plt.tight_layout()
        plt.savefig(path)
        logger.info(f"Saved{path}")
    except Exception as e:
        logger.exception("Failed to generate monthly trends plot.")
        raise
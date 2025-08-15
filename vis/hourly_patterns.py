import pandas as pd
import os
import matplotlib.pyplot as plt
import logging 

def plot_hourly_patterns():
    """"
    Makes a bar plot of crime frequency by hour of day
    
    Output:
    - Saves the plot to data/analyzed/hourly_patterns_plot.png
    """
    logger = logging.getLogger(__name__)
    out_dir = os.path.join("data", "outputs")
    figs_dir = os.path.join(out_dir, "figures")
    os.makedirs(figs_dir, exist_ok=True)

    try:
        df = pd.read_csv(os.path.join(out_dir, "hourly_trends.csv"))
        plt.figure(figsize=(10, 6))
        plt.bar(df['hour'], df['crime_count'], color='skyblue')
        plt.title("Crime Frequency by Hour of Day")
        plt.xlabel("Hour (0-23)")
        plt.ylabel("Crime Count")
        path = os.path.join(figs_dir, "hourly_patterns_plot.png")
        plt.tight_layout()
        plt.savefig(path)
        logger.info(f"Saved {path}")
    except Exception as e:
        logger.exception("Failed to generate hourly patterns plot.")
        raise
import pandas as pd
import os
import matplotlib.pyplot as plt
import logging

def plot_hotspots(top_n=10):
    """
    Genertes a bar plot of the top N crime hotspots by area.

    Parameters:
    - top_n: Number of top hotspots to display (default is 10)

    Output:
    - Saves the plot to data/analyzed/hotspots_plot.png
    """
    logger = logging.getLogger(__name__)
    out_dir = os.path.join("data", "outputs")
    figs_dir = os.path.join(out_dir, "figures")
    os.makedirs(figs_dir, exist_ok=True)

    try:
        df = pd.read_csv(os.path.join(out_dir, "area_hotspots.csv")).head(top_n)
        plt.figure(figsize=(10, 6))
        plt.barh(df['area_name'], df['crime_count'], color='salmon')
        plt.title(f"Top {top_n} Crime Hotspots by Area")
        plt.xlabel("Crime Count")
        plt.ylabel("Area")
        path = os.path.join(figs_dir, "hotspots_plot.png")
        plt.tight_layout()
        plt.savefig(path)
        logger.info(f"Saved {path}")

    except Exception as e:
        logger.exception("Failed to generate hotspots plot.")
        raise
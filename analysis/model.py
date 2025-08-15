import pandas as pd
import os
import logging 
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

def run_model(processed_path: str, k_values=(3,4,5,6,7,)):
    logger = logging.getLogger(__name__)
    out_dir = os.path.join("data", "outputs")
    figs_dir = os.path.join(out_dir, "figures")
    metrics_dir = os.path.join(out_dir, "metrics")
    os.makedirs(figs_dir, exist_ok=True)
    os.makedirs(metrics_dir, exist_ok=True) 

    try:
        df = pd.read_csv(processed_path)
        lat_col = next((col for col in df.columns if col.upper() in ("LAT", 'LATITUDE')), None)
        lon_col = next((col for col in df.columns if col.upper() in ("LON", "LNG", "LONGITUDE", "LONG")), None)
        if not lat_col or not lon_col:
            raise ValueError("Latitude and Longitude columns not found in data.")
        
        coords = df[[lat_col, lon_col]].dropna()
        if len(coords) < max(k_values) * 3:
            logger.warning("Not enough data points for clustering. Skipping model run.")

        rows = []
        for k in k_values:
            kmeans = KMeans(n_clusters=k, n_init = "auto", random_state=42)
            labels = kmeans.fit_predict(coords)
            sil = np.nan
            inertia = kmeans.inertia_
            try:
                sil = silhouette_score(coords, labels)
            except Exception as e:
                logger.warning(f"Silhouette score calculation failed for k={k}: {e}")
            rows.append({'k': k, 'inertia': inertia, 'silhouette': sil})


        metrics = pd.DataFrame(rows)
        metrics_path = os.path.join(metrics_dir, "kmeans_metrics.csv")
        metrics.to_csv(metrics_path, index=False)

        #pick best k by highest silhouette 
        best = metrics.loc[metrics['silhouette'].idxmax()]if metrics['silhouette'].notna().any() else metrics.loc[metrics['inertia'].idxmin()]
        best_k = int(best['k'])

        #final model with best k
        final_km = KMeans(n_clusters=best_k, n_init = "auto", random_state=42)
        coords = coords.copy()
        coords['cluster'] = final_km.fit_predict(coords)

        #summaries
        cluster_sizes = coords['cluster'].value_counts().sort_index().reset_index()
        cluster_sizes.columns = ['cluster', 'crime_count']
        cluster_path = os.path.join(out_dir, "area_hotspots.csv")
        cluster_sizes.to_csv(cluster_path, index=False)

        #plots 
        plt.figure()
        plt.plot(metrics['k'], metrics['inertia'], marker='o')
        plt.title("KMeans vs Inertia")
        plt.xlabel("k")
        plt.ylabel("Inertia")
        plt.tight_layout()
        plt.savefig(os.path.join(figs_dir, "kmeans_inertia.png"))

        plt.figure()
        plt.plot(metrics['k'], metrics['silhouette'], marker='o')
        plt.title("KMeans vs Silhouette Score")
        plt.xlabel("k")
        plt.ylabel("Silhouette Score")
        plt.tight_layout()
        plt.savefig(os.path.join(figs_dir, "kmeans_silhouette.png"))

        logger.info(f"Model + metrics saved in {out_dir}")
        return {"metric_csv": metrics_path, "cluster_csv": cluster_path}
    except Exception as e:
        logger.exception("Modeling failed.")
        raise
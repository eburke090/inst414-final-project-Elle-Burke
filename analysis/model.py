import pandas as pd
import os
import logging 
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt


def run_model(processed_path: str, k_values=(3,4,5,6,7,)):
    """
    Run KMeans on incident coordinates and saves
    returns dict with paths to metrics and cluster summaries
    """
    logger = logging.getLogger(__name__)

    out_dir = os.path.join("data", "outputs")
    figs_dir = os.path.join(out_dir, "figures")
    metrics_dir = os.path.join(out_dir, "metrics")
    os.makedirs(figs_dir, exist_ok=True)
    os.makedirs(metrics_dir, exist_ok=True) 

    df = pd.read_csv(processed_path)

    lat_candidates = ["LAT", "LATITUDE", "latitude", "Y"]
    lon_candidates = ["LON", "LNG", "LONGITUDE", "longitude", "X", "LONG"]

    def pick(colnames, candidates):
        lookup = {c.upper():c for c in colnames}
        for c in candidates:
            if c.upper() in lookup:
                return lookup[c.upper()]
        return None
    
    lat_col = pick(df.columns, lat_candidates)
    lon_col = pick(df.columns, lon_candidates)
    if not lat_col or not lon_col:
        raise ValueError("Latitude/Longitude columns not found in data")
    
    coords = df[[lat_col, lon_col]].dropna()
    if coords.shape[0] < max(k_values) * 3:
        logger.warning("Not enough data points for clustering")

    rows = []
    for k in k_values:
        kmeans = KMeans(n_clusters=k, n_init="auto", random_state=42)
        labels = kmeans.fit_predict(coords)
        inertia = kmeans.inertia_
        try:
            sil = silhouette_score(coords, labels)
        except Exception as e:
            logger.warning(f"Silhouette score calculation failed for k={k}: {e}")
            sil = np.nan
        rows.append({"k": k, "inertia": inertia, "silhouette": sil})

    metrics = pd.DataFrame(rows)
    metrics_csv = os.path.join(metrics_dir, "kmeans_metrics.csv")
    metrics.to_csv(metrics_csv, index=False)

    #choose the best k 
    if metrics["silhouette"].notna().any():
        best_row = metrics.loc[metrics["silhouette"].idxmax()]
    else:
        best_row = metrics.loc[metrics["inertia"].idxmin()]
    best_k = int(best_row["k"])

    #final model & clusters
    final_km=KMeans(n_clusters=best_k, n_init="auto", random_state=42)
    final_labels = final_km.fit_predict(coords)

    assign = coords.copy()
    assign["cluster"] = final_labels
    assign_csv = os.path.join(metrics_dir, "kmeans_assignments.csv")
    assign.to_csv(assign_csv, index=False)

    #cluster sizes for hot spot vis
    cluster_sizes = assign["cluster"].value_counts().sort_index().reset_index()
    cluster_sizes.columns = ["area_name", "crime_count"]
    area_csv = os.path.join(out_dir, "area_hotspots.csv")
    cluster_sizes.to_csv(area_csv, index=False)

    #plot silhouette
    plt.figure()
    plt.plot(metrics["k"], metrics["inertia"], marker='o')
    plt.title("KMeans Inertia vs. k")
    plt.xlabel("k")
    plt.ylabel("Inertia")
    plt.tight_layout()
    inertia_png = os.path.join(figs_dir, "kmeans_inertia.png")
    plt.savefig(inertia_png)

    plt.figure()
    plt.plot(metrics["k"], metrics["silhouette"], marker='o')
    plt.title("KMeans Silhouette Score vs. k")
    plt.xlabel("k")
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    sil_png = os.path.join(figs_dir, "kmeans_silhouette.png")
    plt.savefig(sil_png)

    logger.info(f"KMeans(best_k={best_k}) done. saved in {out_dir}")
    return{
        "best_k": best_k,
        "metrics_csv": metrics_csv,
        "assignments_csv": assign_csv,
        "area_csv": area_csv,
        "inertia_png": inertia_png,
        "silhouette_png": sil_png
    }

    """
        # Plot clusters
        plt.figure(figsize=(8,6))
        plt.scatter(coords[lon_col], coords[lat_col], c=labels, cmap="tab10", s=10)
        plt.scatter(kmeans.cluster_centers_[:,1], kmeans.cluster_centers_[:,0], 
                    c='red', marker='X', s=200, label='Centroids')
        plt.title(f"KMeans Clustering (k={k})")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(figs_dir, f"kmeans_k{k}.png"))
        plt.close()
    """
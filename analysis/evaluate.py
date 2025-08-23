import os
import json
import logging
import pandas as pd

def evaluate_kmeans(metrics_csv: str, out_dir: str = "data/outputs"):
    """
    Read CSV and make an evaluation report:

    Returns dict with best_k and paths to reports
    """
    logger = logging.getLogger(__name__)
    metrics = pd.read_csv(metrics_csv)

    metrics_dir = os.path.join(out_dir, "metrics")
    os.makedirs(metrics_dir, exist_ok=True)

    # Pick best k using silhouette if availabl
    if metrics["silhouette"].notna().any():
        best_row = metrics.loc[metrics["silhouette"].idxmax()]
        crit = "Highest silhouette"
    #if not avaiable pick by inertia
    else:
        best_row = metrics.loc[metrics["inertia"].idxmin()]
        crit = "Lowest inertia (silhouette not available)"

    best_k = int(best_row["k"])
    best_sil = None if pd.isna(best_row["silhouette"] ) else float(best_row["silhouette"])
    best_inertia = float( best_row["inertia"])

    md = f"""# Model & Evaluation — KMeans

**Model**: KMeans clustering on incident coordinates (latitude/longitude)  
**Candidate k values**: {list(metrics['k'])}  
**Selection criterion**: {crit}

**Best k**: {best_k}  
**Best silhouette**: {best_sil if best_sil is not None else "N/A"}  
**Best inertia**: {best_inertia:,.0f}

**Artifacts**
- Metrics table: `data/outputs/metrics/kmeans_metrics.csv`
- Elbow plot: `data/outputs/figures/kmeans_inertia.png`
- Silhouette plot: `data/outputs/figures/kmeans_silhouette.png`

**Interpretation**
- *Silhouette* closer to 1.0 means tighter, well-separated clusters.
- *Inertia* lower is better, reflecting compact clusters; use the elbow inflection to avoid overfitting.
"""

    report = os.path.join(metrics_dir, "model_report.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write(md)

    # JSON report (machine-readable)
    report_json = os.path.join(metrics_dir, "model_report.json")
    with open(report_json, "w", encoding="utf-8") as f:
        json.dump(
            {
                "model": "KMeans",
                "candidate_k": metrics["k"].tolist(),
                "criterion": crit,
                "best_k": best_k,
                "best_silhouette": best_sil,
                "best_inertia": best_inertia,
                "metrics_csv": os.path.relpath(metrics_csv).replace("\\", "/"),
            },
            f,
            indent=2,
        )

    logger.info(f"Saved evaluation report: {report}, {report_json}")
    return {"best_k": best_k, "report_md": report, "report_json": report_json}

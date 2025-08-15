import logging
from logging.handlers import RotatingFileHandler

from etl.extract import extract_data
from etl.transform_load import transform_data
from analysis.evaluate import evaluate_data
from analysis.model import run_model
from vis.monthly_trends import plot_monthly_trends
from vis.hourly_patterns import plot_hourly_patterns
from vis.hotspots import plot_hotspots

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fh = RotatingFileHandler("pipeline.log", maxBytes=1000000, backupCount=2)
    fmt = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

def run_pipeline():
    logging.info(">>>Starting pipeline<<<")
    
    # A. Extract
    try:
        extracted_path = extract_data()
    except Exception:
        logging.error("Pipeline aborted during extraction.")

    # B. Transform and Load
    try:
        if extracted_path:
            processed_path = transform_data(extracted_path)
    except Exception:
        logging.error("Transform stage failed")
    
    # C. Analysis - Evaluate
    try:
        if processed_path:
            evaluate_data(processed_path)
    except Exception:
        logging.error("Evaluation stage failed")

    # D. Analysis - Model
    try:
        if processed_path:
            run_model(processed_path)
    except Exception:
        logging.error("Modeling stage failed")
    
    logging.error(">>>Pipeline finisgehed<<<")

def run_visualizations():
    logging.info(">>>Starting visualizations<<<")
    for func in (plot_monthly_trends, plot_hourly_patterns, plot_hotspots):
        try:
            func()
        except Exception:
            logging.error(f"Visualization {func.__name__} failed")


if __name__ == "__main__":
    setup_logging()
    try:
        run_pipeline()
        run_visualizations()
    except Exception:
        logging.critical("Pipeline failed catastrophically.")
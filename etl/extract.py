import os
import pandas as pd
import logging 

def extract_data(url="https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD", 
                 fallback = "Crime_Data_from_2020_to_Present.csv"):
    """
    Downloads raw LAPD crime data and saves to data/raw/.
    """

    print("Extracting raw data from LAPD source...")
    logger = logging.getLogger(__name__)
    extracted_dir = os.path.join("data", "extracted")
    os.makedirs(extracted_dir, exist_ok=True)
    out_path = os.path.join(extracted_dir, "crime_data_raw.csv")

    try:
        logger.info("Attempting to download data from URL.")
        df = pd.read_csv(url)
        df.to_csv(out_path, index=False)
        logger.info(f"Data successfully downloaded and saved to {out_path}.")
        return out_path
    except Exception as e:
        logger.warning(f"Failed to download data from URL. Error: {e}")
        try:
            df + pd.read_csv(fallback)
            df.to_csv(out_path, index=False)
            logger.info(f"Data successfully loaded from fallback file and saved to {out_path}.")
            return out_path
        except Exception as e2:
            logger.error(f"Failed to load data from fallback file. Error: {e2}")
            raise RuntimeError("Data extraction failed from both URL and fallback file.")
    


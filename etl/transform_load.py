import os 
import pandas as pd
import logging

def _convert_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Helper function to convert columns to appropriate data types.
    """
    rename_map = {
        'DATE': 'Incident_Date',
        'DATE OCCURRED': 'Incident_Date',
        'DATE_OCC': 'Incident_Date',
        'TIME': 'TIME',
        'TIME OCCURRED': 'TIME',
        'TIME_OCC': 'TIME',
        'Crm Cd': 'Crime_Desecription',
        'Crm Cd Desc': 'Crime_Description',
    }


    cols_lower = {col.lower(): col for col in df.columns}
    for key, new_name in list(rename_map.items()):
        #if exact not present, try case insensitive match
        if key not in df.columns:
            maybe = cols_lower.get(key.lower())
            if maybe:
                rename_map[maybe] = new_name
            rename_map.pop(key, None)
    df = df.rename(columns=rename_map)
    return df

def transform_data(extracted_path: str):
    logger = logging.getLogger(__name__)
    processed_dir = os.path.join("data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    out_path = os.path.join(processed_dir, "crime_clean.csv")

    try:
        logger.info(f"Reading extracted data from {extracted_path}.")
        df = pd.read_csv(extracted_path)
        df = _convert_columns(df)

        required = ['Incident_Date', 'TIME', 'Crime_Description']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns for transformation: {missing}")
        
        #clean
        df['Incident_Date'] = pd.to_datetime(df['Incident_Date'], errors='coerce')
        df = df.dropna(subset=['Incident_Date'])
        df = df.drop_duplicates()
        df.reset_index(drop=True)
        if 'ID' not in df.columns:
            df['ID'] = df.index + 1

        top_types = df['Crime_Description'].value_counts().head(5)
        logger.info(f"Top crime types:\n{top_types.to_string()}")
        logger.info(f"Date range: {df['Incident_Date'].min()} to {df['Incident_Date'].max()}")

        df.to_csv(out_path, index=False)
        logger.info(f"Processed data saved to {out_path}.")
        return out_path
    except Exception as e:
        logger.exception("transform data failed.")
        raise
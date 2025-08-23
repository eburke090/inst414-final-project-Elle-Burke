# inst414-final-project-Elle-Burke
LA Crime Data Analysis

# OVERVIEW
This project explores the patterens of firearm related deaths in the LA area from a dataset containting recent (2020-present) data.
This pipeline extracts, cleans, and models the dataset resulting in evaluation metrics and visuzaliciations. 

# PROJECT STRUCTURE
- 'data/' -> raw and processed datasets
- 'etl/' -> scripts for extracting, transforming, and modeling 
- 'requirnemnets.txt' -> needed coding packages/libraries

# SETUP INSTRUCTIONS 
1) Clone the repository 
2) install librarieis using pip install -r requirenments.txt
3) run the whole project with ETL, analysis, and visualziaotn pipeline 

# MODEL - KMEANS
Cluster incident locations (lat/longitude) to highlight hotspots
-using KMeans scikit-learn
- k's used (3,4,5,6,7)
- incident coordicnations only 

# MODEL EVAL
Select the best k using solhouette score when avaiable (the higher the better)

# BUSINESS PROBLEM
The LAPD aims to reduce response times and optimize the allocation of its patrol resources. THis project aims to build a model that can preduct and identify crime hotspots by location and time using previous crime reports


# DATA SETS USED
**Crime Data from 2020 to Present**  
    Source: data.gov (https://catalog.data.gov/dataset/crime-data-from-2020-to-present) 
    Format: CSV  
    Characteristics:
    - Structured tabular format
    - Grows over time
    - Contains fields like date, time, location, crime type, and more


# TECHNIQUES USED 

**Data Engineering:**
    - VS Code with SQL Server extension to interact with the database

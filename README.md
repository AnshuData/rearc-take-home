### Quest Take-Home Exam Submission

This repository contains my submission for the Quest Take-Home Exam, organized into three parts. 
Each part demonstrates ingestion, processing, and analysis of data using Python.

Repository Structure

├── part-1/
│   └── series_data_ingest.py       # Ingest series data from web
├── part-2/
│   └── population_data_ingest.py   # Ingest population data from api
├── part-3/
│   └── data_analytics.ipynb        # Data analysis notebook
└── README.md

## Part 1 – Series Data Ingestion

Dataset: Available in S3 at:
s3://rearc-series-data/

Script: part-1/series_data_ingest.py

Description:
Reads time-series data from web-url, performs parsing/validation, and prepares it for downstream analysis.

## Part 2 – Population Data Ingestion

Dataset: Available in S3 at:
s3://rearc-series-data/

Script: part-2/population_data_ingest.py

Description:
Ingests and processes population data using API call.

## Part 3 – Data Analytics

Notebook: part-3/data_analytics.ipynb

Description:
Provides analysis and insights as per the instructions

## Requirements
All scripts are written in Python 3.9+ and require the following packages:

boto3
requests
beautifulsoup4
loguru
pandas

Install dependencies with:

pip install -r requirements.txt

Running the Code :

Clone this repository:

git clone https://github.com/rearc-data/quest.git
cd quest

Run Part 1 ingestion: python part-1/series_data_ingest.py

Run Part 2 ingestion: python part-2/population_data_ingest.py

Open Part 3 analysis in Jupyter:

jupyter notebook part-3/data_analytics.ipynb

Notes

Ensure you have AWS credentials configured (aws configure) to allow access to the S3 bucket.
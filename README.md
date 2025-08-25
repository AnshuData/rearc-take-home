### Quest Take-Home Exam Submission

This repository contains my submission for the Quest Take-Home Exam, organized into three parts. 
Each part demonstrates ingestion, processing, and analysis of data using Python.

## Part 1 – Series Data Ingestion
Script: part-1/series_data_ingest.py

Description:
    Reads the data from public BLS data web-url, and sync with data in AWS s3 bucket.


## Part 2 – Population Data Ingestion
script : part-2/population_data_ingest.py

Description:
    Ingests and processes population data using API call.

## Part 3 – Data Analytics
Script : part-3/data_analytics.ipynb

Description:
    Provides analysis and insights as per the instructions

## Requirements
All scripts are written in Python 3.9+ and require the following packages:

boto3

requests

beautifulsoup4

loguru

pandas

aws cli

Install dependencies with:

pip install -r requirements.txt


## Running the Code :

1. Clone this repository: git clone https://github.com/AnshuData/rearc-take-home.git

2. cd rearc-take-home 

3. Run Part 1 ingestion: python part-1/series_data_ingest.py
   
    Note: We need to schedule this script in-order to continously keep in sync between source and sink; preferably using lambda function.

5. Run Part 2 ingestion: python part-2/population_data_ingest.py

6. Open Part 3 analysis in Jupyter: jupyter notebook part-3/data_analytics.ipynb

Notes : Ensure you have AWS credentials configured (aws configure) to allow access to the S3 bucket to upload files.
Notes : We can automate the ingestion scripts to run on a schedule by setting them up as AWS Glue jobs (with triggers for time-based scheduling).


Deliverables:
    1. Data in S3:
        You can view the files using the AWS CLI without credentials:

        In any Linux terminal (Note: you will need awscli installed)

        aws s3 ls s3://rearc-series-data/ --no-sign-request
        aws s3 ls s3://honolulu-population-data/ --no-sign-request


        ## Part 1 – Series Data Ingestion
        The uploaded dataset is publicly available in S3 at: s3://rearc-series-data/
        urls -
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.class
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.contacts
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.data.0.Current
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.data.1.AllData
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.duration
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.footnote
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.period
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.seasonal
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.measure
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.sector
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.series
        https://rearc-series-data.s3.us-west-2.amazonaws.com/pr.txt

        ## Part 2 – Population Data Ingestion
        The uploaded dataset is publicly available in S3 at: s3://honolulu-population-data/
        url - https://honolulu-population-data.s3.us-west-2.amazonaws.com/honolulu-population-data_20250824_170058.json


    2. Source code: 
            All source code has been made available via github link: https://github.com/AnshuData/rearc-take-home.git

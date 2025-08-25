import json
from loguru import logger
from datetime import datetime, timezone

import requests
import boto3

#configs
BUCKET = "honolulu-population-data"  
URL = ("https://honolulu-api.datausa.io/tesseract/data.jsonrecords"
       "?cube=acs_yg_total_population_1&drilldowns=Year%2CNation&locale=en&measures=Population")


def main():
    try:
        # 1) Call API
        resp = requests.get(URL, timeout=15)
        if resp.status_code == 200:

            # 2) Parse JSON
            data = resp.json()

            # 3) Timestamped filename
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"honolulu-population-data_{ts}.json"

            # 4) Upload to S3 (bucket root, no prefix/key hierarchy)
            s3 = boto3.client("s3")
            s3.put_object(
                Bucket=BUCKET,
                Key=filename,
                Body=json.dumps(data).encode("utf-8"),
                ContentType="application/json",
            )

            logger.info(f"Uploaded to s3://{BUCKET}/{filename}")

    except Exception as e:
        logger.error(f"Failed to extract data: {e}")

if __name__ == "__main__":
    main()

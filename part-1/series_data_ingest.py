import boto3
import requests
from bs4 import BeautifulSoup
from loguru import logger


S3_BUCKET = "rearc-series-data"
DATA_SOURCE = "https://download.bls.gov/pub/time.series/pr/"
USER_AGENT = "BLS-Data-Assignment/1.0 (anshujoshi432@gmail.com)"


def get_s3_bucket(bucket_name: str):
    """
    Create and return an S3 Bucket resource.

    Args:
        bucket_name (str): Name of the S3 bucket.

    Returns:
        boto3.resources.factory.s3.Bucket: S3 bucket resource object.
    """
    s3 = boto3.resource("s3")
    return s3.Bucket(bucket_name)


def get_s3_files(bucket) -> set[str]:
    """
    List all object keys currently in the given S3 bucket.

    Args:
        bucket (boto3.resources.factory.s3.Bucket): S3 bucket resource object.

    Returns:
        set[str]: Set of object keys (filenames) in the bucket.
    """
    return {obj.key for obj in bucket.objects.all()}


def get_remote_files(session: requests.Session, url: str) -> set[str]:
    """
    Scrape a remote directory listing and collect filenames.

    Args:
        session (requests.Session): Reusable requests session for HTTP calls.
        url (str): Base URL pointing to a directory listing (must end with "/").

    Returns:
        set[str]: Set of filenames found in the remote directory.
    """
    # Set a User-Agent
    resp = session.get(url, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    return {
        link.get_text().strip()
        for link in soup.find_all("a")
        if link.get_text()
        and not link.get_text().endswith("/")
        and link.get_text() != "[To Parent Directory]"
    }


def download_file(session: requests.Session, url: str, name: str) -> bytes:
    """
    Download a single file from a remote URL.

    Args:
        session (requests.Session): Reusable requests session.
        url (str): Base URL of the directory.
        name (str): Name of the file to download.

    Returns:
        bytes: Raw content of the downloaded file.
    """

    resp = session.get(url + name, headers={"User-Agent": USER_AGENT})
    resp.raise_for_status()
    return resp.content


def upload_file(bucket, name: str, content: bytes):
    """
    Upload or overwrite a file in the S3 bucket.

    Args:
        bucket (boto3.resources.factory.s3.Bucket): S3 bucket resource.
        name (str): Key (filename) under which to store the object in S3.
        content (bytes): File content to upload.

    Side Effects:
        Writes an object to the S3 bucket.
    """
    bucket.put_object(Key=name, Body=content)
    logger.info(f"Uploaded: {name}")


def delete_file(bucket, name: str):
    """
    Delete a file from the S3 bucket.

    Args:
        bucket (boto3.resources.factory.s3.Bucket): S3 bucket resource.
        name (str): Key (filename) of the object to delete.

    Side Effects:
        Removes the object from S3 if it exists.
    """
    bucket.Object(name).delete()
    logger.info(f"Deleted: {name}")


def sync_files(bucket, session, local_files: set[str], remote_files: set[str]):
    """
    Synchronize the contents of an S3 bucket with a remote directory.

    - Uploads new files from remote to S3.
    - Updates files in S3 if the remote version differs.
    - Deletes files in S3 that no longer exist in the remote source.

    Args:
        bucket (boto3.resources.factory.s3.Bucket): Target S3 bucket resource.
        session (requests.Session): Reusable requests session for HTTP calls.
        local_files (set[str]): Set of object keys currently in the S3 bucket.
        remote_files (set[str]): Set of filenames available on the remote source.

    Side Effects:
        Modifies the S3 bucket to match the remote directory.
    """
    changes_made = False  # track if any changes happened

    # Add or update
    for name in remote_files:
        content = download_file(session, DATA_SOURCE, name)
        if name not in local_files:
            upload_file(bucket, name, content)
            changes_made = True
        else:
            s3_obj = bucket.Object(name).get()
            if content != s3_obj["Body"].read():
                upload_file(bucket, name, content)
                changes_made = True

    # Delete extra
    for name in local_files - remote_files:
        delete_file(bucket, name)
        changes_made = True

    # Final message if nothing changed
    if not changes_made:
        logger.info(" All files are already in sync. No updates needed.")


def main():
    """
    Entry point for the sync job.

    Workflow:
        1. Create an S3 bucket resource (using default AWS credentials/region).
        2. Create a single reusable requests.Session for efficient HTTP calls.
        3. Get the list of files currently in the S3 bucket.
        4. Scrape the remote directory to get the list of available files.
        5. Call `sync_files` to:
            - Upload new files
            - Update changed files
            - Delete files no longer in the remote source

    Authentication:
        Boto3 automatically resolves AWS credentials & region.
        For local testing, set environment variables:

            export AWS_ACCESS_KEY_ID=...
            export AWS_SECRET_ACCESS_KEY=...
            export AWS_DEFAULT_REGION=us-east-1

        Or configure a profile via `aws configure`.


    """
    try:
        # Initialize the S3 bucket.
        bucket = get_s3_bucket(S3_BUCKET)

        # Create a reusable HTTP session for all requests.
        session = requests.Session()

        # Collect the set of files currently in the S3 bucket.
        local_files = get_s3_files(bucket)

        # Scrape the remote directory and collect all filenames
        remote_files = get_remote_files(session, DATA_SOURCE)

        # Add/update/delete files to mirror remote directory
        sync_files(bucket, session, local_files, remote_files)

    except Exception as e:
        # Catch exceptions
        logger.error(f"[ERROR] Unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

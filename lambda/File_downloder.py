import boto3
import requests

# Initialize S3 client
s3 = boto3.client('s3')

def download_and_upload(url, bucket_name, s3_key):
    """
    Download a file from a URL and upload it to S3.
    """
    try:
        # Download the file
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad HTTP responses
        
        # Log response details
        print(f"Response Content-Type: {response.headers.get('Content-Type')}")
        print(f"Response First 100 Bytes: {response.content[:100]}")  # Log first 100 bytes of content

        # Upload to S3
        s3.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=response.content,
            ContentType='application/csv'  # Adjust based on file type
        )
        print(f"File successfully uploaded to {bucket_name}/{s3_key}")   
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except boto3.exceptions.Boto3Error as e:
        print(f"Error uploading to S3: {e}")

def lambda_handler(event, context):
    """
    Main Lambda handler.
    """
    # Extract and validate input parameters
    url = event.get('url')
    bucket_name = event.get('bucket_name')
    s3_key = event.get('s3_key')  # Provide a default if missing
    
    if not url or not bucket_name:
        return {
            "statusCode": 400,
            "body": "Error: Missing required parameters 'url' or 'bucket_name'."
        }
    
    print(f"URL: {url}")
    print(f"S3 Bucket: {bucket_name}")
    print(f"S3 Key: {s3_key}")

    # Perform the download and upload
    download_and_upload(url, bucket_name, s3_key)
    
    return {
        "statusCode": 200,
        "body": f"File uploaded to {bucket_name}/{s3_key}"
    }

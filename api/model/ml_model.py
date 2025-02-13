import boto3
import os
import requests
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

def detectText(file_path):
    # Fetch AWS credentials and region from environment variables
    aws_region = os.getenv("AWS_REGION")
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    # Ensure credentials are provided
    if not all([aws_region, aws_access_key, aws_secret_key]):
        raise ValueError("AWS credentials or region not set in environment variables.")

    session =boto3.Session(
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    # Configure Textract client
    textract = session.client(
        'textract'
    )

    if file_path.startswith("http"):  # Check if it's a URL
        # Download the file from the URL
        response = requests.get(file_path)
        if response.status_code == 200:
            document_content = BytesIO(response.content)  # Convert the response content to a file-like object
            document_bytes = document_content.getvalue()  # Extract bytes from the BytesIO object
        else:
            raise OSError(f"Failed to download file: {response.status_code} {response.reason}")
    else:
        # Process local file path
        with open(file_path, 'rb') as document:
            document_content = document.read()  # Read the local file content
            document_bytes = document_content  # Store as bytes

    # Detect text from the file
    response = textract.detect_document_text(Document={'Bytes': document_bytes})

    # Extract text line by line
    text = "\n".join(
        item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"
    )

    return text

import json
import boto3
from core.Context import Context
from exceptions.exceptions import InsertErrorException


def lambda_handler(event, _):
    """Function that processes the records inserted in the DynamoDB RAW tables and processes them in the normalized tables."""

    try:
    # Iterate on all inserted records
        for record in event["Records"]:
            # separate INSERTs from other events
            if record["eventName"] == "INSERT":
                processed_profile = process_profile(record["dynamodb"]["NewImage"])
                insert_record(processed_profile)
            
    except Exception as e:
        print(e)
        return e


def process_profile(raw_profile):
    """Function to process the INSERT event of a document"""

    profile = Context(raw_profile)
    profile.process_profile()

    return profile


def insert_record(context):
    try:
        client = boto3.resource("dynamodb")
        table = client.Table("SocialProfile")
        print(table.put_item(Item=context._strategy.profile.common_processed_profile))
        
        client = boto3.resource("dynamodb")
        table = client.Table("SocialProfileMetrics")
        print(table.put_item(Item=context._strategy.profile.metric_processed_profile))

    except InsertErrorException:
        print(
            "New processed profile could not be inserted into its corresponding table"
        )
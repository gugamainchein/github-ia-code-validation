import os
import boto3
from datetime import datetime


class DynamoDBService:
    def __init__(self) -> None:
        dynamodb_resource = boto3.resource("dynamodb")
        self.dynamodb_table = dynamodb_resource.Table(
            os.environ.get("DYNAMODB_TABLE_NAME")
        )

    def save_commit_analyze(self, data_structure: dict) -> bool:
        timestamp = datetime.now().strftime("%Y-%-m-%-d %H:%M:%S")
        self.dynamodb_table.put_item(
            Item={
                "project_name": data_structure.get("project_name"),
                "project_private": data_structure.get("project_private"),
                "owner_name": data_structure.get("owner_name"),
                "owner_username": data_structure.get("owner_username"),
                "files_modified": data_structure.get("files_modified"),
                "commit_id": data_structure.get("commit_id"),
                "commit_message": data_structure.get("commit_message"),
                "commit_url": data_structure.get("commit_url"),
                "commit_changes": data_structure.get("commit_changes"),
                "bedrock_analyze": data_structure.get("bedrock_analyze"),
                "created_at": timestamp,
            },
        )

        return True

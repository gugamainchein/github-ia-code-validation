import json
from src.helpers.lambda_response import HttpResponse
from src.helpers.lambda_payload import HttpRequest
from src.services.github import GitHubService
from src.services.bedrock import BedrockService
from src.services.dynamodb import DynamoDBService


def handler(event: HttpRequest, context: None) -> HttpResponse:
    try:
        body_data = json.loads(event.get("body"))
        github_commit_values = GitHubService(commit=body_data)
        github_commit_values = github_commit_values.extract_commit_fields()
        commit_changes = github_commit_values.get("commit_changes")

        bedrock_analyze_result = BedrockService(user_prompt=commit_changes)
        bedrock_analyze_result = bedrock_analyze_result.invoke_model()

        data_structure = {
            "project_name": github_commit_values.get("project_name"),
            "project_private": github_commit_values.get("project_private"),
            "owner_name": github_commit_values.get("owner_name"),
            "owner_username": github_commit_values.get("owner_username"),
            "files_modified": github_commit_values.get("files_modified"),
            "commit_id": github_commit_values.get("commit_id"),
            "commit_message": github_commit_values.get("commit_message"),
            "commit_url": github_commit_values.get("commit_url"),
            "commit_changes": github_commit_values.get("commit_changes"),
            "bedrock_analyze": bedrock_analyze_result,
        }

        dynamodb_service = DynamoDBService()
        dynamodb_service.save_commit_analyze(data_structure=data_structure)
        response_structure = HttpResponse(body={"data": data_structure})
        return response_structure.lambda_response()
    except Exception as excep:
        response_structure = HttpResponse(body={"data": str(excep)}, status_code=500)
        return response_structure.lambda_response()

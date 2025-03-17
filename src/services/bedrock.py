import json
import boto3


class BedrockService:
    def __init__(self, user_prompt: str) -> None:
        self.bedrock_client = boto3.client("bedrock-runtime")
        self.model_id = "us.deepseek.r1-v1:0"
        self.inference_config = {"max_tokens": 4096, "temperature": 0.5}
        self.user_prompt = user_prompt

    def invoke_model(self) -> str:
        system_prompts = [
            {
                "role": "system",
                "content": """Role: You are a Senior Software Engineer specializing in code analysis and refactoring.

                              Objective: Analyze the given code and provide clear, actionable suggestions for improvement based on Domain-Driven Design (DDD) and Clean Code principles.

                              Guidelines for Feedback:
                              - Code Clarity & Readability: Suggest improvements for better readability and maintainability.
                              - Encapsulation & Modularity: Identify ways to enhance separation of concerns and modularization.
                              - DDD Best Practices: Ensure correct entity, value object, aggregate, repository, and service separation.
                              - Naming Conventions: Recommend meaningful, domain-driven names.
                              - Code Duplication & Optimization: Highlight redundant code and suggest efficient refactoring.
                              - Testability: Suggest ways to improve testability, such as dependency injection.

                              Response Format:
                              - Summarize key improvements.
                              - Provide structured suggestions with examples.
                              - If necessary, recommend alternative design patterns aligned with DDD and Clean Code.""",
            }
        ]

        user_message = [{"role": "user", "content": self.user_prompt}]

        request_body = {
            "messages": system_prompts + user_message,
            "temperature": self.inference_config.get("temperature"),
            "max_tokens": self.inference_config.get("max_tokens"),
            "top_p": 1.0,
        }

        response = self.bedrock_client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response["body"].read())
        response_text = response_body["choices"][0]["message"]["content"].strip()

        return response_text

import requests


class GitHubService:
    def __init__(self, commit: dict) -> None:
        self.commit = commit

    def request_text_from_commit_changes(self, commit_changes_url: str) -> str:
        commit_changes = requests.get(url=commit_changes_url)
        commit_changes = commit_changes.text
        return commit_changes

    def extract_commit_fields(self) -> dict:
        project_name = self.commit.get("repository").get("full_name")
        project_private = self.commit.get("repository").get("private")
        owner_name = self.commit.get("head_commit").get("author").get("name")
        owner_username = self.commit.get("head_commit").get("author").get("username")
        files_modified = self.commit.get("head_commit").get("modified")
        commit_id = self.commit.get("head_commit").get("id")
        commit_message = self.commit.get("head_commit").get("message")
        commit_url = self.commit.get("head_commit").get("url")
        commit_changes = self.request_text_from_commit_changes(
            self.commit.get("compare") + ".diff"
        )

        return {
            "project_name": project_name,
            "project_private": project_private,
            "owner_name": owner_name,
            "owner_username": owner_username,
            "files_modified": files_modified,
            "commit_id": commit_id,
            "commit_message": commit_message,
            "commit_url": commit_url,
            "commit_changes": commit_changes,
        }

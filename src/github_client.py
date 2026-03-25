"""GitHub API client for PR operations."""
import requests
from typing import List, Dict

class GitHubClient:
    BASE = "https://api.github.com"
    def __init__(self, token: str, repo: str):
        self.headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        self.repo = repo

    def get_pr_diff(self, pr_number: int) -> str:
        resp = requests.get(f"{self.BASE}/repos/{self.repo}/pulls/{pr_number}", headers={**self.headers, "Accept": "application/vnd.github.v3.diff"})
        return resp.text

    def post_pr_comment(self, pr_number: int, body: str):
        requests.post(f"{self.BASE}/repos/{self.repo}/issues/{pr_number}/comments", headers=self.headers, json={"body": body})

    def post_review_comment(self, pr_number: int, commit_sha: str, path: str, line: int, body: str):
        requests.post(f"{self.BASE}/repos/{self.repo}/pulls/{pr_number}/comments", headers=self.headers,
            json={"body": body, "commit_id": commit_sha, "path": path, "line": line, "side": "RIGHT"})

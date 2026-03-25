"""Post review comments back to GitHub."""
from src.github_client import GitHubClient
SEVERITY_EMOJI = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}

class CommentPoster:
    def __init__(self, gh_client: GitHubClient, pr_number: int):
        self.gh = gh_client
        self.pr = pr_number

    def post_comment(self, file_path: str, issue: dict):
        emoji = SEVERITY_EMOJI.get(issue.get("severity", "LOW"), "⚪")
        body = f"{emoji} **{issue.get('severity','INFO')} — {issue.get('type','')}**\n\n{issue.get('description','')}\n\n💡 **Fix:** {issue.get('fix_suggestion','')}"
        self.gh.post_pr_comment(self.pr, f"**{file_path}** — {body}")

    def post_summary(self, summary: str):
        self.gh.post_pr_comment(self.pr, f"## 🔍 AI Code Review\n\n{summary}")

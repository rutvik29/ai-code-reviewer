"""Main AI code reviewer entry point."""
import os, sys, json
from src.github_client import GitHubClient
from src.diff_parser import DiffParser
from src.llm_reviewer import LLMReviewer
from src.comment_poster import CommentPoster


def main():
    gh_token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("PR_NUMBER", 0))
    model = os.getenv("MODEL", "gpt-4o")

    if not all([gh_token, openai_key, repo, pr_number]):
        print("Missing required environment variables")
        sys.exit(1)

    print(f"Reviewing PR #{pr_number} in {repo}")

    gh = GitHubClient(token=gh_token, repo=repo)
    diff = gh.get_pr_diff(pr_number)
    files = DiffParser().parse(diff)

    reviewer = LLMReviewer(api_key=openai_key, model=model)
    poster = CommentPoster(gh_client=gh, pr_number=pr_number)

    total_issues = 0
    for file_info in files[:20]:  # limit to 20 files
        issues = reviewer.review_file(file_info)
        for issue in issues:
            poster.post_comment(file_info["path"], issue)
            total_issues += 1

    summary = reviewer.generate_summary(files, total_issues)
    poster.post_summary(summary)
    print(f"Review complete: {total_issues} issues found")


if __name__ == "__main__":
    main()

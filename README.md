# 🔍 AI Code Reviewer

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python)](https://python.org)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=flat&logo=github-actions)](https://github.com/features/actions)
[![GPT-4o](https://img.shields.io/badge/GPT--4o-Powered-412991?style=flat&logo=openai)](https://openai.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Drop this into any repo** — every PR gets automatically reviewed for bugs, security issues, performance problems, and style violations with inline GitHub comments.

## ✨ Highlights

- 🐛 **Bug detection** — null pointer risks, off-by-one errors, race conditions
- 🔒 **Security analysis** — SQL injection, hardcoded secrets, insecure deserialization
- ⚡ **Performance** — N+1 queries, unnecessary loops, memory leaks
- 🎨 **Style enforcement** — naming conventions, dead code, complexity metrics
- 💬 **Inline comments** — posts review directly on affected lines in the PR
- ✅ **Auto-approve** — optionally auto-approves clean PRs below a risk threshold
- 🔌 **Language support** — Python, JavaScript, TypeScript, Go, Java, Rust

## Installation

Add this to your repo:

```bash
# .github/workflows/ai-review.yml
name: AI Code Review
on: [pull_request]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 0}
      - uses: rutvik29/ai-code-reviewer@v1
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model: gpt-4o
          security_check: true
          auto_approve_threshold: 0.8
```

## Review Output Example

```
🔍 AI Code Review — PR #47

📊 Summary: 2 issues found (1 high, 1 low)

🔴 HIGH — security/sql_injection (line 34, auth.py)
   User input directly interpolated into SQL query.
   Fix: Use parameterized queries: cursor.execute(query, (user_id,))

🟡 LOW — performance/n_plus_one (line 89, views.py)  
   N+1 query pattern detected in loop.
   Fix: Use select_related() or prefetch_related()

✅ Overall: Changes look safe to merge after fixing HIGH issue.
```

## Configuration

```yaml
# .ai-reviewer.yml
model: gpt-4o
security_check: true
performance_check: true
style_check: true
max_files_per_review: 20
auto_approve_threshold: 0.85  # 0-1, higher = stricter
ignore_patterns:
  - "**/*.test.*"
  - "**/migrations/**"
language_specific:
  python:
    check_type_hints: true
    check_docstrings: true
```

## License

MIT © Rutvik Trivedi

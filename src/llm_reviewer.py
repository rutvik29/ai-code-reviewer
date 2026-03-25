"""LLM-based code reviewer."""
import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a senior software engineer conducting a thorough code review.
Analyze the provided code diff for:
1. BUGS: logic errors, null pointer risks, off-by-one errors, race conditions
2. SECURITY: SQL injection, XSS, hardcoded secrets, insecure deserialization, SSRF
3. PERFORMANCE: N+1 queries, unnecessary loops, memory leaks, blocking operations
4. STYLE: naming conventions, dead code, overly complex functions, missing type hints

For each issue, output JSON with: type, severity (HIGH/MEDIUM/LOW), line, description, fix_suggestion.
Output ONLY a JSON array. If no issues, output [].
Be specific and actionable. Skip trivial style nits."""),
    ("human", "File: {filename}\n\nDiff:\n{diff}\n\nFind issues (JSON array):")
])

SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful code reviewer. Generate a concise PR review summary."),
    ("human", "PR changed {num_files} files. Found {num_issues} issues. Files: {files}\n\nWrite a 2-3 sentence summary with overall assessment:")
])


class LLMReviewer:
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model, temperature=0, api_key=api_key)
        self.review_chain = REVIEW_PROMPT | self.llm
        self.summary_chain = SUMMARY_PROMPT | self.llm

    def review_file(self, file_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        try:
            result = self.review_chain.invoke({
                "filename": file_info["path"],
                "diff": file_info["diff"][:8000]  # truncate large diffs
            })
            import json
            issues = json.loads(result.content)
            return issues if isinstance(issues, list) else []
        except Exception as e:
            print(f"Review error for {file_info['path']}: {e}")
            return []

    def generate_summary(self, files: List[Dict], total_issues: int) -> str:
        result = self.summary_chain.invoke({
            "num_files": len(files),
            "num_issues": total_issues,
            "files": ", ".join(f["path"] for f in files[:10])
        })
        return result.content

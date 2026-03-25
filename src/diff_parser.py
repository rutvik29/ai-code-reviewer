"""Parse git diffs into structured file chunks."""
from typing import List, Dict

class DiffParser:
    def parse(self, diff_text: str) -> List[Dict]:
        files = []
        current_file = None
        lines = []
        for line in diff_text.split("\n"):
            if line.startswith("diff --git"):
                if current_file:
                    files.append({"path": current_file, "diff": "\n".join(lines)})
                current_file = None
                lines = []
            elif line.startswith("+++ b/"):
                current_file = line[6:].strip()
            elif current_file:
                lines.append(line)
        if current_file:
            files.append({"path": current_file, "diff": "\n".join(lines)})
        return [f for f in files if not f["path"].endswith((".lock", ".sum", ".png", ".jpg"))]

#!/usr/bin/env python3
"""
PreToolUse hook on Read: intercepts document file reads.
- Deterministic formats (DOCX, PPTX, XLSX, etc.): auto-converts via ailang, injects markdown.
- AI-requiring formats (PDF, PNG, audio, video): blocks and advises to run conversion via Bash.
"""
import json
import sys
import os
import subprocess
import glob
import tempfile

DETERMINISTIC = {'.docx', '.pptx', '.xlsx', '.doc', '.ppt', '.xls',
                 '.odt', '.odp', '.ods', '.html', '.epub', '.csv', '.tsv'}
AI_REQUIRED = {'.pdf', '.png', '.jpg', '.jpeg', '.mp3', '.wav', '.flac',
               '.aac', '.ogg', '.aiff', '.mp4', '.mov', '.avi', '.webm', '.mpeg'}
ALL_DOCS = DETERMINISTIC | AI_REQUIRED


def find_docparse():
    base = os.path.expanduser('~/.ailang/cache/registry/sunholo/ailang_parse')
    if not os.path.exists(base):
        return None
    versions = sorted(os.listdir(base), reverse=True)
    for v in versions:
        candidate = os.path.join(base, v, 'docparse/main.ail')
        if os.path.exists(candidate):
            return candidate
    return None


def main():
    data = json.loads(sys.stdin.read())

    if data.get('tool_name') != 'Read':
        sys.exit(0)

    file_path = data.get('tool_input', {}).get('file_path', '')
    if not file_path:
        sys.exit(0)

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALL_DOCS:
        sys.exit(0)

    if not os.path.exists(file_path):
        sys.exit(0)

    docparse = find_docparse()

    if ext in DETERMINISTIC and docparse:
        output_dir = tempfile.mkdtemp(prefix='claude-docparse-')
        env = os.environ.copy()
        env['DOCPARSE_OUTPUT_DIR'] = output_dir

        result = subprocess.run(
            ['ailang', 'run', '--entry', 'main', '--caps', 'IO,FS,Env', docparse, file_path],
            capture_output=True, text=True, env=env, timeout=90
        )

        if result.returncode == 0:
            output_files = glob.glob(os.path.join(output_dir, '*.md'))
            if output_files:
                latest = max(output_files, key=os.path.getmtime)
                with open(latest) as f:
                    content = f.read()
                for md in output_files:
                    os.remove(md)
                try:
                    os.rmdir(output_dir)
                except OSError:
                    pass

                out = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "block",
                        "permissionDecisionReason": f"Auto-converted {os.path.basename(file_path)} to markdown via ailang.",
                        "additionalContext": f"[Auto-converted: {file_path}]\n\n{content}"
                    }
                }
                print(json.dumps(out))
                return

    # AI-requiring format or conversion failed: block and advise
    ailang_path = docparse or 'docparse/main.ail'
    cmd = f'DOCPARSE_OUTPUT_DIR=/tmp/claude-docparse ailang run --entry main --caps IO,FS,Env,AI --ai gemini-2.5-flash {ailang_path} "{file_path}"'

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "block",
            "permissionDecisionReason": f"Document needs AI conversion before reading.",
            "additionalContext": (
                f"[Conversion required: {file_path}]\n\n"
                f"This file requires AI-powered conversion (needs GOOGLE_API_KEY). "
                f"Run via Bash then read output from /tmp/claude-docparse/:\n\n"
                f"```bash\nmkdir -p /tmp/claude-docparse\n{cmd}\n```"
            )
        }
    }
    print(json.dumps(out))


main()

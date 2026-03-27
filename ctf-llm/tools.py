# tools.py
# ============================================================
# SIMULATED AGENT TOOLS — CTF Workshop
# ============================================================
# EDUCATIONAL NOTE:
# This file contains an INTENTIONALLY VULNERABLE file reader.
# In a real application, you would ALWAYS validate and sanitize
# the file path before reading. The absence of that check here
# is the vulnerability being demonstrated (OWASP ASI04 / ASI05).
# ============================================================

import os

# Base directory the tool is "supposed" to read from.
# In a secure implementation, we would enforce this restriction.
# Here we do NOT — and that's the bug.
DOCS_BASE_DIR = os.path.join(os.path.dirname(__file__), "docs")


def get_file(filename: str) -> str:
    """
    Reads the content of a file from the server.

    INTENDED BEHAVIOR: Read files only from the docs/ folder.

    ACTUAL BEHAVIOR (VULNERABLE): Accepts any path, including
    relative paths with '../' that escape the docs/ sandbox.

    WHAT A SECURE VERSION WOULD DO:
        safe_path = os.path.realpath(os.path.join(DOCS_BASE_DIR, filename))
        if not safe_path.startswith(os.path.realpath(DOCS_BASE_DIR)):
            return "[ERROR] Access denied: path traversal detected."

    WHY THIS IS DANGEROUS (ASI04 — Excessive Agency):
    The LLM agent can be convinced by user input to call this tool
    with any path, including '../../secret/flag3.txt'. The tool
    executes without questioning the action — demonstrating that
    LLM agents must have strict boundaries on what they can do.

    WHY THIS IS DANGEROUS (ASI05 — Insufficient Output Filtering):
    The tool returns the raw file contents back to the LLM, which
    then includes it verbatim in its response to the user. There
    is no filtering of what sensitive data may be in the file.
    """

    # ⚠️  INTENTIONALLY MISSING: Path traversal protection
    # The path is used as-is, relative to the docs/ directory.
    # This means '../../secret/flag3.txt' resolves to secret/flag3.txt
    target_path = os.path.join(DOCS_BASE_DIR, filename)

    try:
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"[ERROR] Archivo no encontrado: {filename}"
    except PermissionError:
        return f"[ERROR] Sin permisos para leer: {filename}"
    except Exception as e:
        return f"[ERROR] No se pudo leer el archivo: {str(e)}"


def list_docs() -> list[str]:
    """
    Returns a list of available documents in the docs/ folder.
    Used by the RAG endpoint to know which files to read.
    """
    try:
        return [
            f for f in os.listdir(DOCS_BASE_DIR)
            if os.path.isfile(os.path.join(DOCS_BASE_DIR, f)) and f.endswith(".txt")
        ]
    except Exception:
        return []

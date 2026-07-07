"""Core services for the repo-aware AI Agent prototype."""

from .decision_log import ai_configured, build_ai_decision_log_text, build_decision_log
from .repository import (
    infer_coding_style_profile,
    iter_code_files,
    read_repo_text,
    safe_extract_zip,
    scan_repository,
)
from .retrieval import build_code_index, retrieve_relevant_chunks
from .validation import run_validation_commands, runnable_validation_commands

__all__ = [
    "ai_configured",
    "build_ai_decision_log_text",
    "build_code_index",
    "build_decision_log",
    "infer_coding_style_profile",
    "iter_code_files",
    "read_repo_text",
    "retrieve_relevant_chunks",
    "run_validation_commands",
    "runnable_validation_commands",
    "safe_extract_zip",
    "scan_repository",
]

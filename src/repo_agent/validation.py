import subprocess
from pathlib import Path


def runnable_validation_commands(repo_profile: dict) -> list[str]:
    commands: list[str] = []
    for key in ["test_commands", "lint_commands", "build_commands"]:
        for command in repo_profile.get(key, []):
            if command and "Chưa phát hiện" not in command and command not in commands:
                commands.append(command)
    return commands[:4]


def run_validation_commands(repo_path: Path, commands: list[str], timeout_sec: int = 60) -> list[dict]:
    results: list[dict] = []
    for command in commands:
        try:
            completed = subprocess.run(
                command,
                cwd=repo_path,
                shell=True,
                text=True,
                capture_output=True,
                timeout=timeout_sec,
            )
            output = (completed.stdout or "") + ("\n" + completed.stderr if completed.stderr else "")
            results.append(
                {
                    "Lệnh": command,
                    "Exit code": completed.returncode,
                    "Kết quả": "Pass" if completed.returncode == 0 else "Fail",
                    "Log": output[-5000:] if output else "(không có output)",
                }
            )
        except subprocess.TimeoutExpired as exc:
            output = (exc.stdout or "") + ("\n" + exc.stderr if exc.stderr else "")
            results.append(
                {
                    "Lệnh": command,
                    "Exit code": "timeout",
                    "Kết quả": "Timeout",
                    "Log": output[-5000:] if output else f"Lệnh vượt quá {timeout_sec} giây.",
                }
            )
    return results

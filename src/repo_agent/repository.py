import hashlib
import json
import os
import re
import zipfile
from pathlib import Path

from .config import CODE_SUFFIXES, EXCLUDED_REPO_DIRS, LANGUAGE_BY_SUFFIX, OUTPUT_DIR


def safe_extract_zip(zip_bytes: bytes, original_name: str) -> Path:
    digest = hashlib.sha256(zip_bytes).hexdigest()[:12]
    target_dir = OUTPUT_DIR / "uploaded_repos" / digest
    target_dir.mkdir(parents=True, exist_ok=True)
    zip_path = target_dir / original_name
    if not zip_path.exists():
        zip_path.write_bytes(zip_bytes)
    extract_dir = target_dir / "repo"
    extract_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            member_path = extract_dir / member.filename
            resolved = member_path.resolve()
            if not str(resolved).startswith(str(extract_dir.resolve())):
                continue
            if member.is_dir():
                resolved.mkdir(parents=True, exist_ok=True)
            else:
                resolved.parent.mkdir(parents=True, exist_ok=True)
                if not resolved.exists():
                    with archive.open(member) as src, resolved.open("wb") as dst:
                        dst.write(src.read())

    children = [p for p in extract_dir.iterdir() if p.is_dir()]
    files = [p for p in extract_dir.iterdir() if p.is_file()]
    if len(children) == 1 and not files:
        return children[0]
    return extract_dir


def scan_repository(repo_text: str) -> dict:
    repo_path = Path(repo_text.strip().strip('"')).expanduser() if repo_text.strip() else OUTPUT_DIR.parent
    result = {
        "path": repo_path,
        "exists": repo_path.exists() and repo_path.is_dir(),
        "file_count": 0,
        "languages": {},
        "configs": [],
        "top_dirs": [],
        "frameworks": [],
        "scripts": {},
        "test_commands": [],
        "lint_commands": [],
        "build_commands": [],
        "style_signals": [],
    }
    if not result["exists"]:
        return result

    suffix_counts: dict[str, int] = {}
    top_dirs: set[str] = set()
    files: list[Path] = []
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_REPO_DIRS and not d.startswith(".cache")]
        rel_root = Path(root).relative_to(repo_path)
        if rel_root.parts:
            top_dirs.add(rel_root.parts[0])
        for filename in filenames:
            path = Path(root) / filename
            files.append(path)
            suffix = path.suffix.lower()
            if suffix:
                suffix_counts[suffix] = suffix_counts.get(suffix, 0) + 1
        if len(files) >= 1500:
            break

    result["file_count"] = len(files)
    result["top_dirs"] = sorted(top_dirs)[:18]
    result["languages"] = {
        LANGUAGE_BY_SUFFIX.get(suffix, suffix): count
        for suffix, count in sorted(suffix_counts.items(), key=lambda item: item[1], reverse=True)[:8]
    }

    config_names = {
        "package.json",
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "tsconfig.json",
        "vite.config.ts",
        "next.config.js",
        "next.config.mjs",
        "tailwind.config.js",
        "tailwind.config.ts",
        "pytest.ini",
        "ruff.toml",
        ".eslintrc",
        ".eslintrc.json",
        "eslint.config.js",
        "vitest.config.ts",
        "jest.config.js",
        "Dockerfile",
    }
    result["configs"] = sorted({path.name for path in files if path.name in config_names})

    package_path = repo_path / "package.json"
    if package_path.exists():
        try:
            package_data = json.loads(package_path.read_text(encoding="utf-8"))
            deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}
            scripts = package_data.get("scripts", {})
            result["scripts"] = scripts
            if "react" in deps:
                result["frameworks"].append("React")
            if "next" in deps:
                result["frameworks"].append("Next.js")
            if "vue" in deps:
                result["frameworks"].append("Vue")
            if "express" in deps:
                result["frameworks"].append("Express")
            if "zustand" in deps:
                result["style_signals"].append("State management có dấu hiệu dùng Zustand.")
            if "tailwindcss" in deps:
                result["style_signals"].append("CSS có dấu hiệu dùng Tailwind.")
            if "typescript" in deps or (repo_path / "tsconfig.json").exists():
                result["frameworks"].append("TypeScript")
                result["style_signals"].append("Có TypeScript, nên ưu tiên type rõ ràng và không bỏ qua lỗi type.")
            for name in scripts:
                lowered = name.lower()
                if "test" in lowered:
                    result["test_commands"].append(f"npm run {name}")
                if "lint" in lowered:
                    result["lint_commands"].append(f"npm run {name}")
                if "build" in lowered:
                    result["build_commands"].append(f"npm run {name}")
        except (json.JSONDecodeError, OSError, UnicodeDecodeError):
            result["style_signals"].append("Có package.json nhưng chưa đọc được nội dung.")

    pyproject_path = repo_path / "pyproject.toml"
    requirements_path = repo_path / "requirements.txt"
    if pyproject_path.exists() or requirements_path.exists():
        result["frameworks"].append("Python")
        py_text = ""
        for path in [pyproject_path, requirements_path]:
            if path.exists():
                try:
                    py_text += "\n" + path.read_text(encoding="utf-8", errors="ignore").lower()
                except OSError:
                    pass
        if "fastapi" in py_text:
            result["frameworks"].append("FastAPI")
        if "django" in py_text:
            result["frameworks"].append("Django")
        if "pytest" in py_text or (repo_path / "pytest.ini").exists():
            result["test_commands"].append("pytest")
        if "ruff" in py_text or (repo_path / "ruff.toml").exists():
            result["lint_commands"].append("ruff check .")
        if "mypy" in py_text:
            result["lint_commands"].append("mypy .")

    if any(name in result["top_dirs"] for name in ["src", "app", "components"]):
        result["style_signals"].append("Code chính có vẻ được tách theo thư mục src/app/components.")
    if any("test" in name.lower() for name in result["top_dirs"]) or any(
        path.name.endswith((".test.ts", ".test.tsx", "_test.py")) for path in files[:500]
    ):
        result["style_signals"].append("Có cấu trúc test trong repo, AI phải thêm/sửa test cùng thay đổi logic.")

    result["frameworks"] = sorted(set(result["frameworks"])) or ["Chưa nhận diện rõ"]
    result["test_commands"] = sorted(set(result["test_commands"])) or ["Chưa phát hiện, cần hỏi người dùng"]
    result["lint_commands"] = sorted(set(result["lint_commands"])) or ["Chưa phát hiện, cần hỏi người dùng"]
    result["build_commands"] = sorted(set(result["build_commands"])) or ["Chưa phát hiện, cần hỏi người dùng"]
    result["style_signals"] = result["style_signals"] or [
        "Chưa đủ tín hiệu; cần đọc thêm code mẫu trước khi sinh code."
    ]
    return result


def iter_code_files(repo_path: Path, limit: int = 160) -> list[Path]:
    if not repo_path.exists() or not repo_path.is_dir():
        return []
    files: list[Path] = []
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_REPO_DIRS and not d.startswith(".cache")]
        for filename in filenames:
            path = Path(root) / filename
            if path.suffix.lower() in CODE_SUFFIXES and path.stat().st_size <= 240_000:
                files.append(path)
        if len(files) >= limit:
            break
    return files[:limit]


def read_repo_text(path: Path, max_chars: int = 80_000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]
    except OSError:
        return ""


def infer_coding_style_profile(repo_path: Path, repo_profile: dict) -> list[str]:
    files = iter_code_files(repo_path, limit=120)
    samples = "\n".join(read_repo_text(path, max_chars=12_000) for path in files[:80])
    signals = list(repo_profile.get("style_signals", []))

    tsconfig_path = repo_path / "tsconfig.json"
    if tsconfig_path.exists():
        tsconfig = read_repo_text(tsconfig_path, max_chars=20_000).lower()
        if '"strict": true' in tsconfig or '"strict":true' in tsconfig:
            signals.append("Dùng TypeScript strict.")

    if re.search(r"export\s+(function|const)\s+[A-Z][A-Za-z0-9_]*", samples):
        signals.append("Component có xu hướng dùng named export.")
    if re.search(r"function\s+[A-Z][A-Za-z0-9_]*\s*\(|const\s+[A-Z][A-Za-z0-9_]*\s*=", samples):
        signals.append("Component đặt tên PascalCase.")
    if re.search(r"\buse[A-Z][A-Za-z0-9_]*\s*\(", samples):
        signals.append("Hook đặt tên theo pattern useSomething.")
    if "Promise<" in samples or re.search(r"async\s+function|async\s*\(", samples):
        signals.append("API/helper bất đồng bộ nên giữ kiểu trả về async/Promise.")
    if "try {" in samples and "catch" in samples:
        signals.append("Error thường được xử lý bằng try/catch.")
    if "toast.error" in samples or "toast(" in samples:
        signals.append("Thông báo lỗi có dấu hiệu dùng toast.")
    if "className=" in samples and any(token in samples for token in ["flex ", "grid ", "text-", "bg-", "rounded-"]):
        signals.append("UI có dấu hiệu dùng Tailwind/class utility.")
    if not re.search(r"class\s+[A-Z][A-Za-z0-9_]*\s+extends\s+React", samples):
        signals.append("Không thấy class component React nổi bật; ưu tiên functional component nếu là React.")
    if any(path.name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx", "_test.py", "test.py")) for path in files):
        signals.append("Có test trong repo; AI nên thêm/sửa test cùng thay đổi logic.")
    if re.search(r"from\s+\.[\w.]+\s+import|import\s+{[^}]+}\s+from", samples):
        signals.append("Cần giữ convention import/export hiện có thay vì tạo đường dẫn mới tùy tiện.")

    deduped: list[str] = []
    for signal in signals:
        if signal and signal not in deduped:
            deduped.append(signal)
    return deduped[:10] or ["Chưa đủ code mẫu để rút style; cần retrieve thêm file liên quan."]

import re
from pathlib import Path

from .repository import iter_code_files, read_repo_text


def split_code_chunks(path: Path, repo_path: Path, text: str) -> list[dict]:
    rel = path.relative_to(repo_path).as_posix()
    pattern = re.compile(
        r"(?m)^(?:export\s+)?(?:async\s+)?(?:function|class|interface|type)\s+([A-Za-z_][\w]*)|"
        r"(?m)^(?:export\s+)?(?:const|let|var)\s+([A-Za-z_][\w]*)\s*="
    )
    matches = list(pattern.finditer(text))
    if not matches:
        return [{"path": rel, "symbol": path.stem, "kind": "file", "content": text[:4200]}]

    chunks: list[dict] = []
    for idx, match in enumerate(matches[:18]):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else min(len(text), start + 5200)
        symbol = match.group(1) or match.group(2) or path.stem
        chunks.append(
            {
                "path": rel,
                "symbol": symbol,
                "kind": "symbol",
                "content": text[start:end][:4200],
            }
        )
    return chunks


def build_code_index(repo_path: Path) -> list[dict]:
    chunks: list[dict] = []
    for path in iter_code_files(repo_path, limit=140):
        text = read_repo_text(path, max_chars=70_000)
        if text.strip():
            chunks.extend(split_code_chunks(path, repo_path, text))
        if len(chunks) >= 500:
            break
    return chunks[:500]


def tokenize_for_search(text: str) -> set[str]:
    return {token.lower() for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", text)}


def retrieve_relevant_chunks(chunks: list[dict], query: str, top_k: int = 5) -> list[dict]:
    query_terms = tokenize_for_search(query)
    if not query_terms:
        return chunks[:top_k]
    scored: list[tuple[float, dict]] = []
    for chunk in chunks:
        path_terms = tokenize_for_search(chunk["path"].replace("/", " "))
        symbol_terms = tokenize_for_search(chunk["symbol"])
        content_terms = tokenize_for_search(chunk["content"][:3000])
        score_value = (
            3.0 * len(query_terms & path_terms)
            + 2.5 * len(query_terms & symbol_terms)
            + 1.0 * len(query_terms & content_terms)
        )
        if score_value:
            scored.append((score_value, chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]] or chunks[:top_k]

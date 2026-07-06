from __future__ import annotations

import io
import os
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "outputs"
FIGURE_DIR = OUTPUT_DIR / "figures"

load_dotenv(ROOT / ".env")

REQUIRED_TABLES = {
    "task": OUTPUT_DIR / "task_ai_skill_shift.csv",
    "skill": OUTPUT_DIR / "skill_shift_summary.csv",
    "reliable_skill": OUTPUT_DIR / "reliable_skill_shift_summary.csv",
    "occupation": OUTPUT_DIR / "occupation_shift_summary.csv",
    "sector": OUTPUT_DIR / "sector_shift_summary.csv",
    "worker_group": OUTPUT_DIR / "worker_group_summary.csv",
}

OPTIONAL_TABLES = {
    "model_occupation": OUTPUT_DIR / "regression_exploratory_occupation_shift.csv",
    "model_sector": OUTPUT_DIR / "regression_exploratory_sector_shift.csv",
}

SCORE_COLUMNS = [
    "automation_exposure_index",
    "worker_pull_index",
    "human_complementarity_index",
    "innovation_momentum_index",
    "skill_shift_pressure",
]


st.set_page_config(
    page_title="Dashboard chuyển dịch kỹ năng AI",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
    [data-testid="stMetricValue"] {font-size: 1.65rem;}
    [data-testid="stMetricLabel"] {font-size: 0.82rem;}
    .small-note {color: #64748b; font-size: 0.9rem; line-height: 1.4;}
    .section-title {font-size: 1.1rem; font-weight: 700; margin: 0.4rem 0 0.2rem;}
    .insight-card {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.8rem 0.9rem;
        background: #f8fafc;
        min-height: 132px;
    }
    .insight-card strong {
        color: #0f172a;
        font-size: 0.92rem;
    }
    .insight-card p {
        color: #475569;
        font-size: 0.88rem;
        line-height: 1.35;
        margin: 0.35rem 0 0;
    }
    .agent-shell {
        border: 1px solid #1e293b;
        border-radius: 8px;
        background: #0f172a;
        color: #e5e7eb;
        padding: 0.9rem;
        margin: 0.4rem 0 1rem;
    }
    .agent-panel {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background: #ffffff;
        padding: 0.85rem;
        min-height: 116px;
    }
    .agent-panel-dark {
        border: 1px solid #334155;
        border-radius: 8px;
        background: #111827;
        color: #dbeafe;
        padding: 0.8rem;
    }
    .agent-title {
        font-size: 0.96rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .agent-muted {
        color: #94a3b8;
        font-size: 0.86rem;
        line-height: 1.35;
    }
    .agent-status {
        display: inline-block;
        border: 1px solid #38bdf8;
        border-radius: 999px;
        padding: 0.18rem 0.55rem;
        color: #bae6fd;
        font-size: 0.78rem;
        font-weight: 700;
        margin-bottom: 0.45rem;
    }
    .agent-file {
        border-left: 3px solid #38bdf8;
        padding-left: 0.55rem;
        margin: 0.3rem 0;
        color: #cbd5e1;
        font-size: 0.86rem;
    }
    .agent-trace {
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 0.65rem;
        background: #f8fafc;
        font-size: 0.88rem;
        line-height: 1.45;
    }
    .risk-note {
        border-left: 3px solid #0ea5e9;
        padding: 0.5rem 0.65rem;
        background: #f0f9ff;
        color: #0f172a;
        font-size: 0.88rem;
        line-height: 1.4;
        margin: 0.4rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def load_tables() -> tuple[dict[str, pd.DataFrame], list[Path]]:
    missing = [path for path in REQUIRED_TABLES.values() if not path.exists()]
    tables: dict[str, pd.DataFrame] = {}
    if missing:
        return tables, missing

    for name, path in REQUIRED_TABLES.items():
        tables[name] = read_csv(path)

    for name, path in OPTIONAL_TABLES.items():
        if path.exists():
            tables[name] = read_csv(path)

    return tables, []


def pct(value: float | int | None) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    return f"{value:.1%}"


def num(value: float | int | None, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "n/a"
    return f"{value:,.{digits}f}"


def choose_columns(frame: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return frame[[col for col in columns if col in frame.columns]].copy()


def filtered_tasks(
    task: pd.DataFrame,
    sectors: list[str],
    occupation_query: str,
    transition_types: list[str],
    mismatch_types: list[str],
) -> pd.DataFrame:
    out = task.copy()
    if sectors:
        out = out[out["sector"].isin(sectors)]
    if occupation_query:
        query = occupation_query.strip().lower()
        out = out[
            out["Occupation (O*NET-SOC Title)"].astype(str).str.lower().str.contains(query)
            | out["Task"].astype(str).str.lower().str.contains(query)
        ]
    if transition_types:
        out = out[out["transition_type"].isin(transition_types)]
    if mismatch_types:
        out = out[out["mismatch_type"].isin(mismatch_types)]
    return out


def filter_by_task_scope(frame: pd.DataFrame, task_scope: pd.DataFrame, key_col: str) -> pd.DataFrame:
    if frame.empty or key_col not in frame.columns:
        return frame
    if key_col == "Occupation (O*NET-SOC Title)":
        allowed = set(task_scope[key_col].dropna().unique())
    elif key_col == "sector":
        allowed = set(task_scope["sector"].dropna().unique())
    else:
        return frame
    return frame[frame[key_col].isin(allowed)].copy()


def horizontal_bar(
    frame: pd.DataFrame,
    x: str,
    y: str,
    color: str | None = None,
    title: str | None = None,
    height: int = 460,
):
    if frame.empty:
        st.info("Không có dòng nào khớp với bộ lọc hiện tại.")
        return
    fig = px.bar(
        frame.iloc[::-1],
        x=x,
        y=y,
        orientation="h",
        color=color,
        title=title,
        color_continuous_scale="Tealgrn",
    )
    fig.update_layout(height=height, margin=dict(l=8, r=8, t=48, b=8))
    st.plotly_chart(fig, width="stretch")


def first_or_na(frame: pd.DataFrame, column: str) -> str:
    if frame.empty or column not in frame.columns:
        return "n/a"
    value = frame.iloc[0][column]
    if pd.isna(value):
        return "n/a"
    return str(value)


def concise_task(text: str, max_len: int = 130) -> str:
    text = " ".join(str(text).split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 3].rstrip() + "..."


def insight_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="insight-card">
            <strong>{title}</strong>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def language_for_path(path: str) -> str:
    suffix = Path(path).suffix.lower()
    return {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".json": "json",
        ".md": "markdown",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".sql": "sql",
        ".css": "css",
        ".html": "html",
    }.get(suffix, "text")


def default_demo_repo() -> dict[str, str]:
    return {
        "README.md": """# RepoPilot demo

Repo mẫu cho giao diện Tool-based Code Agent.

Mục tiêu:
- Nạp source code thành tri thức có cấu trúc.
- Agent đọc file, tìm symbol và trả lời kèm nguồn.
- Mọi hành động rủi ro đi qua 4 thanh kiểm soát.
""",
        "src/auth/service.py": '''from src.database.user_repo import UserRepository


class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def login(self, email: str, password: str) -> dict:
        user = self.users.find_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        if not self.users.verify_password(user, password):
            raise ValueError("Invalid credentials")
        return {"user_id": user.id, "role": user.role}
''',
        "src/auth/router.py": '''from fastapi import APIRouter
from src.auth.service import AuthService

router = APIRouter()


@router.post("/login")
def login(payload: dict, auth: AuthService):
    return auth.login(payload["email"], payload["password"])
''',
        "src/database/user_repo.py": '''class UserRepository:
    def find_by_email(self, email: str):
        return None

    def verify_password(self, user, password: str) -> bool:
        return False
''',
        "tests/test_auth_login.py": '''from src.auth.service import AuthService


def test_login_invalid_user(user_repo):
    service = AuthService(user_repo)
    try:
        service.login("missing@example.com", "secret")
    except ValueError:
        assert True
''',
    }


def parse_zip_repo(uploaded_file) -> tuple[dict[str, str], list[str]]:
    files: dict[str, str] = {}
    skipped: list[str] = []
    ignored_parts = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".next",
        ".pytest_cache",
    }
    text_suffixes = {
        ".py",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".json",
        ".md",
        ".txt",
        ".toml",
        ".yaml",
        ".yml",
        ".sql",
        ".css",
        ".html",
    }

    with zipfile.ZipFile(io.BytesIO(uploaded_file.getvalue())) as archive:
        for info in archive.infolist():
            path = Path(info.filename)
            clean_name = "/".join(path.parts)
            if info.is_dir():
                continue
            if any(part in ignored_parts for part in path.parts):
                skipped.append(clean_name)
                continue
            if path.suffix.lower() not in text_suffixes:
                skipped.append(clean_name)
                continue
            if info.file_size > 200_000:
                skipped.append(clean_name)
                continue

            raw = archive.read(info.filename)
            if b"\x00" in raw[:2048]:
                skipped.append(clean_name)
                continue
            files[clean_name] = raw.decode("utf-8", errors="replace")

    return dict(sorted(files.items())), skipped


def find_symbols_for_content(path: str, content: str) -> list[dict[str, str | int]]:
    symbols: list[dict[str, str | int]] = []
    suffix = Path(path).suffix.lower()

    if suffix == ".py":
        pattern = re.compile(r"^\s*(def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE)
    elif suffix in {".js", ".jsx", ".ts", ".tsx"}:
        pattern = re.compile(
            r"^\s*(function|class)\s+([A-Za-z_][A-Za-z0-9_]*)|"
            r"^\s*const\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:async\s*)?\(",
            re.MULTILINE,
        )
    else:
        return symbols

    for match in pattern.finditer(content):
        kind = match.group(1) or "function"
        name = match.group(2) or match.group(3)
        line = content[: match.start()].count("\n") + 1
        symbols.append({"symbol": str(name), "type": str(kind), "file": path, "line": line})

    return symbols


def build_symbol_table(repo_files: dict[str, str]) -> pd.DataFrame:
    rows: list[dict[str, str | int]] = []
    for path, content in repo_files.items():
        rows.extend(find_symbols_for_content(path, content))
    if not rows:
        return pd.DataFrame(columns=["symbol", "type", "file", "line"])
    return pd.DataFrame(rows).sort_values(["file", "line"]).reset_index(drop=True)


def control_summary(strictness: int, action_risk: int, human_review: int, autonomy: int) -> str:
    strict_text = (
        "chỉ kết luận từ file đã đọc"
        if strictness >= 71
        else "ưu tiên repo nhưng cho phép suy luận nền nhẹ"
        if strictness >= 31
        else "có thể giải thích thêm kiến thức nền ngoài repo"
    )
    risk_text = (
        "chỉ đọc và giải thích"
        if action_risk <= 30
        else "được đề xuất hướng sửa"
        if action_risk <= 70
        else "có thể tạo patch hoặc chạy kiểm tra khi được duyệt"
    )
    review_text = (
        "hỏi trước mọi hành động rủi ro"
        if human_review >= 71
        else "hỏi trước khi tạo patch"
        if human_review >= 31
        else "trả lời trực tiếp với cảnh báo phù hợp"
    )
    autonomy_text = (
        "tự lập plan và đọc nhiều file liên quan"
        if autonomy >= 71
        else "đọc thêm file phụ thuộc trực tiếp"
        if autonomy >= 31
        else "chỉ xử lý đúng câu hỏi"
    )
    return (
        f"Agent hiện {strict_text}; quyền hành động là {risk_text}; "
        f"chế độ review sẽ {review_text}; mức tự chủ cho phép {autonomy_text}."
    )


def allowed_tools(action_risk: int, human_review: int) -> pd.DataFrame:
    rows = [
        ("list_files", "Thấp", "Luôn cho phép"),
        ("read_file", "Thấp", "Chỉ đọc file trong repo đã nạp"),
        ("search_code", "Thấp", "Dùng cho tìm literal, không quét secrets"),
        ("find_symbol", "Thấp", "Dùng bảng symbol đã index"),
    ]
    if action_risk >= 31:
        rows.extend(
            [
                ("find_references", "Trung bình", "Cho phép khi repo đã index"),
                ("get_dependency_graph", "Trung bình", "Cho phép xem quan hệ file/symbol"),
                ("suggest_fix", "Trung bình", "Chỉ đề xuất, chưa sửa file"),
            ]
        )
    if action_risk >= 61:
        review = "Cần người duyệt trước khi apply" if human_review >= 31 else "Chỉ tạo diff preview"
        rows.append(("create_patch", "Cao", review))
    if action_risk >= 81:
        review = "Cần xác nhận trước khi chạy" if human_review >= 71 else "Cho phép chạy lệnh test giới hạn"
        rows.append(("run_tests", "Cao", review))
    return pd.DataFrame(rows, columns=["Tool", "Rủi ro", "Điều kiện"])


def get_ai_settings() -> dict[str, str | bool | None]:
    if os.getenv("AGENT_DISABLE_AI", "").strip() == "1":
        return {
            "configured": False,
            "provider": "Disabled",
            "api_key": "",
            "base_url": None,
            "model": None,
        }

    dashscope_key = os.getenv("DASHSCOPE_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    api_key = dashscope_key or openai_key
    provider = "DashScope" if dashscope_key else "OpenAI-compatible"
    model = (
        os.getenv("DASHSCOPE_MODEL", "").strip()
        or os.getenv("OPENAI_MODEL", "").strip()
        or ("qwen-plus" if dashscope_key else "gpt-4o-mini")
    )
    base_url = os.getenv("DASHSCOPE_BASE_URL", "").strip() or os.getenv("OPENAI_BASE_URL", "").strip() or None
    return {
        "configured": bool(api_key and model),
        "provider": provider,
        "api_key": api_key,
        "base_url": base_url,
        "model": model,
    }


def truncate_text(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 80].rstrip() + "\n\n[Đã rút gọn vì file/context quá dài]"


def build_repo_context(
    repo_files: dict[str, str],
    symbol_table: pd.DataFrame,
    selected_file: str,
    question: str,
    max_chars: int = 14_000,
) -> str:
    file_list = "\n".join(f"- {path}" for path in list(repo_files)[:80])
    if len(repo_files) > 80:
        file_list += f"\n- ... còn {len(repo_files) - 80} file khác"

    symbol_view = "Chưa có symbol."
    if not symbol_table.empty:
        symbol_view = symbol_table.head(80).to_csv(index=False)

    query_terms = [part for part in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", question) if len(part) >= 3]
    related_paths = [selected_file]
    for path, content in repo_files.items():
        if path == selected_file:
            continue
        if any(re.search(rf"\b{re.escape(term)}\b", content, flags=re.IGNORECASE) for term in query_terms):
            related_paths.append(path)
        if len(related_paths) >= 5:
            break

    sections = [
        "FILE LIST:",
        file_list,
        "\nSYMBOL TABLE:",
        symbol_view,
    ]
    for path in related_paths:
        sections.extend(
            [
                f"\nFILE: {path}",
                "```",
                truncate_text(repo_files[path], 3_500),
                "```",
            ]
        )

    return truncate_text("\n".join(sections), max_chars)


def ask_configured_ai(
    repo_files: dict[str, str],
    symbol_table: pd.DataFrame,
    selected_file: str,
    question: str,
    strictness: int,
    action_risk: int,
    human_review: int,
    autonomy: int,
) -> tuple[str, pd.DataFrame, str]:
    fallback_answer, trace = analyze_agent_question(repo_files, symbol_table, selected_file, question)
    settings = get_ai_settings()

    if not settings["configured"]:
        trace.loc[len(trace)] = ("llm_completion", "Chưa cấu hình API key/model", "Dùng fallback")
        return fallback_answer, trace, "fallback"

    repo_context = build_repo_context(repo_files, symbol_table, selected_file, question)
    system_prompt = (
        "Bạn là Code Agent làm việc trên repository đã import. "
        "Chỉ kết luận dựa trên repo context được cung cấp; nếu thiếu bằng chứng thì nói rõ. "
        "Luôn trả lời bằng tiếng Việt, dễ hiểu, có file/dòng hoặc symbol khi có thể. "
        "Không tự nhận đã chạy test, tạo patch, hay đọc file ngoài context. "
        "Nếu hành động rủi ro cao, hãy nói cần human review."
    )
    user_prompt = f"""
Câu hỏi của người dùng:
{question}

File đang mở:
{selected_file}

Thanh kiểm soát:
- GitHub Strictness: {strictness}/100
- Action Risk: {action_risk}/100
- Human Review: {human_review}/100
- Autonomy: {autonomy}/100

Repo context đã index:
{repo_context}

Hãy trả lời như một AI Agent trong IDE: nêu kết luận chính trước, sau đó nêu bằng chứng file/symbol, cuối cùng nêu bước tiếp theo phù hợp với thanh kiểm soát.
"""

    try:
        client_kwargs = {"api_key": str(settings["api_key"])}
        if settings["base_url"]:
            client_kwargs["base_url"] = str(settings["base_url"])
        client_kwargs["timeout"] = 20.0
        client = OpenAI(**client_kwargs)
        response = client.chat.completions.create(
            model=str(settings["model"]),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=900,
        )
        content = response.choices[0].message.content or ""
        answer = content.strip() or fallback_answer
        trace.loc[len(trace)] = ("llm_completion", f"{settings['provider']} / {settings['model']}", "Hoàn tất")
        return answer, trace, "ai"
    except Exception as exc:
        trace.loc[len(trace)] = ("llm_completion", f"{settings['provider']} / {settings['model']}", "Lỗi, dùng fallback")
        answer = (
            f"Không gọi được AI thật ({exc.__class__.__name__}), nên app tạm dùng phân tích local.\n\n"
            f"{fallback_answer}"
        )
        return answer, trace, "fallback"


def analyze_agent_question(
    repo_files: dict[str, str],
    symbol_table: pd.DataFrame,
    selected_file: str,
    question: str,
) -> tuple[str, pd.DataFrame]:
    query = question.strip() or "Phân tích repo hiện tại"
    lower_query = query.lower()

    matched_symbol = None
    if not symbol_table.empty:
        for symbol in symbol_table["symbol"].astype(str).sort_values(key=lambda s: s.str.len(), ascending=False):
            if re.search(rf"\b{re.escape(symbol.lower())}\b", lower_query):
                matched_symbol = symbol
                break

    if matched_symbol is None and "login" in lower_query:
        matched_symbol = "login"

    trace_rows = [
        ("list_files", "Đọc cây repo và đếm file", "Hoàn tất"),
        ("read_file", selected_file, "Hoàn tất"),
    ]

    if matched_symbol:
        trace_rows.append(("find_symbol", matched_symbol, "Hoàn tất"))
        symbol_hits = (
            symbol_table[symbol_table["symbol"].astype(str).str.lower() == matched_symbol.lower()]
            if not symbol_table.empty
            else pd.DataFrame()
        )
        reference_hits = [
            path for path, content in repo_files.items() if re.search(rf"\b{re.escape(matched_symbol)}\b", content)
        ]
        trace_rows.append(("find_references", matched_symbol, "Hoàn tất"))

        if not symbol_hits.empty:
            lead = symbol_hits.iloc[0]
            ref_text = ", ".join(reference_hits[:6]) if reference_hits else "chưa thấy file khác gọi hoặc nhắc tới symbol này"
            conclusion = (
                f"Agent tìm thấy `{matched_symbol}` tại `{lead['file']}`, dòng {lead['line']}. "
                f"Các file có liên quan trực tiếp: {ref_text}. "
                "Nếu sửa phần này, nên kiểm tra route/caller, lớp repository hoặc service liên quan, rồi chạy test gần nhất trước khi tạo patch."
            )
        else:
            conclusion = (
                f"Agent chưa thấy symbol `{matched_symbol}` trong bảng symbol, nhưng đã dùng `search_code` kiểu literal để tìm trong repo. "
                f"File có nhắc tới từ khóa này: {', '.join(reference_hits[:6]) if reference_hits else 'chưa có file nào'}."
            )
    else:
        selected_symbols = (
            symbol_table[symbol_table["file"] == selected_file]["symbol"].astype(str).tolist()
            if not symbol_table.empty
            else []
        )
        trace_rows.append(("extract_outline", selected_file, "Hoàn tất"))
        if selected_symbols:
            conclusion = (
                f"Agent đã đọc `{selected_file}` và phát hiện các symbol chính: {', '.join(selected_symbols[:8])}. "
                "Hãy hỏi cụ thể tên hàm/class nếu muốn phân tích ảnh hưởng hoặc nơi được gọi."
            )
        else:
            conclusion = (
                f"Agent đã đọc `{selected_file}` nhưng chưa phát hiện function/class rõ ràng. "
                "Có thể đây là file tài liệu, cấu hình, hoặc ngôn ngữ chưa có parser trong prototype."
            )

    trace = pd.DataFrame(trace_rows, columns=["Tool", "Input", "Trạng thái"])
    return conclusion, trace


def render_code_agent_mode() -> None:
    st.title("Tool-based Code Agent IDE")
    st.caption(
        "Prototype giao diện giống VS Code: nạp source code làm tri thức, Agent đọc repo bằng tool, "
        "và 4 thanh kiểm soát quyết định mức tự chủ."
    )

    st.markdown(
        """
        <div class="agent-shell">
            <span class="agent-status">Ready for prototype</span>
            <div class="agent-title">Mục tiêu trải nghiệm</div>
            <div class="agent-muted">
                Người dùng không chỉ chat với AI. Họ nhìn thấy file nào được đọc, symbol nào được tìm,
                tool nào được gọi và quyền hành động nào đang bị chặn bởi thanh kiểm soát.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    import_col, status_col = st.columns([1.35, 0.9])
    with import_col:
        st.subheader("Nạp source code làm tri thức")
        github_url = st.text_input(
            "GitHub public URL",
            placeholder="https://github.com/org/repo",
            help="Trong prototype Streamlit này, URL được ghi nhận để mô phỏng luồng clone. ZIP upload sẽ được đọc thật.",
        )
        uploaded_zip = st.file_uploader("Upload ZIP source code", type=["zip"])
    with status_col:
        st.subheader("Trạng thái index")
        st.markdown(
            """
            <div class="agent-panel">
                <div class="agent-title">Pipeline MVP</div>
                <div class="agent-muted">
                    Import source → lọc file lớn/vendor → tạo file tree → trích symbol → Agent dùng tool để trả lời.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    skipped_files: list[str] = []
    source_status = "Demo repo mẫu"
    if uploaded_zip is not None:
        try:
            repo_files, skipped_files = parse_zip_repo(uploaded_zip)
            source_status = f"Đã nạp ZIP: {uploaded_zip.name}"
            if not repo_files:
                st.warning("ZIP không có file text/source phù hợp, nên đang hiển thị repo mẫu.")
                repo_files = default_demo_repo()
                source_status = "Demo repo mẫu"
        except zipfile.BadZipFile:
            st.error("File ZIP không đọc được. Ứng dụng đang quay về repo mẫu.")
            repo_files = default_demo_repo()
            source_status = "Demo repo mẫu"
    else:
        repo_files = default_demo_repo()
        if github_url.strip():
            source_status = "Đã nhận GitHub URL, bước MVP tiếp theo sẽ clone và index repo"

    symbol_table = build_symbol_table(repo_files)
    file_names = list(repo_files)

    top_metrics = st.columns(4)
    top_metrics[0].metric("File đã nạp", f"{len(repo_files):,}")
    top_metrics[1].metric("Symbol tìm thấy", f"{len(symbol_table):,}")
    top_metrics[2].metric("File bị bỏ qua", f"{len(skipped_files):,}")
    top_metrics[3].metric("Trạng thái", "Ready")

    left_col, center_col, right_col = st.columns([0.95, 1.65, 1.05])

    with right_col:
        st.markdown("#### 4 thanh kiểm soát")
        strictness = st.slider("GitHub Strictness", 0, 100, 82, 5)
        action_risk = st.slider("Action Risk", 0, 100, 45, 5)
        human_review = st.slider("Human Review", 0, 100, 75, 5)
        autonomy = st.slider("Autonomy", 0, 100, 60, 5)

        st.markdown(
            f"""
            <div class="risk-note">
                {control_summary(strictness, action_risk, human_review, autonomy)}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Tool được phép")
        st.dataframe(allowed_tools(action_risk, human_review), width="stretch", hide_index=True, height=300)

        st.markdown("##### Guardrail đang bật")
        guardrails = [
            "Không bịa nội dung file chưa đọc.",
            "Không apply patch trực tiếp trong prototype.",
            "Auth, security, database và payment luôn cần review.",
            "Câu trả lời phải nêu rõ file/dòng khi có bằng chứng.",
        ]
        for item in guardrails:
            st.markdown(f"- {item}")

    with left_col:
        st.markdown("#### Repo Explorer")
        st.markdown(
            f"""
            <div class="agent-panel-dark">
                <span class="agent-status">{source_status}</span>
                <div class="agent-title">File tree</div>
                <div class="agent-muted">Chọn file để xem nội dung và để Agent dùng làm bằng chứng.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        selected_file = st.selectbox("File", file_names, key="agent_selected_file")
        preview_files = file_names[:10]
        st.markdown(
            "".join(f'<div class="agent-file">{path}</div>' for path in preview_files),
            unsafe_allow_html=True,
        )
        if len(file_names) > len(preview_files):
            st.caption(f"Còn {len(file_names) - len(preview_files):,} file khác.")

        st.markdown("#### Symbol Outline")
        if symbol_table.empty:
            st.info("Chưa phát hiện function/class trong các file đã nạp.")
        else:
            st.dataframe(symbol_table.head(20), width="stretch", hide_index=True, height=260)

    with center_col:
        st.markdown("#### Editor tri thức")
        selected_content = repo_files[selected_file]
        st.code(selected_content, language=language_for_path(selected_file), line_numbers=True)

        st.markdown("#### Agent chat")
        question = st.text_area(
            "Câu hỏi cho Agent",
            value="Hàm login ảnh hưởng đến những file nào?",
            height=88,
            key="agent_question",
        )
        ai_settings = get_ai_settings()
        if ai_settings["configured"]:
            st.caption(f"AI thật đang bật: {ai_settings['provider']} / {ai_settings['model']}")
        else:
            st.warning("Chưa thấy cấu hình AI hợp lệ trong `.env`; bấm nút sẽ dùng phân tích local.")
        run_agent = st.button("Agent phân tích", type="primary", key="agent_run")

        query = question.strip() or "Phân tích repo hiện tại"
        repo_signature = f"{source_status}|{len(repo_files)}|{selected_file}"
        if run_agent:
            with st.spinner("Agent đang đọc repo, gọi tool và hỏi AI trong .env..."):
                conclusion, trace, answer_source = ask_configured_ai(
                    repo_files,
                    symbol_table,
                    selected_file,
                    query,
                    strictness,
                    action_risk,
                    human_review,
                    autonomy,
                )
            st.session_state["agent_result"] = {
                "question": query,
                "repo_signature": repo_signature,
                "conclusion": conclusion,
                "trace": trace,
                "answer_source": answer_source,
            }

        result = st.session_state.get("agent_result")
        if result and result.get("repo_signature") == repo_signature:
            if result.get("answer_source") == "ai":
                st.success("AI trong .env đã phân tích xong")
            else:
                st.warning("Đang hiển thị kết quả fallback/local vì AI chưa gọi được")
            st.markdown(f"**Câu hỏi:** {result['question']}")
            st.info(result["conclusion"])
            st.markdown('<div class="agent-trace">Tool trace của lượt phân tích</div>', unsafe_allow_html=True)
            st.dataframe(result["trace"], width="stretch", hide_index=True)
        else:
            st.markdown(
                """
                <div class="agent-trace">
                    Chưa có lượt phân tích nào cho file đang chọn. Nhấn <strong>Agent phân tích</strong>
                    để Agent đọc file, tìm symbol và trả lời kèm tool trace.
                </div>
                """,
                unsafe_allow_html=True,
            )

st.sidebar.title("Chế độ")
app_mode = st.sidebar.radio("Chọn giao diện", ["Dashboard phân tích", "Code Agent IDE"], index=0)
if app_mode == "Code Agent IDE":
    render_code_agent_mode()
    st.stop()


tables, missing_tables = load_tables()
if missing_tables:
    st.title("Dashboard chuyển dịch kỹ năng AI")
    st.error("Thiếu file output bắt buộc. Hãy chạy pipeline hoặc notebook phân tích trước.")
    st.write([str(path) for path in missing_tables])
    st.stop()

task = tables["task"]
skill = tables["skill"]
reliable_skill = tables["reliable_skill"]
occupation = tables["occupation"]
sector = tables["sector"]
worker_group = tables["worker_group"]
model_occupation = tables.get("model_occupation", pd.DataFrame())
model_sector = tables.get("model_sector", pd.DataFrame())


st.sidebar.title("Bộ lọc")
all_sectors = sorted(task["sector"].dropna().astype(str).unique())
selected_sectors = st.sidebar.multiselect("Ngành", all_sectors)
occupation_query = st.sidebar.text_input("Tìm nghề hoặc task")

transition_options = sorted(task["transition_type"].dropna().astype(str).unique())
selected_transitions = st.sidebar.multiselect("Loại chuyển dịch", transition_options)

mismatch_options = sorted(task["mismatch_type"].dropna().astype(str).unique())
selected_mismatches = st.sidebar.multiselect("Loại lệch pha", mismatch_options)

top_n = st.sidebar.slider("Số dòng top trong biểu đồ", min_value=5, max_value=30, value=15, step=5)
show_reliable_only = st.sidebar.checkbox("Chỉ dùng ranking đủ tin cậy", value=True)

task_scope = filtered_tasks(
    task,
    selected_sectors,
    occupation_query,
    selected_transitions,
    selected_mismatches,
)

occupation_scope = filter_by_task_scope(occupation, task_scope, "Occupation (O*NET-SOC Title)")
sector_scope = filter_by_task_scope(sector, task_scope, "sector")

st.title("Dashboard chuyển dịch kỹ năng khi có AI")
st.caption(
    "Trực quan hóa task, kỹ năng, nghề, ngành, nhóm worker và kết quả mô hình khám phá."
)

with st.expander("Các chỉ số này nói gì?", expanded=False):
    st.markdown(
        """
        - `automation_exposure_index`: AI đã có nhiều tín hiệu có thể tham gia vào task này.
        - `worker_pull_index`: người làm việc có xu hướng muốn AI hỗ trợ hoặc tự động hóa task này.
        - `human_complementarity_index`: task vẫn cần con người vì chuyên môn, giao tiếp, phán đoán hoặc kiểm soát chất lượng.
        - `skill_shift_pressure`: áp lực thay đổi kỹ năng/task càng cao khi automation exposure và worker pull cao nhưng human complementarity thấp hơn.
        - `exploratory_shift_score`: điểm xếp hạng từ mô hình khám phá; dùng để chọn nơi cần xem sâu hơn, không phải dự báo chắc chắn.
        """
    )


metric_cols = st.columns(6)
metric_cols[0].metric("Task", f"{len(task_scope):,}", f"{len(task):,} tổng")
metric_cols[1].metric(
    "Nghề",
    f"{task_scope['Occupation (O*NET-SOC Title)'].nunique():,}",
    f"{task['Occupation (O*NET-SOC Title)'].nunique():,} tổng",
)
metric_cols[2].metric("Ngành", f"{task_scope['sector'].nunique():,}", f"{task['sector'].nunique():,} tổng")
metric_cols[3].metric("Tín hiệu worker", pct(task_scope["has_worker_signal"].mean()))
metric_cols[4].metric("Tín hiệu expert", pct(task_scope["has_expert_signal"].mean()))
metric_cols[5].metric("Cặp worker + expert", pct(task_scope["paired_worker_expert_signal"].mean()))

summary_skill = (reliable_skill.copy() if show_reliable_only else skill.copy()).sort_values(
    "skill_shift_pressure", ascending=False
)
summary_occupation = occupation_scope.sort_values("skill_shift_pressure", ascending=False)
summary_sector = sector_scope.sort_values("skill_shift_pressure", ascending=False)
transition_leader = (
    task_scope["transition_type"].value_counts(dropna=True).idxmax()
    if not task_scope.empty and task_scope["transition_type"].notna().any()
    else "n/a"
)
mismatch_leader = (
    task_scope["mismatch_type"].value_counts(dropna=True).idxmax()
    if not task_scope.empty and task_scope["mismatch_type"].notna().any()
    else "n/a"
)

st.subheader("Diễn giải nhanh")
card_cols = st.columns(4)
with card_cols[0]:
    insight_card(
        "Tín hiệu kỹ năng chính",
        "Kỹ năng có áp lực chuyển dịch cao nhất trong bộ lọc hiện tại: "
        f"{first_or_na(summary_skill, 'skill_list')}. Nên đọc như ưu tiên reskilling, không phải kết luận thay thế con người.",
    )
with card_cols[1]:
    insight_card(
        "Nghề cần chú ý",
        "Nghề có áp lực chuyển dịch cao nhất: "
        f"{first_or_na(summary_occupation, 'Occupation (O*NET-SOC Title)')}. Xem bảng task để biết task nào đang kéo điểm lên.",
    )
with card_cols[2]:
    insight_card(
        "Mẫu hình theo ngành",
        "Ngành nổi bật nhất trong bộ lọc: "
        f"{first_or_na(summary_sector, 'sector')}. Điểm ngành là trung bình từ nhiều task, nên ngành có mẫu nhỏ cần đọc thận trọng.",
    )
with card_cols[3]:
    insight_card(
        "Cách đọc chủ đạo",
        f"Loại chuyển dịch phổ biến nhất: {transition_leader}. Lệch pha phổ biến nhất: {mismatch_leader}. Các nhãn này tóm tắt pattern ở cấp task.",
    )


tabs = st.tabs(["Tổng quan", "Khám phá dữ liệu"])


with tabs[0]:
    st.markdown(
        """
        **Ý nghĩa chính:** dashboard này cho thấy task nào có khả năng đổi cách làm khi AI tham gia.
        Nếu một task vừa có tín hiệu AI mạnh vừa được worker muốn tự động hóa, nó đáng được xem như ứng viên
        để thiết kế lại quy trình. Nếu task vẫn cần human complementarity cao, hướng phù hợp hơn thường là
        AI hỗ trợ con người thay vì thay thế hoàn toàn.
        """
    )
    left, right = st.columns([1.35, 1])

    with left:
        plot_data = task_scope.dropna(
            subset=["automation_exposure_index", "human_complementarity_index"]
        ).copy()
        if plot_data.empty:
            st.info("Không có task đủ dữ liệu chỉ số để vẽ quadrant plot.")
        else:
            plot_data["bubble_size"] = (
                plot_data["worker_pull_index"].fillna(plot_data["worker_pull_index"].median())
                .clip(lower=0)
                .mul(28)
                .add(6)
            )
            fig = px.scatter(
                plot_data,
                x="automation_exposure_index",
                y="human_complementarity_index",
                size="bubble_size",
                color="skill_shift_pressure",
                hover_name="Task",
                hover_data={
                    "Occupation (O*NET-SOC Title)": True,
                    "sector": True,
                    "worker_pull_index": ":.3f",
                    "skill_shift_pressure": ":.3f",
                    "bubble_size": False,
                },
                color_continuous_scale="Viridis",
                title="Quadrant task: automation exposure và human complementarity",
            )
            fig.add_vline(x=0.6, line_width=1, line_dash="dash", line_color="#94a3b8")
            fig.add_hline(y=0.6, line_width=1, line_dash="dash", line_color="#94a3b8")
            fig.update_layout(height=580, margin=dict(l=8, r=8, t=48, b=8))
            st.plotly_chart(fig, width="stretch")
            st.caption(
                "Góc phải-trên gợi ý AI hỗ trợ con người; góc phải-dưới nghiêng về tự động hóa nhiều hơn; góc trái-trên là vùng kỹ năng con người còn bền."
            )

    with right:
        transition_counts = (
            task_scope["transition_type"]
            .value_counts(dropna=False)
            .rename_axis("transition_type")
            .reset_index(name="tasks")
        )
        fig = px.bar(
            transition_counts,
            x="tasks",
            y="transition_type",
            orientation="h",
            title="Phân bố loại chuyển dịch",
            color="tasks",
            color_continuous_scale="Blues",
        )
        fig.update_layout(height=270, margin=dict(l=8, r=8, t=44, b=8), showlegend=False)
        st.plotly_chart(fig, width="stretch")
        st.caption(
            "Mỗi nhãn tóm tắt một kiểu thay đổi có thể xảy ra ở cấp task, giúp thấy nhanh nhóm task nào cần ưu tiên phân tích."
        )

        mismatch_counts = (
            task_scope["mismatch_type"]
            .value_counts(dropna=False)
            .rename_axis("mismatch_type")
            .reset_index(name="tasks")
        )
        fig = px.bar(
            mismatch_counts,
            x="tasks",
            y="mismatch_type",
            orientation="h",
            title="Lệch pha giữa khả năng AI và mong muốn worker",
            color="tasks",
            color_continuous_scale="Oranges",
        )
        fig.update_layout(height=300, margin=dict(l=8, r=8, t=44, b=8), showlegend=False)
        st.plotly_chart(fig, width="stretch")
        st.caption(
            "Lệch pha cho biết worker desire, expert capability và nhu cầu human agency đang cùng hướng hay ngược hướng."
        )

    st.subheader("Các ranking chính")
    st.markdown(
        "Ba ranking này trả lời ba câu hỏi khác nhau: **kỹ năng** nào cần reskilling, **nghề** nào có cụm task dễ chuyển dịch hơn, và **ngành** nào có áp lực rộng hơn."
    )
    skill_col, occ_col, sec_col = st.columns(3)

    with skill_col:
        skill_scope = reliable_skill.copy() if show_reliable_only else skill.copy()
        skill_scope = skill_scope.sort_values("skill_shift_pressure", ascending=False).head(top_n)
        horizontal_bar(
            skill_scope,
            x="skill_shift_pressure",
            y="skill_list",
            color="automation_exposure_index",
            title="Kỹ năng",
            height=430,
        )

    with occ_col:
        occ_rank = occupation_scope.sort_values("skill_shift_pressure", ascending=False).head(top_n)
        horizontal_bar(
            occ_rank,
            x="skill_shift_pressure",
            y="Occupation (O*NET-SOC Title)",
            color="automation_exposure_index",
            title="Nghề",
            height=430,
        )

    with sec_col:
        sec_rank = sector_scope.sort_values("skill_shift_pressure", ascending=False).head(top_n)
        horizontal_bar(
            sec_rank,
            x="skill_shift_pressure",
            y="sector",
            color="automation_exposure_index",
            title="Ngành",
            height=430,
        )

    st.subheader("Độ phủ theo loại tín hiệu")
    st.caption(
        "Coverage là kiểm tra chất lượng dữ liệu. Coverage thấp nghĩa là điểm số trong bộ lọc hiện tại có ít bằng chứng hơn."
    )
    coverage = (
        task_scope[
            [
                "has_worker_signal",
                "has_expert_signal",
                "has_usage_signal",
                "has_paper_signal",
                "has_company_signal",
                "paired_worker_expert_signal",
            ]
        ]
        .mean()
        .mul(100)
        .round(1)
        .rename("coverage_pct")
        .reset_index()
        .rename(columns={"index": "signal"})
    )
    st.dataframe(coverage, width="stretch", hide_index=True)

    with st.expander("Hình đã tạo từ pipeline"):
        figure_paths = [
            FIGURE_DIR / "task_skill_shift_quadrant.png",
            FIGURE_DIR / "capability_desire_mismatch.png",
            FIGURE_DIR / "top_skill_shift_pressure.png",
        ]
        cols = st.columns(3)
        for col, path in zip(cols, figure_paths):
            with col:
                if path.exists():
                    st.image(str(path), caption=path.name, width="stretch")
                else:
                    st.warning(f"Thiếu {path.name}")


with tabs[1]:
    st.markdown(
        """
        **Đi sâu vào bằng chứng:** tab này cho phép xem task cụ thể đứng sau các kết luận tổng quan.
        Những task có `skill_shift_pressure` cao là nơi quy trình làm việc có thể thay đổi mạnh hơn.
        Những task có `human_complementarity_index` cao là nơi con người vẫn giữ vai trò quan trọng.
        """
    )
    task_section, model_section, table_section = st.columns([1.2, 1, 0.9])

    with task_section:
        st.subheader("Khám phá task")
        if not task_scope.empty:
            task_leader = task_scope.sort_values("skill_shift_pressure", ascending=False).iloc[0]
            st.info(
                "Task có áp lực cao nhất trong bộ lọc hiện tại: "
                f"{concise_task(task_leader['Task'])} "
                f"({task_leader['Occupation (O*NET-SOC Title)']})."
            )
        sort_options = [col for col in SCORE_COLUMNS if col in task_scope.columns]
        sort_by = st.selectbox(
            "Sắp xếp task theo",
            sort_options,
            index=sort_options.index("skill_shift_pressure"),
            key="task_sort_by",
        )
        ascending = st.checkbox("Tăng dần", value=False, key="task_ascending")

        task_view = task_scope.sort_values(sort_by, ascending=ascending)
        st.dataframe(
            choose_columns(
                task_view,
                [
                    "Task ID",
                    "Occupation (O*NET-SOC Title)",
                    "sector",
                    "Task",
                    "automation_exposure_index",
                    "worker_pull_index",
                    "human_complementarity_index",
                    "innovation_momentum_index",
                    "skill_shift_pressure",
                    "ai_capability_score",
                    "worker_desire_score",
                    "human_agency_score",
                    "transition_type",
                    "mismatch_type",
                    "signal_count",
                ],
            ),
            width="stretch",
            hide_index=True,
            height=680,
        )

    with model_section:
        st.subheader("Mô hình khám phá")
        st.caption(
            "Ranking này chỉ mang tính khám phá, không phải bằng chứng nhân quả hay xác suất mất việc. Nên dùng để chọn nơi cần phân tích sâu hơn."
        )
        if model_occupation.empty or model_sector.empty:
            st.warning("Chưa thấy CSV output của mô hình. Hãy chạy lại ai_skill_shift_research.ipynb.")
        else:
            model_occ = model_occupation.copy()
            model_sec = model_sector.copy()
            if selected_sectors:
                model_occ = model_occ[model_occ["sector"].isin(selected_sectors)]
                model_sec = model_sec[model_sec["sector"].isin(selected_sectors)]
            if occupation_query:
                q = occupation_query.strip().lower()
                model_occ = model_occ[model_occ["occupation"].astype(str).str.lower().str.contains(q)]

            if show_reliable_only and "reliable_for_ranking" in model_occ.columns:
                model_occ = model_occ[model_occ["reliable_for_ranking"]]
            if show_reliable_only and "reliable_for_ranking" in model_sec.columns:
                model_sec = model_sec[model_sec["reliable_for_ranking"]]

            if not model_occ.empty:
                model_leader = model_occ.sort_values("exploratory_shift_score", ascending=False).iloc[0]
                st.info(
                    "Mô hình hiện xếp cao nhất: "
                    f"{model_leader['occupation']} với điểm {num(model_leader['exploratory_shift_score'])}. "
                    "Cần kiểm tra responses/users/tasks trước khi xem thứ hạng này là ổn định."
                )

            top_model_occ = model_occ.sort_values("exploratory_shift_score", ascending=False).head(top_n)
            horizontal_bar(
                top_model_occ,
                x="exploratory_shift_score",
                y="occupation",
                color="ai_capability",
                title="Nghề theo exploratory score",
                height=390,
            )
            top_model_sec = model_sec.sort_values("exploratory_shift_score", ascending=False).head(top_n)
            horizontal_bar(
                top_model_sec,
                x="exploratory_shift_score",
                y="sector",
                color="ai_capability",
                title="Ngành theo exploratory score",
                height=310,
            )

    with table_section:
        st.subheader("Bảng dữ liệu")
        st.caption(
            "Dùng `task` để xem bằng chứng chi tiết, `reliable_skill` cho ranking kỹ năng chính, `occupation`/`sector` cho tổng hợp theo nhóm, và bảng model cho ranking fitted-score khám phá."
        )
        table_name = st.selectbox("Bảng", sorted(tables.keys()), key="data_table_name")
        selected_table = tables[table_name]
        st.write(f"{table_name}: {selected_table.shape[0]:,} dòng x {selected_table.shape[1]:,} cột")
        st.download_button(
            "Tải CSV",
            selected_table.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            file_name=f"{table_name}.csv",
            mime="text/csv",
            key="download_table",
        )
        st.dataframe(selected_table, width="stretch", hide_index=True, height=620)


import os

import pandas as pd
from openai import OpenAI

from .validation import runnable_validation_commands


def build_decision_log(
    user_task: str,
    repo_profile: dict,
    style_profile: dict,
    selected_control: str,
    selected_control_row: pd.Series,
    retrieved_chunks: list[dict],
) -> dict:
    files = [f"{chunk['path']} :: {chunk['symbol']}" for chunk in retrieved_chunks]
    validation = runnable_validation_commands(repo_profile)
    style_lines = [
        line.strip("- ").strip()
        for line in str(style_profile.get("Coding style rút ra", "")).splitlines()
        if line.strip()
    ]
    return {
        "title": user_task.strip() or "Tác vụ chưa đặt tên",
        "files": files,
        "reasons": [
            f"Giữ đúng repo style: {', '.join(style_lines[:3]) if style_lines else style_profile.get('Framework/ngôn ngữ', 'chưa rõ')}.",
            f"Chỉ dùng context đã retrieve từ {len(files)} đoạn code liên quan thay vì nhét toàn bộ repo vào prompt.",
            f"Tuân thủ mức kiểm soát {selected_control}: {selected_control_row['AI được làm']}",
        ],
        "tradeoffs": [
            "Không fine-tune model ngay, vì repo thay đổi thường xuyên và RAG cập nhật nhanh hơn.",
            "Không tạo abstraction mới nếu chưa thấy pattern tương tự trong các file retrieve được.",
            "Nếu thiếu file liên quan, AI phải yêu cầu retrieve thêm thay vì đoán kiến trúc.",
        ],
        "risks": [
            "Có thể retrieve thiếu context nếu tên task quá chung chung.",
            "Code sinh ra phải qua test/lint/build trước khi được merge.",
            f"Con người vẫn giữ quyền: {selected_control_row['Con người phải làm']}",
        ],
        "validation": validation
        or ["Chưa phát hiện lệnh test/lint/build; cần khai báo trong package.json hoặc pyproject.toml."],
    }


def ai_configured() -> bool:
    return bool(os.getenv("DASHSCOPE_API_KEY") and os.getenv("DASHSCOPE_BASE_URL") and os.getenv("DASHSCOPE_MODEL"))


def build_ai_decision_log_text(
    user_task: str,
    repo_profile: dict,
    style_profile: dict,
    selected_control: str,
    selected_control_row: pd.Series,
    retrieved_chunks: list[dict],
) -> str:
    if not ai_configured():
        raise RuntimeError("Thiếu DASHSCOPE_API_KEY, DASHSCOPE_BASE_URL hoặc DASHSCOPE_MODEL trong .env.")

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv("DASHSCOPE_BASE_URL"),
    )
    context_snippets = "\n\n".join(
        f"### {chunk['path']} :: {chunk['symbol']}\n```text\n{chunk['content'][:1600]}\n```"
        for chunk in retrieved_chunks[:5]
    )
    if not context_snippets:
        context_snippets = "Chưa retrieve được code context; hãy nói rõ cần retrieve thêm trước khi code."

    validation = runnable_validation_commands(repo_profile)
    prompt = f"""Hãy viết một PR Decision Log bằng tiếng Việt cho AI coding agent.

Tác vụ/PR:
{user_task}

Repo style:
- Framework/ngôn ngữ: {style_profile.get("Framework/ngôn ngữ", "chưa rõ")}
- Cấu trúc project: {style_profile.get("Cấu trúc project", "chưa rõ")}
- Config quan trọng: {style_profile.get("Config quan trọng", "chưa rõ")}
- Coding style rút ra:
{style_profile.get("Coding style rút ra", "chưa rõ")}
- Skill/convention bổ sung: {style_profile.get("Skill/convention bổ sung", "chưa khai báo")}

Mức kiểm soát AI Agent:
- {selected_control}
- AI được làm: {selected_control_row['AI được làm']}
- Con người phải làm: {selected_control_row['Con người phải làm']}

Code context retrieve từ repo:
{context_snippets}

Validation cần chạy:
{chr(10).join(f"- {cmd}" for cmd in validation) if validation else "- Chưa phát hiện lệnh test/lint/build; cần yêu cầu người dùng bổ sung."}

Yêu cầu output:
- Có tiêu đề PR.
- Có mục File/context được dùng.
- Có mục Lý do chọn hướng xử lý.
- Có mục Trade-off.
- Có mục Rủi ro & cách kiểm soát.
- Có mục Validation.
- Có mục Kết luận ngắn về mức độ tin cậy.
- Không bịa file không có trong context.
- Nếu context thiếu, nói rõ cần retrieve thêm.
"""
    response = client.chat.completions.create(
        model=os.getenv("DASHSCOPE_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "Bạn là senior software engineer viết PR Decision Log rõ ràng, ngắn gọn, có trách nhiệm chất lượng.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""

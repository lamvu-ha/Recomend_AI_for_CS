from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

import src.repo_agent as repo_agent


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
load_dotenv(BASE_DIR / ".env")

PALETTE = {
    "ink": "#17324D",
    "teal": "#129C9A",
    "coral": "#EF6F52",
    "gold": "#DDBF6F",
    "slate": "#69717D",
    "mist": "#E8EEF2",
    "paper": "#FBFAF7",
}

REC_COLORS = {
    "Agent bán tự động": PALETTE["teal"],
    "Copilot + review bắt buộc": PALETTE["coral"],
    "Con người dẫn dắt, AI hỗ trợ": PALETTE["gold"],
    "Thử nghiệm / theo dõi": PALETTE["slate"],
    "Cần thêm dữ liệu": "#B8B8B8",
}

REG_FEATURES = [
    "automation_exposure_index",
    "worker_pull_index",
    "human_complementarity_index",
    "innovation_momentum_index",
    "expert_uncertainty_requirement",
    "expert_domain_expertise_requirement",
    "quality_critical_task",
]

FEATURE_LABELS = {
    "automation_exposure_index": "Mức tiếp xúc AI",
    "worker_pull_index": "Worker muốn AI",
    "human_complementarity_index": "Mức cần con người",
    "innovation_momentum_index": "Động lực đổi mới",
    "expert_uncertainty_requirement": "Độ bất định",
    "expert_domain_expertise_requirement": "Yêu cầu chuyên môn miền",
    "quality_critical_task": "Task critical về chất lượng",
}


st.set_page_config(
    page_title="AI Agent và sự dịch chuyển kỹ năng",
    page_icon="",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #17324D;
        --teal: #129C9A;
        --coral: #EF6F52;
        --gold: #DDBF6F;
        --paper: #FBFAF7;
    }
    .stApp {
        background: #FBFAF7;
        color: var(--ink);
    }
    h1, h2, h3 {
        color: var(--ink);
        letter-spacing: 0;
    }
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E6E1D8;
        padding: 14px 16px;
        border-radius: 8px;
        box-shadow: 0 1px 2px rgba(23, 50, 77, 0.06);
    }
    .explain-box {
        background: #FFFFFF;
        border-left: 5px solid var(--teal);
        border-radius: 8px;
        padding: 16px 18px;
        margin: 8px 0 18px 0;
        box-shadow: 0 1px 2px rgba(23, 50, 77, 0.06);
    }
    .warning-box {
        background: #FFF7EE;
        border-left: 5px solid var(--coral);
        border-radius: 8px;
        padding: 16px 18px;
        margin: 8px 0 18px 0;
    }
    .path-card {
        background: #FFFFFF;
        border: 1px solid #E6E1D8;
        border-radius: 8px;
        padding: 14px 16px;
        height: 100%;
    }
    .path-title {
        font-weight: 700;
        color: var(--ink);
        margin-bottom: 8px;
    }
    .small-note {
        color: #59646F;
        font-size: 0.94rem;
    }
    .solution-panel {
        background: #FFFFFF;
        border: 1px solid #D7DEE8;
        border-radius: 8px;
        padding: 16px;
        min-height: 620px;
    }
    .solution-title {
        font-weight: 700;
        color: var(--ink);
        border-bottom: 1px solid #E5EAF0;
        margin: -16px -16px 16px -16px;
        padding: 12px 16px;
    }
    .level-rail {
        height: 12px;
        border-radius: 999px;
        background: linear-gradient(90deg, #4FC16E 0%, #F4C542 50%, #EF6F52 100%);
        margin: 18px 6px 8px 6px;
        position: relative;
    }
    .level-marker {
        width: 22px;
        height: 22px;
        border-radius: 999px;
        border: 3px solid #17324D;
        background: #FFFFFF;
        position: relative;
        top: -5px;
        box-shadow: 0 1px 4px rgba(23, 50, 77, 0.24);
    }
    .level-labels {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        color: #6B7280;
        font-size: 0.78rem;
        margin: 0 2px 12px 2px;
        text-align: center;
    }
    .selected-level {
        background: #EAF2FF;
        border-radius: 8px;
        padding: 14px 16px;
        color: #174A8B;
        margin: 14px 0;
    }
    .compact-row {
        display: grid;
        grid-template-columns: 1.3fr 0.55fr 0.55fr 0.55fr 0.75fr;
        gap: 8px;
        align-items: center;
        border: 1px solid #DFE6EF;
        border-left: 4px solid #EF6F52;
        border-radius: 7px;
        padding: 10px 12px;
        margin: 8px 0;
        font-size: 0.86rem;
    }
    .level-pill {
        background: #EF3F3F;
        color: #FFFFFF;
        border-radius: 7px;
        padding: 6px 8px;
        text-align: center;
        font-weight: 700;
        font-size: 0.78rem;
    }
    .pr-card {
        border: 1px solid #D7DEE8;
        border-radius: 8px;
        padding: 14px 16px;
        background: #FFFFFF;
        margin-top: 16px;
    }
    .pr-header {
        background: #2F73B9;
        color: #FFFFFF;
        border-radius: 5px;
        padding: 10px 12px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .success-note {
        background: #F0FFF5;
        border: 1px dashed #2DBE65;
        border-radius: 6px;
        padding: 10px 12px;
        margin-top: 14px;
        text-align: center;
        color: #24583B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def read_csv(name: str) -> pd.DataFrame:
    path = OUTPUT_DIR / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_data() -> dict[str, pd.DataFrame]:
    return {
        "tasks": read_csv("cs_agent_task_recommendations.csv"),
        "task_groups": read_csv("cs_task_group_summary.csv"),
        "occupations": read_csv("cs_occupation_agent_summary.csv"),
        "ols": read_csv("cs_regression_quality_risk_ols.csv"),
        "logit": read_csv("cs_regression_copilot_review_logit.csv"),
        "reg_ref": read_csv("cs_regression_reference.csv"),
        "pathway": read_csv("cs_skill_shift_pathway.csv"),
        "reskill_occ": read_csv("cs_reskilling_priority_by_occupation.csv"),
        "reskill_group": read_csv("cs_reskilling_priority_by_task_group.csv"),
        "reskill_task": read_csv("cs_reskilling_priority_by_task.csv"),
        "raw_tasks": read_csv("task_ai_skill_shift.csv"),
    }


def pct(value: float) -> str:
    if pd.isna(value):
        return "Chưa đủ dữ liệu"
    return f"{value:.1%}"


def score(value: float) -> str:
    if pd.isna(value):
        return "NA"
    return f"{value:.2f}"


def clean_tasks(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    for col in [
        "code_acceleration_potential",
        "quality_risk_need",
        "automation_exposure_index",
        "worker_pull_index",
        "human_complementarity_index",
        "innovation_momentum_index",
        "expert_uncertainty_requirement",
        "expert_domain_expertise_requirement",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    if "quality_critical_task" in df.columns:
        df["quality_critical_task"] = df["quality_critical_task"].fillna(False).astype(bool)
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    filtered = df.copy()
    with st.sidebar:
        st.header("Bộ lọc")
        groups = sorted(filtered["task_group_vi"].dropna().unique().tolist())
        selected_groups = st.multiselect(
            "Nhóm task",
            groups,
            default=groups,
            help="Lọc theo nhóm công việc trong ngành khoa học máy tính.",
        )
        if selected_groups:
            filtered = filtered[filtered["task_group_vi"].isin(selected_groups)]

        recs = list(REC_COLORS.keys())
        selected_recs = st.multiselect(
            "Khuyến nghị AI Agent",
            recs,
            default=recs,
            help="So sánh các mức triển khai AI Agent khác nhau.",
        )
        if selected_recs:
            filtered = filtered[filtered["agent_recommendation"].isin(selected_recs)]

        occ_options = sorted(filtered["Occupation (O*NET-SOC Title)"].dropna().unique().tolist())
        selected_occ = st.selectbox(
            "Nghề cụ thể",
            ["Tất cả"] + occ_options,
            help="Chọn một nghề để xem task liên quan rõ hơn.",
        )
        if selected_occ != "Tất cả":
            filtered = filtered[filtered["Occupation (O*NET-SOC Title)"].eq(selected_occ)]

        st.caption("Các bộ lọc này áp dụng cho bảng task và bản đồ AI Agent ở tab 1.")
    return filtered


def metric_row(tasks: pd.DataFrame, filtered: pd.DataFrame) -> None:
    total = len(tasks)
    visible = len(filtered)
    review_count = int(filtered["agent_recommendation"].eq("Copilot + review bắt buộc").sum())
    critical_share = filtered["quality_critical_task"].mean() if visible else np.nan
    avg_accel = filtered["code_acceleration_potential"].mean() if visible else np.nan
    avg_risk = filtered["quality_risk_need"].mean() if visible else np.nan

    cols = st.columns(5)
    cols[0].metric("Task trong ngành CS", f"{visible}/{total}")
    cols[1].metric("Tiềm năng tăng tốc code", score(avg_accel))
    cols[2].metric("Nhu cầu kiểm soát chất lượng", score(avg_risk))
    cols[3].metric("Task critical", pct(critical_share))
    cols[4].metric("Cần Copilot + review", f"{review_count} task")


def agent_quadrant(df: pd.DataFrame) -> go.Figure:
    plot_df = df.dropna(subset=["code_acceleration_potential", "quality_risk_need"]).copy()
    if plot_df.empty:
        return go.Figure()

    x_line = plot_df["code_acceleration_potential"].median()
    y_line = plot_df["quality_risk_need"].median()
    plot_df["task_short"] = plot_df["Task"].astype(str).str.wrap(75).str.replace("\n", "<br>")

    fig = px.scatter(
        plot_df,
        x="code_acceleration_potential",
        y="quality_risk_need",
        color="agent_recommendation",
        color_discrete_map=REC_COLORS,
        size=np.clip(plot_df.get("task_importance_weight", pd.Series(1, index=plot_df.index)).fillna(1), 0.2, None),
        hover_data={
            "Occupation (O*NET-SOC Title)": True,
            "task_group_vi": True,
            "quality_critical_task": True,
            "code_acceleration_potential": ":.2f",
            "quality_risk_need": ":.2f",
            "agent_recommendation": True,
            "Task": False,
            "task_short": True,
        },
        labels={
            "code_acceleration_potential": "Tiềm năng tăng tốc code",
            "quality_risk_need": "Nhu cầu kiểm soát chất lượng",
            "agent_recommendation": "Khuyến nghị",
            "task_short": "Task",
            "task_group_vi": "Nhóm task",
            "quality_critical_task": "Task critical",
        },
    )
    fig.add_vline(x=x_line, line_dash="dash", line_color=PALETTE["slate"], opacity=0.7)
    fig.add_hline(y=y_line, line_dash="dash", line_color=PALETTE["slate"], opacity=0.7)
    fig.add_annotation(
        x=0.98,
        y=0.98,
        xref="paper",
        yref="paper",
        text="Tăng tốc cao + rủi ro cao: cần review/test",
        showarrow=False,
        align="right",
        bgcolor="rgba(255,255,255,0.82)",
        bordercolor="#E6E1D8",
    )
    fig.update_traces(marker=dict(line=dict(width=0.7, color="white"), opacity=0.82))
    fig.update_layout(
        height=560,
        margin=dict(l=10, r=10, t=35, b=10),
        title="Bản đồ AI Agent: tăng tốc code so với rủi ro chất lượng",
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
        legend_title_text="Khuyến nghị",
    )
    return fig


def group_signal_chart(group_df: pd.DataFrame) -> go.Figure:
    if group_df.empty:
        return go.Figure()
    cols = [
        "code_acceleration_potential",
        "quality_risk_need",
        "human_complementarity_index",
    ]
    label_map = {
        "code_acceleration_potential": "Tăng tốc code",
        "quality_risk_need": "Rủi ro chất lượng",
        "human_complementarity_index": "Cần con người",
    }
    long_df = group_df[["task_group_vi", "task_count"] + cols].melt(
        id_vars=["task_group_vi", "task_count"],
        value_vars=cols,
        var_name="signal",
        value_name="score",
    )
    long_df["signal_vi"] = long_df["signal"].map(label_map)
    fig = px.bar(
        long_df,
        y="task_group_vi",
        x="score",
        color="signal_vi",
        barmode="group",
        orientation="h",
        color_discrete_map={
            "Tăng tốc code": PALETTE["teal"],
            "Rủi ro chất lượng": PALETTE["coral"],
            "Cần con người": PALETTE["gold"],
        },
        labels={"score": "Điểm trung bình", "task_group_vi": "", "signal_vi": "Tín hiệu"},
        hover_data={"task_count": True},
    )
    fig.update_layout(
        height=420,
        margin=dict(l=10, r=10, t=35, b=10),
        title="Tín hiệu theo nhóm task",
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
        legend_title_text="",
    )
    return fig


def recommendation_chart(tasks: pd.DataFrame) -> go.Figure:
    if tasks.empty:
        return go.Figure()
    counts = (
        tasks["agent_recommendation"]
        .value_counts()
        .reindex(list(REC_COLORS.keys()))
        .dropna()
        .reset_index()
    )
    counts.columns = ["Khuyến nghị", "Số task"]
    fig = px.bar(
        counts,
        y="Khuyến nghị",
        x="Số task",
        orientation="h",
        color="Khuyến nghị",
        color_discrete_map=REC_COLORS,
        text="Số task",
    )
    fig.update_layout(
        height=370,
        margin=dict(l=10, r=10, t=35, b=10),
        title="Phân bổ khuyến nghị AI Agent",
        showlegend=False,
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
    )
    fig.update_traces(textposition="outside")
    return fig


def regression_chart(ols: pd.DataFrame, logit: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    if not ols.empty:
        ols_plot = ols.sort_values("coef")
        fig.add_trace(
            go.Bar(
                x=ols_plot["coef"],
                y=ols_plot["variable_vi"],
                orientation="h",
                name="OLS: rủi ro chất lượng",
                marker_color=[
                    PALETTE["coral"] if v > 0 else PALETTE["teal"] for v in ols_plot["coef"]
                ],
                hovertemplate="%{y}<br>Hệ số: %{x:.3f}<extra></extra>",
            )
        )
    if not logit.empty:
        logit_plot = logit.sort_values("odds_ratio")
        fig.add_trace(
            go.Bar(
                x=np.log(logit_plot["odds_ratio"].clip(lower=1e-6)),
                y=logit_plot["variable_vi"],
                orientation="h",
                name="Logit: cần Copilot + review",
                marker_color=PALETTE["gold"],
                hovertemplate="%{y}<br>log(odds ratio): %{x:.2f}<extra></extra>",
            )
        )
    fig.add_vline(x=0, line_color=PALETTE["ink"], line_width=1)
    fig.update_layout(
        barmode="group",
        height=460,
        margin=dict(l=10, r=10, t=35, b=10),
        title="Hồi quy khám phá: tín hiệu nào liên quan đến quality gate?",
        xaxis_title="Hệ số chuẩn hóa / log(odds ratio)",
        yaxis_title="",
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
        legend_title_text="Mô hình",
    )
    return fig


def sigmoid(x: float) -> float:
    return 1 / (1 + np.exp(-np.clip(x, -30, 30)))


def build_regression_reference(tasks: pd.DataFrame, raw_tasks: pd.DataFrame) -> pd.DataFrame:
    frames = []
    if not raw_tasks.empty:
        raw = raw_tasks.copy()
        if "sector" in raw.columns:
            raw = raw[raw["sector"].eq("Computer and Mathematical")]
        frames.append(raw)
    if not tasks.empty:
        frames.append(tasks.copy())

    reference = pd.concat(frames, ignore_index=True, sort=False) if frames else pd.DataFrame()
    for col in REG_FEATURES + ["quality_risk_need"]:
        if col in reference.columns:
            reference[col] = pd.to_numeric(reference[col], errors="coerce")
    if "quality_critical_task" in reference.columns:
        reference["quality_critical_task"] = reference["quality_critical_task"].fillna(0).astype(float)
    return reference


def default_feature_value(reference: pd.DataFrame, feature: str) -> float:
    if reference.empty or feature not in reference.columns:
        if not reference.empty and {"variable", "mean"}.issubset(reference.columns):
            row = reference[reference["variable"].eq(feature)]
            if not row.empty and pd.notna(row["mean"].iloc[0]):
                return float(row["mean"].iloc[0])
        return 0.5
    value = reference[feature].dropna().mean()
    if pd.isna(value):
        return 0.5
    return float(value)


def feature_std(reference: pd.DataFrame, feature: str) -> float:
    if reference.empty or feature not in reference.columns:
        if not reference.empty and {"variable", "std"}.issubset(reference.columns):
            row = reference[reference["variable"].eq(feature)]
            if not row.empty and pd.notna(row["std"].iloc[0]) and row["std"].iloc[0] != 0:
                return float(row["std"].iloc[0])
        return 1.0
    std = reference[feature].dropna().std(ddof=0)
    if pd.isna(std) or std == 0:
        return 1.0
    return float(std)


def slider_bounds(reference: pd.DataFrame, feature: str) -> tuple[float, float, float]:
    if feature == "quality_critical_task":
        return 0.0, 1.0, 1.0
    if not reference.empty and {"variable", "p02", "p98"}.issubset(reference.columns):
        row = reference[reference["variable"].eq(feature)]
        if not row.empty:
            low = float(row["p02"].iloc[0])
            high = float(row["p98"].iloc[0])
            step = 0.05 if feature.startswith("expert_") else 0.01
            if feature.startswith("expert_"):
                return max(0.0, round(low, 2)), min(5.0, round(high, 2)), step
            return max(0.0, round(low, 2)), min(1.0, round(high, 2)), step
    if feature.startswith("expert_"):
        values = reference[feature].dropna() if feature in reference.columns else pd.Series(dtype=float)
        low = float(values.quantile(0.02)) if not values.empty else 1.0
        high = float(values.quantile(0.98)) if not values.empty else 5.0
        return max(0.0, round(low, 2)), min(5.0, round(high, 2)), 0.05
    return 0.0, 1.0, 0.01


def predict_from_regression(
    values: dict[str, float],
    reference: pd.DataFrame,
    tasks: pd.DataFrame,
    ols: pd.DataFrame,
    logit: pd.DataFrame,
) -> dict[str, object]:
    z_values = {}
    for feature in REG_FEATURES:
        mean = default_feature_value(reference, feature)
        std = feature_std(reference, feature)
        z_values[feature] = (values.get(feature, mean) - mean) / std

    ols_coef = dict(zip(ols.get("variable", []), ols.get("coef", [])))
    logit_coef = dict(zip(logit.get("variable", []), logit.get("coef", [])))

    if not reference.empty and "ols_intercept" in reference.columns and pd.notna(reference["ols_intercept"].iloc[0]):
        baseline_risk = float(reference["ols_intercept"].iloc[0])
    else:
        baseline_risk = tasks["quality_risk_need"].dropna().mean()
        if pd.isna(baseline_risk):
            baseline_risk = 0.5
    risk_linear = float(baseline_risk + sum(ols_coef.get(f, 0.0) * z_values[f] for f in REG_FEATURES))
    risk_pred = float(np.clip(risk_linear, 0, 1))

    if not reference.empty and "logit_intercept" in reference.columns and pd.notna(reference["logit_intercept"].iloc[0]):
        logit_intercept = float(reference["logit_intercept"].iloc[0])
    else:
        review_rate = tasks["agent_recommendation"].eq("Copilot + review bắt buộc").mean()
        review_rate = float(np.clip(review_rate if not pd.isna(review_rate) else 0.2, 0.01, 0.99))
        logit_intercept = np.log(review_rate / (1 - review_rate))
    review_logit = float(logit_intercept + sum(logit_coef.get(f, 0.0) * z_values[f] for f in REG_FEATURES))
    review_prob = float(sigmoid(review_logit))

    contributions = []
    for feature in REG_FEATURES:
        contributions.append(
            {
                "feature": feature,
                "label": FEATURE_LABELS[feature],
                "ols_contribution": ols_coef.get(feature, 0.0) * z_values[feature],
                "logit_contribution": logit_coef.get(feature, 0.0) * z_values[feature],
            }
        )

    if values.get("quality_critical_task", 0) >= 0.5 and (review_prob >= 0.35 or risk_pred >= 0.45):
        recommendation = "Copilot + review bắt buộc"
    elif review_prob >= 0.65:
        recommendation = "Copilot + review bắt buộc"
    elif risk_pred >= 0.62:
        recommendation = "Con người dẫn dắt, AI hỗ trợ"
    elif review_prob <= 0.25 and risk_pred <= 0.35 and values.get("quality_critical_task", 0) < 0.5:
        recommendation = "Agent bán tự động"
    else:
        recommendation = "Thử nghiệm / theo dõi"

    return {
        "quality_risk_need": risk_pred,
        "review_probability": review_prob,
        "recommendation": recommendation,
        "contributions": pd.DataFrame(contributions),
    }


def contribution_chart(contrib: pd.DataFrame, column: str, title_text: str) -> go.Figure:
    if contrib.empty:
        return go.Figure()
    plot_df = contrib.copy()
    plot_df["abs_value"] = plot_df[column].abs()
    plot_df = plot_df.sort_values("abs_value", ascending=True).tail(7)
    fig = px.bar(
        plot_df,
        x=column,
        y="label",
        orientation="h",
        color=column,
        color_continuous_scale=["#129C9A", "#E8EEF2", "#EF6F52"],
        color_continuous_midpoint=0,
        labels={column: "Đóng góp vào dự đoán", "label": ""},
    )
    fig.add_vline(x=0, line_color=PALETTE["ink"], line_width=1)
    fig.update_layout(
        height=360,
        title=title_text,
        margin=dict(l=10, r=10, t=45, b=10),
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
        showlegend=False,
        coloraxis_showscale=False,
    )
    return fig


def regression_simulator(
    tasks: pd.DataFrame,
    raw_tasks: pd.DataFrame,
    ols: pd.DataFrame,
    logit: pd.DataFrame,
    reg_ref: pd.DataFrame,
) -> None:
    reference = reg_ref if not reg_ref.empty else build_regression_reference(tasks, raw_tasks)
    if reference.empty or ols.empty or logit.empty:
        st.info("Chưa đủ dữ liệu để mô phỏng hồi quy.")
        return

    st.subheader("Kéo thả để xem dự đoán hồi quy thay đổi")
    st.markdown(
        """
        <div class="explain-box">
        <b>Cách dùng:</b> kéo các thanh trượt để giả lập một task có mức tiếp xúc AI,
        độ bất định, yêu cầu chuyên môn và mức cần con người khác nhau. Mô hình sẽ tính lại
        hai kết quả: <b>rủi ro chất lượng dự đoán</b> và <b>xác suất cần Copilot + review bắt buộc</b>.
        Khuyến nghị cuối kết hợp cả hai kết quả này với rule bảo thủ cho task critical.
        Đây là mô phỏng khám phá, không phải chứng minh nhân quả.
        </div>
        """,
        unsafe_allow_html=True,
    )

    controls, results = st.columns([1, 1.25])
    values = {}
    with controls:
        preset = st.selectbox(
            "Chọn tình huống mẫu",
            [
                "Tự điều chỉnh",
                "Task sinh code đơn giản",
                "Task review/debug critical",
                "Task kiến trúc/bảo mật rủi ro cao",
            ],
            help="Preset chỉ đặt nhanh giá trị slider; bạn vẫn có thể kéo lại từng biến.",
        )
        presets = {
            "Task sinh code đơn giản": {
                "automation_exposure_index": 0.85,
                "worker_pull_index": 0.65,
                "human_complementarity_index": 0.25,
                "innovation_momentum_index": 0.85,
                "expert_uncertainty_requirement": 2.0,
                "expert_domain_expertise_requirement": 2.3,
                "quality_critical_task": 0.0,
            },
            "Task review/debug critical": {
                "automation_exposure_index": 0.80,
                "worker_pull_index": 0.65,
                "human_complementarity_index": 0.75,
                "innovation_momentum_index": 0.80,
                "expert_uncertainty_requirement": 4.0,
                "expert_domain_expertise_requirement": 3.8,
                "quality_critical_task": 1.0,
            },
            "Task kiến trúc/bảo mật rủi ro cao": {
                "automation_exposure_index": 0.82,
                "worker_pull_index": 0.60,
                "human_complementarity_index": 0.85,
                "innovation_momentum_index": 0.75,
                "expert_uncertainty_requirement": 4.4,
                "expert_domain_expertise_requirement": 4.5,
                "quality_critical_task": 1.0,
            },
        }
        preset_values = presets.get(preset, {})

        for feature in REG_FEATURES:
            low, high, step = slider_bounds(reference, feature)
            default = preset_values.get(feature, default_feature_value(reference, feature))
            default = float(np.clip(default, low, high))
            if feature == "quality_critical_task":
                values[feature] = 1.0 if st.toggle(
                    FEATURE_LABELS[feature],
                    value=bool(round(default)),
                    help="Bật nếu task liên quan QA, security, troubleshooting, backup, production hoặc compliance.",
                ) else 0.0
            else:
                values[feature] = st.slider(
                    FEATURE_LABELS[feature],
                    min_value=float(low),
                    max_value=float(high),
                    value=float(default),
                    step=float(step),
                    help="Kéo sang phải nghĩa là tín hiệu này mạnh hơn.",
                )

    prediction = predict_from_regression(values, reference, tasks, ols, logit)
    risk = prediction["quality_risk_need"]
    review_prob = prediction["review_probability"]
    rec = prediction["recommendation"]

    with results:
        m1, m2, m3 = st.columns(3)
        m1.metric("Rủi ro chất lượng dự đoán", score(risk))
        m2.metric("Xác suất cần review", pct(review_prob))
        m3.metric("Khuyến nghị", rec)

        gauge = go.Figure()
        gauge.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=review_prob * 100,
                number={"suffix": "%"},
                title={"text": "Xác suất cần Copilot + review"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": REC_COLORS.get(rec, PALETTE["coral"])},
                    "steps": [
                        {"range": [0, 30], "color": "#E8F3F1"},
                        {"range": [30, 60], "color": "#FFF3D4"},
                        {"range": [60, 100], "color": "#FFE1D9"},
                    ],
                    "threshold": {"line": {"color": PALETTE["ink"], "width": 3}, "value": review_prob * 100},
                },
            )
        )
        gauge.update_layout(height=285, margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="#FBFAF7")
        st.plotly_chart(gauge, width="stretch")

        st.caption(
            "Lưu ý: xác suất Logit nhạy nhất với mức tiếp xúc AI, worker muốn AI và động lực đổi mới; "
            "rủi ro chất lượng OLS nhạy hơn với mức cần con người, độ bất định và chuyên môn miền."
        )

        if rec == "Agent bán tự động":
            st.success("Diễn giải: task này có thể thử tự động hóa có kiểm soát, nhưng vẫn nên có logging, test và rollback.")
        elif rec == "Copilot + review bắt buộc":
            st.warning("Diễn giải: AI có thể giúp tăng tốc, nhưng output cần review/test trước khi dùng thật.")
        elif rec == "Con người dẫn dắt, AI hỗ trợ":
            st.info("Diễn giải: con người nên giữ vai trò quyết định; AI phù hợp để gợi ý, tóm tắt hoặc tạo nháp.")
        else:
            st.info("Diễn giải: nên thí điểm nhỏ, đo lỗi và thu thêm dữ liệu trước khi mở rộng.")

    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            contribution_chart(
                prediction["contributions"],
                "ols_contribution",
                "Yếu tố làm thay đổi rủi ro chất lượng",
            ),
            width="stretch",
        )
    with c2:
        st.plotly_chart(
            contribution_chart(
                prediction["contributions"],
                "logit_contribution",
                "Yếu tố làm thay đổi xác suất cần review",
            ),
            width="stretch",
        )


def reskill_occ_chart(df: pd.DataFrame, top_n: int = 12) -> go.Figure:
    if df.empty:
        return go.Figure()
    plot_df = df.sort_values("reskilling_priority_score", ascending=False).head(top_n)
    fig = px.bar(
        plot_df.sort_values("reskilling_priority_score"),
        x="reskilling_priority_score",
        y="Occupation (O*NET-SOC Title)",
        orientation="h",
        color="critical_task_share",
        color_continuous_scale=["#E8EEF2", PALETTE["coral"]],
        labels={
            "reskilling_priority_score": "Điểm ưu tiên reskilling",
            "Occupation (O*NET-SOC Title)": "",
            "critical_task_share": "Tỉ lệ task critical",
        },
        hover_data={
            "task_count": True,
            "code_acceleration_potential": ":.2f",
            "quality_risk_need": ":.2f",
            "human_complementarity_index": ":.2f",
        },
    )
    fig.update_layout(
        height=500,
        margin=dict(l=10, r=10, t=35, b=10),
        title="Nghề nên ưu tiên đào tạo lại",
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
    )
    return fig


def reskill_group_chart(df: pd.DataFrame) -> go.Figure:
    if df.empty:
        return go.Figure()
    plot_df = df.sort_values("reskilling_priority_score")
    fig = px.bar(
        plot_df,
        x="reskilling_priority_score",
        y="task_group_vi",
        orientation="h",
        color="critical_task_share",
        color_continuous_scale=["#E8EEF2", PALETTE["teal"], PALETTE["coral"]],
        labels={
            "reskilling_priority_score": "Điểm ưu tiên reskilling",
            "task_group_vi": "",
            "critical_task_share": "Tỉ lệ task critical",
        },
        hover_data={"task_count": True, "quality_risk_need": ":.2f"},
    )
    fig.update_layout(
        height=430,
        margin=dict(l=10, r=10, t=35, b=10),
        title="Nhóm task cần nâng cấp kỹ năng",
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
    )
    return fig


def pathway_view(pathway: pd.DataFrame) -> None:
    if pathway.empty:
        st.info("Chưa có bảng pathway.")
        return

    st.markdown(
        """
        <div class="explain-box">
        <b>Cách đọc:</b> AI không làm câu chuyện chuyển từ "biết code" sang "không cần code".
        Dữ liệu gợi ý hướng dịch chuyển hợp lý hơn là từ tự tạo output sang kiểm soát output:
        biết đặt yêu cầu, kiểm chứng, review, test, đánh giá trade-off và chịu trách nhiệm chất lượng.
        </div>
        """,
        unsafe_allow_html=True,
    )

    for _, row in pathway.iterrows():
        cols = st.columns([1, 1, 1.25])
        cols[0].markdown(
            f"""
            <div class="path-card">
            <div class="path-title">Trước AI</div>
            {row['before_ai']}
            </div>
            """,
            unsafe_allow_html=True,
        )
        cols[1].markdown(
            f"""
            <div class="path-card">
            <div class="path-title">Khi có AI hỗ trợ</div>
            {row['ai_augmented_work']}
            </div>
            """,
            unsafe_allow_html=True,
        )
        cols[2].markdown(
            f"""
            <div class="path-card">
            <div class="path-title">Kỹ năng cần nâng cấp</div>
            {row['human_premium_skill']}
            <div class="small-note">Nhóm task: {row['related_task_group']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def extract_known_skills(raw_tasks: pd.DataFrame) -> list[str]:
    if raw_tasks.empty or "skill_list" not in raw_tasks.columns:
        return []
    skills: set[str] = set()
    for value in raw_tasks["skill_list"].dropna().astype(str):
        cleaned = value.strip()
        if cleaned.startswith("[") and cleaned.endswith("]"):
            cleaned = cleaned.strip("[]")
            parts = [p.strip().strip("'\"") for p in cleaned.split(",")]
        else:
            parts = [cleaned]
        for part in parts:
            if part and part.lower() != "nan":
                skills.add(part)
    return sorted(skills)


def split_skills(text: str) -> list[str]:
    return [skill.strip() for chunk in text.splitlines() for skill in chunk.split(",") if skill.strip()]


def repo_agent_pipeline_chart() -> go.Figure:
    labels = [
        "Folder repo",
        "Repo Scanner",
        "Style Profiler",
        "Vector Index",
        "Prompt context",
        "AI sinh code",
        "Test/Lint/Build",
        "Code + độ tin cậy",
    ]
    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="fixed",
                node=dict(
                    pad=18,
                    thickness=18,
                    line=dict(color="#FFFFFF", width=1),
                    label=labels,
                    color=[
                        PALETTE["ink"],
                        PALETTE["teal"],
                        PALETTE["gold"],
                        "#7B9ACC",
                        PALETTE["coral"],
                        PALETTE["teal"],
                        PALETTE["coral"],
                        PALETTE["ink"],
                    ],
                ),
                link=dict(
                    source=list(range(len(labels) - 1)),
                    target=list(range(1, len(labels))),
                    value=[1] * (len(labels) - 1),
                    color=["rgba(18,156,154,0.22)"] * (len(labels) - 1),
                ),
            )
        ]
    )
    fig.update_layout(
        height=360,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="#FBFAF7",
        font=dict(size=13, color=PALETTE["ink"]),
    )
    return fig


def personalization_level_chart() -> go.Figure:
    level_df = pd.DataFrame(
        {
            "Mức": ["Prompt + RAG", "Fine-tune style", "Feedback learning"],
            "Phù hợp hiện tại": [0.95, 0.45, 0.65],
            "Chi phí/độ khó": [0.30, 0.85, 0.70],
        }
    )
    fig = go.Figure()
    fig.add_bar(
        y=level_df["Mức"],
        x=level_df["Phù hợp hiện tại"],
        orientation="h",
        name="Phù hợp với đề tài",
        marker_color=PALETTE["teal"],
    )
    fig.add_bar(
        y=level_df["Mức"],
        x=level_df["Chi phí/độ khó"],
        orientation="h",
        name="Chi phí/độ khó",
        marker_color=PALETTE["coral"],
    )
    fig.update_layout(
        barmode="group",
        height=300,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(range=[0, 1], tickformat=".0%"),
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
        legend=dict(orientation="h", y=1.12),
    )
    return fig


def control_level_chart() -> go.Figure:
    control_df = pd.DataFrame(
        {
            "Mức kiểm soát": [
                "1. Gợi ý",
                "2. Copilot có review",
                "3. Agent bán tự động",
                "4. Tự động có giám sát",
            ],
            "Mức tự động hóa": [0.20, 0.45, 0.70, 0.90],
            "Mức kiểm soát con người": [0.95, 0.80, 0.55, 0.35],
        }
    )
    fig = go.Figure()
    fig.add_bar(
        y=control_df["Mức kiểm soát"],
        x=control_df["Mức tự động hóa"],
        orientation="h",
        name="Tự động hóa",
        marker_color=PALETTE["teal"],
    )
    fig.add_bar(
        y=control_df["Mức kiểm soát"],
        x=control_df["Mức kiểm soát con người"],
        orientation="h",
        name="Kiểm soát con người",
        marker_color=PALETTE["coral"],
    )
    fig.update_layout(
        barmode="group",
        height=330,
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(range=[0, 1], tickformat=".0%"),
        plot_bgcolor="#FBFAF7",
        paper_bgcolor="#FBFAF7",
        legend=dict(orientation="h", y=1.12),
    )
    return fig


def control_level_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Mức": "1. Gợi ý",
                "AI được làm": "Giải thích, gợi ý hướng sửa, tạo checklist, đề xuất test.",
                "Con người phải làm": "Tự quyết định và tự sửa code.",
                "Dùng khi": "Task mới, thiếu context repo, rủi ro cao, yêu cầu ngoài nghề.",
            },
            {
                "Mức": "2. Copilot có review",
                "AI được làm": "Viết nháp code/test theo file liên quan và coding style profile.",
                "Con người phải làm": "Review diff, chọn merge, kiểm tra logic nghiệp vụ.",
                "Dùng khi": "Task có tăng tốc code nhưng có rủi ro chất lượng.",
            },
            {
                "Mức": "3. Agent bán tự động",
                "AI được làm": "Sửa code trong phạm vi nhỏ, chạy test/lint/build, tự sửa lỗi lặp lại.",
                "Con người phải làm": "Duyệt cuối trước khi merge hoặc deploy.",
                "Dùng khi": "Repo đã có test tốt, task nằm đúng nghề và đúng module.",
            },
            {
                "Mức": "4. Tự động có giám sát",
                "AI được làm": "Tự xử lý task lặp lại, tạo PR, cập nhật test và báo cáo độ tin cậy.",
                "Con người phải làm": "Giám sát policy, audit định kỳ, can thiệp khi validation fail.",
                "Dùng khi": "Task lặp lại, rủi ro thấp, có CI/CD và rollback rõ ràng.",
            },
        ]
    )


def occupation_scope_view(tasks: pd.DataFrame, reskill_task: pd.DataFrame, raw_tasks: pd.DataFrame) -> None:
    if tasks.empty:
        st.info("Chưa có dữ liệu task để cá nhân hóa theo nghề.")
        return

    st.subheader("Cá nhân hóa AI Agent theo repository / coding style personalization")
    st.markdown(
        """
        <div class="explain-box">
        <b>Ý tưởng chính:</b> khi người dùng đưa vào một folder repo, AI không nên code theo kiểu chung chung.
        Hệ thống cần hiểu cấu trúc project, framework, convention đặt tên, cách tổ chức file, pattern xử lý lỗi,
        style test, import/export, comment/documentation và các helper nội bộ đã có.
        Với một repo cụ thể, hướng tốt nhất là <b>RAG + phân tích codebase + prompt context + kiểm thử tự động</b>,
        chưa cần fine-tune model ngay.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.plotly_chart(repo_agent_pipeline_chart(), width="stretch")

    st.markdown("### 1. Đưa folder repo vào và quét project")
    default_repo = str(BASE_DIR)
    repo_text = st.text_input(
        "Đường dẫn folder repo",
        value=default_repo,
        help="Vì Streamlit chạy local, bạn có thể nhập path folder trên máy để app nhận diện cấu trúc repo.",
        key="repo_folder_path",
    )
    repo_profile = repo_agent.scan_repository(repo_text)

    if not repo_profile["exists"]:
        st.error("Không tìm thấy folder repo. Hãy kiểm tra lại đường dẫn.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("File đã quét", repo_profile["file_count"])
        c2.metric("Ngôn ngữ chính", next(iter(repo_profile["languages"]), "Chưa rõ"))
        c3.metric("Framework", ", ".join(repo_profile["frameworks"][:2]))
        c4.metric("Config tìm thấy", len(repo_profile["configs"]))

        left, right = st.columns([1, 1])
        with left:
            st.markdown("**Ngôn ngữ / file type trong repo**")
            lang_df = pd.DataFrame(
                {"Ngôn ngữ": list(repo_profile["languages"].keys()), "Số file": list(repo_profile["languages"].values())}
            )
            if not lang_df.empty:
                fig = px.bar(
                    lang_df,
                    x="Số file",
                    y="Ngôn ngữ",
                    orientation="h",
                    color="Số file",
                    color_continuous_scale=["#E8EEF2", PALETTE["teal"]],
                )
                fig.update_layout(
                    height=300,
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor="#FBFAF7",
                    paper_bgcolor="#FBFAF7",
                    showlegend=False,
                )
                st.plotly_chart(fig, width="stretch")
            else:
                st.info("Chưa nhận diện được file code.")
        with right:
            st.markdown("**Tín hiệu cấu trúc repo**")
            st.dataframe(
                pd.DataFrame(
                    {
                        "Loại tín hiệu": ["Framework", "Config", "Thư mục chính", "Style signal"],
                        "Giá trị": [
                            ", ".join(repo_profile["frameworks"]),
                            ", ".join(repo_profile["configs"]) or "Chưa phát hiện",
                            ", ".join(repo_profile["top_dirs"]) or "Chưa phát hiện",
                            "\n".join(repo_profile["style_signals"]),
                        ],
                    }
                ),
                width="stretch",
                hide_index=True,
            )

    occupations = sorted(tasks["Occupation (O*NET-SOC Title)"].dropna().unique().tolist())
    selected_occ = st.selectbox(
        "Chọn ngành nghề / vai trò mà AI Agent được phép hỗ trợ",
        occupations,
        help="AI Agent sẽ chỉ thực hiện đúng phạm vi công việc của nghề này.",
        key="personalized_occupation",
    )

    occ_tasks = tasks[tasks["Occupation (O*NET-SOC Title)"].eq(selected_occ)].copy()
    occ_reskill = reskill_task[reskill_task["Occupation (O*NET-SOC Title)"].eq(selected_occ)].copy()

    st.markdown("### 2. Tạo hồ sơ coding style và skill profile")
    known_skills = extract_known_skills(raw_tasks)
    selected_skills = st.multiselect(
        "Thêm skill có sẵn của người dùng / team",
        known_skills,
        default=[],
        help="Các skill này giúp AI cá nhân hóa cách hỗ trợ theo năng lực và vai trò.",
    )
    custom_skill_text = st.text_area(
        "Thêm skill riêng hoặc convention nội bộ",
        placeholder="Ví dụ: React, FastAPI, Zustand, Vitest, toast.error, Repository pattern, viết test cạnh component...",
        help="Nhập mỗi skill trên một dòng hoặc ngăn cách bằng dấu phẩy.",
    )
    custom_skills = split_skills(custom_skill_text)
    all_skills = selected_skills + custom_skills

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Task thuộc nghề", len(occ_tasks))
    c2.metric("Nhóm task", occ_tasks["task_group_vi"].nunique())
    c3.metric("Task critical", pct(occ_tasks["quality_critical_task"].mean() if len(occ_tasks) else np.nan))
    c4.metric("Skill đã thêm", len(all_skills))

    allowed_groups = (
        occ_tasks.groupby("task_group_vi", as_index=False)
        .agg(
            task_count=("Task ID", "count"),
            code_acceleration_potential=("code_acceleration_potential", "mean"),
            quality_risk_need=("quality_risk_need", "mean"),
        )
        .sort_values("task_count", ascending=False)
    )

    left, right = st.columns([1, 1])
    with left:
        st.markdown("**Phạm vi task AI được phép hỗ trợ theo nghề**")
        st.dataframe(
            allowed_groups,
            width="stretch",
            hide_index=True,
            column_config={
                "task_group_vi": "Nhóm task",
                "task_count": "Số task",
                "code_acceleration_potential": st.column_config.ProgressColumn(
                    "Tăng tốc code", min_value=0, max_value=1, format="%.2f"
                ),
                "quality_risk_need": st.column_config.ProgressColumn(
                    "Rủi ro chất lượng", min_value=0, max_value=1, format="%.2f"
                ),
            },
        )
    with right:
        st.markdown("**Quality gate theo nghề đã chọn**")
        rec_counts = occ_tasks["agent_recommendation"].value_counts().reindex(list(REC_COLORS.keys())).dropna()
        if not rec_counts.empty:
            rec_plot = rec_counts.rename_axis("Khuyến nghị").reset_index(name="Số task")
            fig = px.bar(
                rec_plot,
                x="Số task",
                y="Khuyến nghị",
                orientation="h",
                color="Khuyến nghị",
                color_discrete_map=REC_COLORS,
                text="Số task",
            )
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=False,
                plot_bgcolor="#FBFAF7",
                paper_bgcolor="#FBFAF7",
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Chưa có đủ khuyến nghị cho nghề này.")

    st.markdown("### 3. Bốn mức kiểm soát AI Agent")
    st.markdown(
        """
        <div class="explain-box">
        <b>Cách đọc:</b> repo-aware AI Agent không nên chỉ có một chế độ "tự code".
        Tùy mức rủi ro, chất lượng test và phạm vi nghề, hệ thống cần chọn mức kiểm soát phù hợp:
        càng rủi ro cao thì càng cần con người review, càng lặp lại và có CI tốt thì agent mới được tự động nhiều hơn.
        </div>
        """,
        unsafe_allow_html=True,
    )
    recommended_control = "2. Copilot có review"
    if len(occ_tasks) and occ_tasks["quality_critical_task"].mean() < 0.25 and occ_tasks["quality_risk_need"].mean() < 0.45:
        recommended_control = "3. Agent bán tự động"
    if len(occ_tasks) and occ_tasks["quality_critical_task"].mean() > 0.45:
        recommended_control = "1. Gợi ý"

    control_options = control_level_table()["Mức"].tolist()
    selected_control = st.radio(
        "Chọn mức kiểm soát khi AI viết code",
        control_options,
        index=control_options.index(recommended_control),
        horizontal=True,
        help="Mức này quyết định AI chỉ gợi ý, được viết nháp, được sửa code có validation, hay được tự động hóa task lặp lại.",
        key="agent_control_level",
    )

    left, right = st.columns([1, 1.15])
    with left:
        st.plotly_chart(control_level_chart(), width="stretch")
    with right:
        table = control_level_table()
        st.dataframe(
            table,
            width="stretch",
            hide_index=True,
            column_config={
                "Mức": "Mức kiểm soát",
                "AI được làm": "AI được làm",
                "Con người phải làm": "Con người phải làm",
                "Dùng khi": "Dùng khi",
            },
        )

    selected_control_row = control_level_table().loc[control_level_table()["Mức"].eq(selected_control)].iloc[0]
    st.markdown(
        f"""
        <div class="warning-box">
        <b>Mức đang chọn:</b> {selected_control}.<br>
        <b>AI được làm:</b> {selected_control_row['AI được làm']}<br>
        <b>Con người giữ quyền:</b> {selected_control_row['Con người phải làm']}
        </div>
        """,
        unsafe_allow_html=True,
    )

    style_profile = {
        "Framework/ngôn ngữ": ", ".join(repo_profile["frameworks"]),
        "Cấu trúc project": ", ".join(repo_profile["top_dirs"]) or "Cần đọc thêm repo",
        "Config quan trọng": ", ".join(repo_profile["configs"]) or "Cần hỏi người dùng",
        "Test nên chạy": ", ".join(repo_profile["test_commands"]),
        "Lint/typecheck nên chạy": ", ".join(repo_profile["lint_commands"]),
        "Build nên chạy": ", ".join(repo_profile["build_commands"]),
        "Coding style rút ra": "\n".join(f"- {signal}" for signal in inferred_style),
        "Skill/convention bổ sung": ", ".join(all_skills) if all_skills else "Chưa khai báo",
        "Mức kiểm soát AI Agent": selected_control,
    }
    st.markdown("**Coding Style Profile rút ra từ repo**")
    st.dataframe(
        pd.DataFrame({"Thành phần": list(style_profile.keys()), "Kết luận dùng cho AI Agent": list(style_profile.values())}),
        width="stretch",
        hide_index=True,
    )

    st.markdown("### 4. Chia nhỏ code, tạo index và chỉ lấy file liên quan")
    retrieval_cols = st.columns(3)
    retrieval_cols[0].markdown(
        """
        <div class="path-card">
        <div class="path-title">Chunk code</div>
        Chia theo file, function, class, component, module để không nhét toàn bộ repo vào prompt.
        </div>
        """,
        unsafe_allow_html=True,
    )
    retrieval_cols[1].markdown(
        """
        <div class="path-card">
        <div class="path-title">Vector index / code search</div>
        Khi user yêu cầu, hệ thống tìm đúng file liên quan như service, page, route, store, test.
        </div>
        """,
        unsafe_allow_html=True,
    )
    retrieval_cols[2].markdown(
        """
        <div class="path-card">
        <div class="path-title">Prompt có context</div>
        AI nhận repo style, file liên quan, yêu cầu cụ thể và quy tắc không tạo abstraction mới nếu không cần.
        </div>
        """,
        unsafe_allow_html=True,
    )

    user_task = st.text_input(
        "Mô phỏng yêu cầu coding của người dùng",
        value="Thêm chức năng login bằng Google",
        key="repo_user_task",
    )
    likely_files = st.multiselect(
        "File/module liên quan nên retrieve vào prompt",
        [
            "auth.service.ts",
            "LoginPage.tsx",
            "routes.ts",
            "user.store.ts",
            "apiClient.ts",
            "components/AuthButton.tsx",
            "tests/auth.test.tsx",
            "README.md",
        ],
        default=["auth.service.ts", "LoginPage.tsx", "apiClient.ts", "tests/auth.test.tsx"],
    )

    st.markdown("### 5. Prompt repo-aware dùng khi gọi AI")
    top_scope = occ_tasks.sort_values(
        ["quality_critical_task", "code_acceleration_potential", "quality_risk_need"],
        ascending=[False, False, False],
    )
    prompt = f"""Bạn là AI coding agent cho repository này.

Phạm vi nghề được phép hỗ trợ:
- {selected_occ}

Repo style:
- Framework/ngôn ngữ: {style_profile["Framework/ngôn ngữ"]}
- Cấu trúc project: {style_profile["Cấu trúc project"]}
- Config quan trọng: {style_profile["Config quan trọng"]}
- Test nên chạy: {style_profile["Test nên chạy"]}
- Lint/typecheck nên chạy: {style_profile["Lint/typecheck nên chạy"]}
- Mức kiểm soát AI Agent: {style_profile["Mức kiểm soát AI Agent"]}
- Skill/convention bổ sung: {style_profile["Skill/convention bổ sung"]}
- Tín hiệu style: {"; ".join(repo_profile["style_signals"])}

Các file liên quan cần đưa vào prompt/RAG:
{chr(10).join(f"- {name}" for name in likely_files) if likely_files else "- Chưa chọn file; phải retrieve trước khi sinh code."}

Yêu cầu của người dùng:
{user_task}

Quy tắc bắt buộc khi sinh code:
- Không fine-tune model cho repo này; dùng RAG + style profile + prompt context.
- Tuân thủ mức kiểm soát đang chọn: {selected_control}.
- Với mức này, AI được làm: {selected_control_row['AI được làm']}
- Con người vẫn phải làm: {selected_control_row['Con người phải làm']}
- Giữ đúng kiến trúc, naming convention, import/export, error handling, test style và helper nội bộ của repo.
- Không tạo abstraction mới nếu repo hiện tại chưa cần.
- Nếu yêu cầu nằm ngoài phạm vi nghề {selected_occ}, hãy từ chối thực hiện trực tiếp và đề xuất vai trò phù hợp hơn.
- Nếu task ảnh hưởng bảo mật, production, dữ liệu, QA hoặc kiến trúc hệ thống, bắt buộc tạo checklist review và test.
- Sau khi sửa code, chạy validation loop: generate code -> test/lint/build -> đọc lỗi -> sửa -> chạy lại.
"""

    st.markdown("**Prompt mẫu**")
    st.code(prompt, language="text")

    st.markdown("### 6. Kiểm thử tự động sau khi AI viết code")
    validation_df = pd.DataFrame(
        {
            "Bước": ["Generate code", "Run test", "Run lint/typecheck", "Run build", "Read error and fix"],
            "Mục đích": [
                "Sinh code theo context repo và coding style profile.",
                "Phát hiện lỗi logic, regression và test thiếu.",
                "Bắt lỗi format, import, type, convention.",
                "Kiểm tra app/package còn build được.",
                "Đưa lỗi ngược lại cho AI sửa tiếp thay vì tin code lần đầu.",
            ],
            "Lệnh gợi ý": [
                "AI edit",
                ", ".join(repo_profile["test_commands"]),
                ", ".join(repo_profile["lint_commands"]),
                ", ".join(repo_profile["build_commands"]),
                "AI fix from error log",
            ],
        }
    )
    st.dataframe(validation_df, width="stretch", hide_index=True)

    st.markdown("### 7. Vì sao chưa nên fine-tune ngay?")
    left, right = st.columns([1, 1])
    with left:
        st.plotly_chart(personalization_level_chart(), width="stretch")
    with right:
        st.markdown(
            """
            <div class="warning-box">
            <b>Khuyến nghị cho đề tài:</b> chọn <b>Mức 1 - Prompt + RAG</b>.
            Fine-tune chỉ nên dùng khi có nhiều ví dụ before/after, nhiều repo ổn định,
            hoặc muốn học style chung của cả team. Với từng repo thay đổi liên tục,
            RAG cập nhật nhanh hơn, rẻ hơn và dễ kiểm soát chất lượng hơn.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="explain-box">
            <b>Câu đưa vào bài phân tích:</b><br>
            Để cá nhân hóa AI Agent trong lập trình, hệ thống không cần huấn luyện lại mô hình cho từng repository.
            Thay vào đó, repository được phân tích để tạo hồ sơ coding style, index các file và truy xuất các đoạn code
            liên quan khi người dùng yêu cầu. AI Agent sau đó sinh code dựa trên context thực tế của repo và được kiểm chứng
            bằng test, lint, build. Cách tiếp cận này giúp AI viết code phù hợp hơn với kiến trúc, convention và chất lượng
            hiện có của dự án.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Xem task cụ thể mà AI Agent được phép xử lý theo nghề đã chọn"):
        st.dataframe(
            top_scope[
                [
                    "Task",
                    "task_group_vi",
                    "quality_critical_task",
                    "code_acceleration_potential",
                    "quality_risk_need",
                    "agent_recommendation",
                ]
            ],
            width="stretch",
            hide_index=True,
            column_config={
                "Task": "Task được phép",
                "task_group_vi": "Nhóm task",
                "quality_critical_task": "Critical",
                "code_acceleration_potential": st.column_config.ProgressColumn(
                    "Tăng tốc code", min_value=0, max_value=1, format="%.2f"
                ),
                "quality_risk_need": st.column_config.ProgressColumn(
                    "Rủi ro chất lượng", min_value=0, max_value=1, format="%.2f"
                ),
                "agent_recommendation": "Cách AI được phép hỗ trợ",
            },
        )

    blocked_examples = tasks[~tasks["Occupation (O*NET-SOC Title)"].eq(selected_occ)].copy()
    blocked_examples = blocked_examples.sample(min(6, len(blocked_examples)), random_state=7)
    with st.expander("Ví dụ yêu cầu ngoài phạm vi nên bị chặn"):
        st.dataframe(
            blocked_examples[["Occupation (O*NET-SOC Title)", "Task", "task_group_vi"]],
            width="stretch",
            hide_index=True,
            column_config={
                "Occupation (O*NET-SOC Title)": "Nghề khác",
                "Task": "Task ngoài phạm vi",
                "task_group_vi": "Nhóm task",
            },
        )


def repo_personalization_solution_view(tasks: pd.DataFrame, reskill_task: pd.DataFrame, raw_tasks: pd.DataFrame) -> None:
    if tasks.empty:
        st.info("Chưa có dữ liệu task để cá nhân hóa AI Agent.")
        return

    st.subheader("Khuyến nghị giải pháp cá nhân hóa AI Agent")

    top_left, top_mid, top_right = st.columns([1.25, 1, 1])
    with top_left:
        repo_input_mode = st.radio(
            "Cách đưa repo vào",
            ["Nhập đường dẫn folder", "Upload file .zip"],
            horizontal=True,
            key="repo_input_mode_compact",
        )
        if repo_input_mode == "Upload file .zip":
            uploaded_repo = st.file_uploader(
                "Upload repo đã nén .zip",
                type=["zip"],
                help="Nén cả folder repo thành .zip rồi upload. App sẽ tự giải nén và quét cấu trúc.",
                key="repo_zip_uploader",
            )
            if uploaded_repo is not None:
                repo_root = repo_agent.safe_extract_zip(uploaded_repo.getvalue(), uploaded_repo.name)
                repo_text = str(repo_root)
                st.caption(f"Đã nạp repo từ ZIP: {repo_root}")
            else:
                repo_text = str(BASE_DIR)
                st.caption("Chưa upload ZIP, app tạm dùng repo hiện tại.")
        else:
            repo_text = st.text_input(
                "Folder repo",
                value=str(BASE_DIR),
                help="Ví dụ: E:\\du-an\\my-repo. Nếu không biết path, hãy nén repo thành .zip và chọn chế độ upload.",
                key="repo_folder_path_compact",
            )
    occupations = sorted(tasks["Occupation (O*NET-SOC Title)"].dropna().unique().tolist())
    with top_mid:
        selected_occ = st.selectbox(
            "Vai trò/nghề",
            occupations,
            help="AI Agent chỉ được xử lý đúng phạm vi nghề này.",
            key="personalized_occupation_compact",
        )
    with top_right:
        custom_skill_text = st.text_area(
            "Skill/convention thêm",
            placeholder="React, FastAPI, Vitest, toast.error...",
            help="Nhập mỗi skill trên một dòng hoặc ngăn cách bằng dấu phẩy.",
            height=88,
            key="compact_skill_text",
        )

    repo_profile = repo_agent.scan_repository(repo_text)
    repo_path = Path(repo_profile["path"])
    inferred_style = repo_agent.infer_coding_style_profile(repo_path, repo_profile) if repo_profile["exists"] else []
    occ_tasks = tasks[tasks["Occupation (O*NET-SOC Title)"].eq(selected_occ)].copy()
    known_skills = extract_known_skills(raw_tasks)
    selected_skills = st.multiselect(
        "Chọn skill có sẵn",
        known_skills,
        default=[],
        key="compact_skill_picker",
    )
    all_skills = selected_skills + split_skills(custom_skill_text)

    recommended_level = 2
    if len(occ_tasks) and occ_tasks["quality_critical_task"].mean() < 0.25 and occ_tasks["quality_risk_need"].mean() < 0.45:
        recommended_level = 3
    if len(occ_tasks) and occ_tasks["quality_critical_task"].mean() > 0.45:
        recommended_level = 1

    control_df = control_level_table()
    group_signal = (
        occ_tasks.groupby("task_group_vi", as_index=False)
        .agg(
            W=("worker_pull_index", "mean"),
            E=("automation_exposure_index", "mean"),
            quality_gap=("quality_risk_need", "mean"),
            task_count=("Task ID", "count"),
        )
        .sort_values("quality_gap", ascending=False)
        .head(4)
    )

    main_left, main_right = st.columns([1, 1])
    with main_left:
        with st.container(border=True):
            st.markdown("**🎛️ Giải pháp 2 — Micro-Agency Slider (Thanh trượt Tự chủ)**")
            st.write(
                "Thanh trượt 4 mức cho phép kỹ sư tự điều chỉnh mức can thiệp của AI theo từng tác vụ. "
                "Mức mặc định được gợi ý từ rủi ro chất lượng và task critical của vai trò đã chọn."
            )
            selected_level = st.slider(
                "Kéo thanh trượt để thử nghiệm mức độ tự trị",
                min_value=1,
                max_value=4,
                value=recommended_level,
                step=1,
                key="agent_control_slider_compact",
            )
            marker_left = {1: 0, 2: 32, 3: 65, 4: 96}[selected_level]
            st.markdown(
                f"""
                <div class="level-rail">
                    <div class="level-marker" style="left: calc({marker_left}% - 11px);"></div>
                </div>
                <div class="level-labels">
                    <div>💡 Gợi ý<br><b>Mức 1</b></div>
                    <div>📝 Dẫn ý<br><b>Mức 2</b></div>
                    <div>💻 Code<br><b>Mức 3</b></div>
                    <div>🚀 Deploy<br><b>Mức 4</b></div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            selected_control = control_df.iloc[selected_level - 1]["Mức"]
            selected_control_row = control_df.iloc[selected_level - 1]
            st.markdown(
                f"""
                <div class="selected-level">
                <b>{selected_control}:</b> {selected_control_row['AI được làm']}
                <br><span class="small-note">Con người giữ quyền: {selected_control_row['Con người phải làm']}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("**Chỉ số W, E, GAP của các nhóm task ở mức này:**")
            if group_signal.empty:
                st.info("Chưa có dữ liệu nhóm task cho nghề này.")
            else:
                for _, row in group_signal.iterrows():
                    w_score = row["W"] * 3
                    e_score = row["E"] * 3
                    gap_score = row["quality_gap"] * 3
                    st.markdown(
                        f"""
                        <div class="compact-row">
                            <b>{row['task_group_vi']}</b>
                            <span>W: {w_score:.1f}</span>
                            <span>E: {e_score:.1f}</span>
                            <span style="color:#EF3F3F;font-weight:700;">Gap: {gap_score:+.1f}</span>
                            <span class="level-pill">🚀 Mức {selected_level}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    style_profile = {
        "Framework/ngôn ngữ": ", ".join(repo_profile["frameworks"]),
        "Cấu trúc project": ", ".join(repo_profile["top_dirs"]) or "Cần đọc thêm repo",
        "Config quan trọng": ", ".join(repo_profile["configs"]) or "Cần hỏi người dùng",
        "Test nên chạy": ", ".join(repo_profile["test_commands"]),
        "Lint/typecheck nên chạy": ", ".join(repo_profile["lint_commands"]),
        "Build nên chạy": ", ".join(repo_profile["build_commands"]),
        "Coding style rút ra": "\n".join(f"- {signal}" for signal in inferred_style),
        "Skill/convention bổ sung": ", ".join(all_skills) if all_skills else "Chưa khai báo",
        "Mức kiểm soát AI Agent": selected_control,
    }

    with main_right:
        with st.container(border=True):
            st.markdown("**🛡️ Giải pháp 3 — AI PR-Defense (Bản tự thuyết minh giải pháp)**")
            st.write(
                "Với task có khoảng trống niềm tin cao, AI không chỉ sinh code mà phải sinh kèm Decision Log: "
                "lý do chọn giải pháp, trade-off, rủi ro và lệnh kiểm thử."
            )
            user_task = st.text_input(
                "Nhập tiêu đề Pull Request hoặc tác vụ",
                value="Tích hợp Rate-Limiter (Redis Lua script)",
                key="repo_user_task_compact",
            )
            code_index = repo_agent.build_code_index(repo_path) if repo_profile["exists"] else []
            retrieved_chunks = repo_agent.retrieve_relevant_chunks(code_index, user_task, top_k=5)
            st.caption(
                f"Đã tạo {len(code_index)} code chunks và retrieve {len(retrieved_chunks)} đoạn liên quan cho task này."
            )
            generation_signature = {
                "task": user_task,
                "level": selected_level,
                "control": selected_control,
                "repo": str(repo_profile["path"]),
                "files": [f"{chunk['path']}::{chunk['symbol']}" for chunk in retrieved_chunks],
            }
            if st.button("Sinh Thuyết minh Quyết định bằng AI", key="fake_pr_defense_button"):
                with st.spinner("Đang gọi AI để sinh Decision Log từ repo context..."):
                    try:
                        ai_text = repo_agent.build_ai_decision_log_text(
                            user_task=user_task,
                            repo_profile=repo_profile,
                            style_profile=style_profile,
                            selected_control=selected_control,
                            selected_control_row=selected_control_row,
                            retrieved_chunks=retrieved_chunks,
                        )
                        st.session_state["generated_decision_log"] = {
                            "mode": "ai",
                            "signature": generation_signature,
                            "title": user_task,
                            "markdown": ai_text,
                        }
                    except Exception as exc:
                        fallback_log = repo_agent.build_decision_log(
                            user_task=user_task,
                            repo_profile=repo_profile,
                            style_profile=style_profile,
                            selected_control=selected_control,
                            selected_control_row=selected_control_row,
                            retrieved_chunks=retrieved_chunks,
                        )
                        st.session_state["generated_decision_log"] = {
                            "mode": "fallback",
                            "signature": generation_signature,
                            "title": fallback_log["title"],
                            "data": fallback_log,
                            "error": str(exc),
                        }

            decision_log = st.session_state.get("generated_decision_log")
            if decision_log and decision_log.get("signature") == generation_signature:
                if decision_log["mode"] == "ai":
                    st.success("Đã sinh Decision Log bằng AI từ repo context và mức kiểm soát hiện tại.")
                    st.markdown(decision_log["markdown"])
                    st.download_button(
                        "Tải decision log .md",
                        data=decision_log["markdown"].encode("utf-8"),
                        file_name="ai_pr_decision_log.md",
                        mime="text/markdown",
                    )
                else:
                    st.warning(f"Không gọi được AI, đang dùng bản fallback rule-based. Lỗi: {decision_log.get('error', 'không rõ')}")
                    fallback = decision_log["data"]
                    files_html = "".join(f"<li>{file}</li>" for file in fallback["files"][:5]) or "<li>Chưa retrieve được file liên quan.</li>"
                    reasons_html = "".join(f"<li>{item}</li>" for item in fallback["reasons"])
                    tradeoffs_html = "".join(f"<li>{item}</li>" for item in fallback["tradeoffs"])
                    risks_html = "".join(f"<li>{item}</li>" for item in fallback["risks"])
                    validation_html = "".join(f"<li>{item}</li>" for item in fallback["validation"])
                    fallback_md = (
                        f"# PR Decision Log: {fallback['title']}\n\n"
                        + "## File/context\n"
                        + "\n".join(f"- {file}" for file in fallback["files"])
                        + "\n\n## Lý do\n"
                        + "\n".join(f"- {item}" for item in fallback["reasons"])
                        + "\n\n## Trade-off\n"
                        + "\n".join(f"- {item}" for item in fallback["tradeoffs"])
                        + "\n\n## Rủi ro\n"
                        + "\n".join(f"- {item}" for item in fallback["risks"])
                        + "\n\n## Validation\n"
                        + "\n".join(f"- {item}" for item in fallback["validation"])
                    )
                    st.markdown(
                        f"""
                        <div class="pr-card">
                            <div class="pr-header">📄 PR #402: {fallback['title']}</div>
                            <b>AI lập luận quyết định (Defense):</b>
                            <ol>
                                <li><b>File/context được dùng:</b><ul>{files_html}</ul></li>
                                <li><b>Lý do chọn hướng xử lý:</b><ul>{reasons_html}</ul></li>
                                <li><b>Trade-off:</b><ul>{tradeoffs_html}</ul></li>
                                <li><b>Rủi ro & kiểm soát:</b><ul>{risks_html}</ul></li>
                                <li><b>Validation cần chạy:</b><ul>{validation_html}</ul></li>
                            </ol>
                            <div class="success-note">💡 <b>Kết quả:</b> PR có context repo, lý do kỹ thuật, trade-off và quality gate rõ ràng.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.download_button(
                        "Tải decision log .md",
                        data=fallback_md.encode("utf-8"),
                        file_name="ai_pr_decision_log.md",
                        mime="text/markdown",
                    )
            else:
                st.info("Nhập tác vụ, chọn mức kiểm soát rồi bấm nút để sinh Decision Log mới từ AI.")

    likely_files = [f"{chunk['path']} :: {chunk['symbol']}" for chunk in retrieved_chunks]
    context_snippets = "\n\n".join(
        f"### {chunk['path']} :: {chunk['symbol']}\n```text\n{chunk['content'][:1800]}\n```"
        for chunk in retrieved_chunks
    )
    if not context_snippets:
        context_snippets = "Chưa retrieve được đoạn code liên quan. Hãy upload repo hoặc nhập path repo đúng trước khi gọi AI."

    prompt = f"""Bạn là AI coding agent cho repository này.

Phạm vi nghề được phép hỗ trợ:
- {selected_occ}

Repo style:
- Framework/ngôn ngữ: {style_profile["Framework/ngôn ngữ"]}
- Cấu trúc project: {style_profile["Cấu trúc project"]}
- Config quan trọng: {style_profile["Config quan trọng"]}
- Test nên chạy: {style_profile["Test nên chạy"]}
- Lint/typecheck nên chạy: {style_profile["Lint/typecheck nên chạy"]}
- Mức kiểm soát AI Agent: {style_profile["Mức kiểm soát AI Agent"]}
- Coding style rút ra:
{style_profile["Coding style rút ra"]}
- Skill/convention bổ sung: {style_profile["Skill/convention bổ sung"]}

Các file liên quan cần đưa vào prompt/RAG:
{chr(10).join(f"- {name}" for name in likely_files) if likely_files else "- Chưa có file liên quan."}

Trích đoạn code liên quan từ repo:
{context_snippets}

Yêu cầu của người dùng:
{user_task}

Quy tắc bắt buộc:
- Không fine-tune model cho repo này; dùng RAG + style profile + prompt context.
- Tuân thủ mức kiểm soát đang chọn: {selected_control}.
- AI được làm: {selected_control_row['AI được làm']}
- Con người vẫn phải làm: {selected_control_row['Con người phải làm']}
- Sau khi sửa code, chạy validation loop: generate code -> test/lint/build -> đọc lỗi -> sửa -> chạy lại.
"""

    with st.expander("Xem hồ sơ repo, prompt RAG và validation loop"):
        metric_cols = st.columns(4)
        metric_cols[0].metric("File đã quét", repo_profile["file_count"])
        metric_cols[1].metric("Ngôn ngữ chính", next(iter(repo_profile["languages"]), "Chưa rõ"))
        metric_cols[2].metric("Framework", ", ".join(repo_profile["frameworks"][:2]))
        metric_cols[3].metric("Task critical", pct(occ_tasks["quality_critical_task"].mean() if len(occ_tasks) else np.nan))

        pipeline_df = pd.DataFrame(
            [
                {
                    "Bước": "1. Quét repo",
                    "Kết quả": f"{repo_profile['file_count']} file, framework: {', '.join(repo_profile['frameworks'])}",
                },
                {
                    "Bước": "2. Style profile",
                    "Kết quả": f"{len(inferred_style)} tín hiệu style/convention",
                },
                {
                    "Bước": "3. Chunk + index",
                    "Kết quả": f"{len(code_index)} chunk theo file/function/class/component",
                },
                {
                    "Bước": "4. Retrieve context",
                    "Kết quả": f"{len(retrieved_chunks)} đoạn code liên quan đến task",
                },
                {
                    "Bước": "5. Validation loop",
                    "Kết quả": f"Test: {style_profile['Test nên chạy']} | Lint: {style_profile['Lint/typecheck nên chạy']} | Build: {style_profile['Build nên chạy']}",
                },
            ]
        )
        st.dataframe(pipeline_df, width="stretch", hide_index=True)

        st.dataframe(
            pd.DataFrame({"Thành phần": list(style_profile.keys()), "Kết luận dùng cho AI Agent": list(style_profile.values())}),
            width="stretch",
            hide_index=True,
        )
        if retrieved_chunks:
            st.markdown("**Các đoạn code được retrieve vào prompt**")
            st.dataframe(
                pd.DataFrame(
                    {
                        "File": [chunk["path"] for chunk in retrieved_chunks],
                        "Symbol/chunk": [chunk["symbol"] for chunk in retrieved_chunks],
                        "Loại": [chunk["kind"] for chunk in retrieved_chunks],
                    }
                ),
                width="stretch",
                hide_index=True,
            )
            for chunk in retrieved_chunks[:3]:
                st.code(
                    f"# {chunk['path']} :: {chunk['symbol']}\n{chunk['content'][:1800]}",
                    language="text",
                )
        st.code(prompt, language="text")

        validation_commands = repo_agent.runnable_validation_commands(repo_profile)
        st.markdown("**Chạy validation thật trên repo**")
        if validation_commands:
            st.write("Các lệnh sẽ chạy:", ", ".join(f"`{cmd}`" for cmd in validation_commands))
            allow_run = st.checkbox(
                "Tôi hiểu các lệnh test/lint/build sẽ chạy trong repo đã chọn.",
                key="allow_repo_validation_run",
            )
            if st.button("Chạy test/lint/build", disabled=not allow_run, key="run_repo_validation_button"):
                validation_results = repo_agent.run_validation_commands(repo_path, validation_commands)
                summary_df = pd.DataFrame(
                    [
                        {key: value for key, value in result.items() if key != "Log"}
                        for result in validation_results
                    ]
                )
                st.dataframe(summary_df, width="stretch", hide_index=True)
                for result in validation_results:
                    st.code(f"$ {result['Lệnh']}\n{result['Log']}", language="text")
        else:
            st.info("Chưa phát hiện lệnh test/lint/build trong repo. Hãy kiểm tra package.json, pyproject.toml hoặc requirements.txt.")

    with st.expander("Vì sao không fine-tune ngay?"):
        st.markdown(
            """
            **Khuyến nghị:** dùng Prompt + RAG trước. Fine-tune chỉ nên dùng khi có nhiều ví dụ before/after,
            nhiều repo ổn định hoặc muốn học style chung của cả team. Với từng repo thay đổi liên tục,
            RAG cập nhật nhanh hơn, rẻ hơn và dễ kiểm soát bằng test/lint/build.
            """
        )


data = load_data()
tasks = clean_tasks(data["tasks"])
filtered_tasks = apply_filters(tasks)

st.title("AI Agent trong ngành khoa học máy tính: sự dịch chuyển kỹ năng")
st.markdown(
    """
    Dashboard này trực quan hóa phân tích từ dữ liệu task/nghề trong nhóm **Computer and Mathematical**.
    Câu chuyện chính: AI có thể làm tăng tốc độ tạo output kỹ thuật, nhưng chất lượng không tự đảm bảo.
    Vì vậy kỹ năng trọng tâm dịch chuyển sang review, test, kiểm chứng, bảo mật, maintainability và quản trị AI Agent.
    """
)

if tasks.empty:
    st.error("Không tìm thấy dữ liệu phân tích trong thư mục outputs.")
    st.stop()

metric_row(tasks, filtered_tasks)

tab_quality, tab_shift, tab_personalize = st.tabs(
    [
        "1. AI, output code và chất lượng",
        "2. Dịch chuyển kỹ năng và reskilling",
        "3. Cá nhân hóa AI Agent",
    ]
)

with tab_quality:
    st.subheader("AI có thể tăng output, nhưng quality gate vẫn là điểm nghẽn")
    st.markdown(
        """
        <div class="warning-box">
        <b>Lưu ý quan trọng:</b> dữ liệu hiện tại không đo trực tiếp defect rate, bug production
        hay failed CI. Vì vậy dashboard không kết luận cứng rằng AI làm chất lượng code giảm.
        Phân tích dùng các proxy như nhu cầu con người, độ bất định, chuyên môn miền và task critical
        để chỉ ra nơi cần review/test mạnh hơn khi dùng AI.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.4, 1])
    with left:
        st.plotly_chart(agent_quadrant(filtered_tasks), width="stretch")
    with right:
        st.plotly_chart(group_signal_chart(data["reskill_group"]), width="stretch")

    st.markdown(
        """
        <div class="explain-box">
        <b>Insight chính:</b> các task ở vùng tăng tốc cao nhưng rủi ro chất lượng cao không nên
        được hiểu là "cứ giao cho agent tự động". Cách triển khai hợp lý hơn là Copilot kèm review,
        test, logging và cơ chế rollback. Đây là điểm làm rõ câu chuyện: output có thể tăng,
        nhưng trách nhiệm chất lượng dịch sang con người và quy trình kiểm soát.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1.15])
    with left:
        st.plotly_chart(recommendation_chart(filtered_tasks), width="stretch")
    with right:
        st.plotly_chart(regression_chart(data["ols"], data["logit"]), width="stretch")

    regression_simulator(tasks, data["raw_tasks"], data["ols"], data["logit"], data["reg_ref"])

    st.subheader("Các task nên đọc kỹ trước khi tự động hóa")
    risky = filtered_tasks.dropna(subset=["code_acceleration_potential", "quality_risk_need"]).copy()
    risky["combined_attention_score"] = (
        0.45 * risky["code_acceleration_potential"]
        + 0.45 * risky["quality_risk_need"]
        + 0.10 * risky["quality_critical_task"].astype(float)
    )
    risky = risky.sort_values("combined_attention_score", ascending=False).head(15)
    st.dataframe(
        risky[
            [
                "Occupation (O*NET-SOC Title)",
                "Task",
                "task_group_vi",
                "quality_critical_task",
                "code_acceleration_potential",
                "quality_risk_need",
                "agent_recommendation",
            ]
        ],
        width="stretch",
        hide_index=True,
        column_config={
            "Occupation (O*NET-SOC Title)": "Nghề",
            "Task": "Task",
            "task_group_vi": "Nhóm task",
            "quality_critical_task": "Critical",
            "code_acceleration_potential": st.column_config.ProgressColumn(
                "Tăng tốc code", min_value=0, max_value=1, format="%.2f"
            ),
            "quality_risk_need": st.column_config.ProgressColumn(
                "Rủi ro chất lượng", min_value=0, max_value=1, format="%.2f"
            ),
            "agent_recommendation": "Khuyến nghị",
        },
    )

with tab_shift:
    st.subheader("Sự dịch chuyển kỹ năng: từ tạo code sang quản trị chất lượng code")
    pathway_view(data["pathway"])

    st.markdown(
        """
        <div class="explain-box">
        <b>Thông điệp để đưa vào báo cáo:</b> kỹ năng lập trình không biến mất.
        Nó dịch chuyển từ việc tự mình viết từng dòng code sang năng lực định hướng AI,
        kiểm tra code do AI tạo, thiết kế test, phát hiện lỗi logic, đánh giá kiến trúc
        và chịu trách nhiệm cuối cùng với chất lượng sản phẩm.
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.25, 1])
    with left:
        top_n = st.slider("Số nghề hiển thị", min_value=5, max_value=20, value=12, step=1)
        st.plotly_chart(reskill_occ_chart(data["reskill_occ"], top_n), width="stretch")
    with right:
        st.plotly_chart(reskill_group_chart(data["reskill_group"]), width="stretch")

    st.subheader("Bảng ưu tiên reskilling theo task")
    task_table = data["reskill_task"].copy()
    search = st.text_input(
        "Tìm task hoặc nghề",
        placeholder="Ví dụ: security, software, test, architect...",
    )
    if search and not task_table.empty:
        mask = (
            task_table["Task"].astype(str).str.contains(search, case=False, na=False)
            | task_table["Occupation (O*NET-SOC Title)"].astype(str).str.contains(search, case=False, na=False)
            | task_table["task_group_vi"].astype(str).str.contains(search, case=False, na=False)
        )
        task_table = task_table[mask]

    task_table = task_table.sort_values("reskilling_priority_score", ascending=False).head(30)
    st.dataframe(
        task_table[
            [
                "Occupation (O*NET-SOC Title)",
                "Task",
                "task_group_vi",
                "quality_critical_task",
                "reskilling_priority_score",
                "code_acceleration_potential",
                "quality_risk_need",
                "agent_recommendation",
            ]
        ],
        width="stretch",
        hide_index=True,
        column_config={
            "Occupation (O*NET-SOC Title)": "Nghề",
            "Task": "Task",
            "task_group_vi": "Nhóm task",
            "quality_critical_task": "Critical",
            "reskilling_priority_score": st.column_config.ProgressColumn(
                "Ưu tiên reskilling", min_value=0, max_value=1, format="%.2f"
            ),
            "code_acceleration_potential": st.column_config.ProgressColumn(
                "Tăng tốc code", min_value=0, max_value=1, format="%.2f"
            ),
            "quality_risk_need": st.column_config.ProgressColumn(
                "Rủi ro chất lượng", min_value=0, max_value=1, format="%.2f"
            ),
            "agent_recommendation": "Khuyến nghị",
        },
    )

    st.markdown(
        """
        <div class="warning-box">
        <b>Khuyến nghị triển khai:</b> bắt đầu với Copilot + review ở các task có điểm reskilling cao,
        vì đây là nơi AI có thể tăng tốc nhưng con người vẫn phải nắm quality gate.
        Với task critical như security, troubleshooting, backup, QA và kiến trúc hệ thống,
        không nên bỏ qua bước review bắt buộc.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_personalize:
    repo_personalization_solution_view(tasks, data["reskill_task"], data["raw_tasks"])

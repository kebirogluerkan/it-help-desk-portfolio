#!/usr/bin/env python3
"""Create KPI tables, charts, and a self-contained HTML dashboard."""

from __future__ import annotations

import argparse
import base64
import io
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


COLORS = {
    "navy": "#12304A",
    "blue": "#2563EB",
    "cyan": "#0891B2",
    "green": "#059669",
    "amber": "#D97706",
    "red": "#DC2626",
    "ink": "#172033",
    "muted": "#667085",
    "grid": "#E4E7EC",
    "paper": "#F7F9FC",
    "white": "#FFFFFF",
}

PRIORITY_ORDER = ["Critical", "High", "Medium", "Low"]


def load_tickets(csv_path: Path) -> pd.DataFrame:
    frame = pd.read_csv(csv_path)
    frame["opened_at"] = pd.to_datetime(frame["opened_at"])
    frame["resolved_at"] = pd.to_datetime(frame["resolved_at"], errors="coerce")
    frame["month"] = frame["opened_at"].dt.to_period("M").astype(str)
    return frame


def calculate_kpis(frame: pd.DataFrame) -> dict[str, float | int]:
    resolved = frame[frame["status"].isin(["Resolved", "Closed"])]
    backlog = frame[frame["status"].isin(["Open", "In Progress"])]
    return {
        "total_tickets": int(len(frame)),
        "resolved_tickets": int(len(resolved)),
        "open_backlog": int(len(backlog)),
        "resolution_rate_pct": round(100 * len(resolved) / len(frame), 1),
        "sla_compliance_pct": round(100 * (resolved["sla_met"] == "Yes").mean(), 1),
        "avg_resolution_hours": round(resolved["resolution_minutes"].mean() / 60, 2),
        "avg_csat": round(resolved["satisfaction_score"].mean(), 2),
        "reopen_rate_pct": round(100 * (resolved["reopened"] == "Yes").mean(), 1),
    }


def style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor(COLORS["white"])
    axis.grid(axis="y", color=COLORS["grid"], linewidth=0.8, alpha=0.8)
    axis.set_axisbelow(True)
    axis.tick_params(colors=COLORS["muted"], labelsize=9)
    for spine in axis.spines.values():
        spine.set_visible(False)


def save_individual_charts(frame: pd.DataFrame, charts_dir: Path) -> dict[str, Path]:
    charts_dir.mkdir(parents=True, exist_ok=True)
    chart_paths: dict[str, Path] = {}

    category = frame["category"].value_counts().sort_values()
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    fig.patch.set_facecolor(COLORS["white"])
    style_axis(ax)
    ax.barh(category.index, category.values, color=COLORS["blue"])
    ax.set_title("Ticket Volume by Category", loc="left", weight="bold", color=COLORS["ink"])
    ax.set_xlabel("Tickets", color=COLORS["muted"])
    fig.tight_layout()
    chart_paths["category"] = charts_dir / "category_volume.png"
    fig.savefig(chart_paths["category"], dpi=170, bbox_inches="tight")
    plt.close(fig)

    monthly = frame.groupby("month").agg(
        opened=("ticket_id", "count"),
        resolved=("status", lambda values: values.isin(["Resolved", "Closed"]).sum()),
    )
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    fig.patch.set_facecolor(COLORS["white"])
    style_axis(ax)
    ax.plot(monthly.index, monthly["opened"], marker="o", linewidth=2.5, color=COLORS["blue"], label="Opened")
    ax.plot(monthly.index, monthly["resolved"], marker="o", linewidth=2.5, color=COLORS["green"], label="Resolved")
    ax.set_title("Monthly Ticket Trend", loc="left", weight="bold", color=COLORS["ink"])
    ax.legend(frameon=False)
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    chart_paths["monthly"] = charts_dir / "monthly_trend.png"
    fig.savefig(chart_paths["monthly"], dpi=170, bbox_inches="tight")
    plt.close(fig)

    resolved = frame[frame["status"].isin(["Resolved", "Closed"])]
    sla = (
        resolved.groupby("priority")["sla_met"]
        .apply(lambda values: 100 * (values == "Yes").mean())
        .reindex(PRIORITY_ORDER)
    )
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    fig.patch.set_facecolor(COLORS["white"])
    style_axis(ax)
    bars = ax.bar(sla.index, sla.values, color=[COLORS["red"], COLORS["amber"], COLORS["blue"], COLORS["cyan"]])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Compliance %", color=COLORS["muted"])
    ax.set_title("SLA Compliance by Priority", loc="left", weight="bold", color=COLORS["ink"])
    ax.bar_label(bars, labels=[f"{value:.1f}%" for value in sla.values], padding=3, color=COLORS["ink"])
    fig.tight_layout()
    chart_paths["sla"] = charts_dir / "sla_by_priority.png"
    fig.savefig(chart_paths["sla"], dpi=170, bbox_inches="tight")
    plt.close(fig)

    status = frame["status"].value_counts()
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    fig.patch.set_facecolor(COLORS["white"])
    ax.pie(
        status.values,
        labels=status.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[COLORS["green"], COLORS["blue"], COLORS["amber"], COLORS["red"]],
        textprops={"color": COLORS["ink"], "fontsize": 9},
        wedgeprops={"linewidth": 2, "edgecolor": "white"},
    )
    ax.set_title("Ticket Status Distribution", loc="left", weight="bold", color=COLORS["ink"])
    fig.tight_layout()
    chart_paths["status"] = charts_dir / "status_distribution.png"
    fig.savefig(chart_paths["status"], dpi=170, bbox_inches="tight")
    plt.close(fig)
    return chart_paths


def create_dashboard_preview(frame: pd.DataFrame, kpis: dict[str, float | int], output: Path) -> None:
    fig = plt.figure(figsize=(16, 10), facecolor=COLORS["paper"])
    grid = fig.add_gridspec(3, 4, height_ratios=[0.72, 2.2, 2.2], hspace=0.42, wspace=0.36)

    cards = [
        ("Total Tickets", f"{kpis['total_tickets']:,}", COLORS["blue"]),
        ("Open Backlog", f"{kpis['open_backlog']:,}", COLORS["amber"]),
        ("SLA Compliance", f"{kpis['sla_compliance_pct']:.1f}%", COLORS["green"]),
        ("Average CSAT", f"{kpis['avg_csat']:.2f} / 5", COLORS["cyan"]),
    ]
    for column, (label, value, accent) in enumerate(cards):
        axis = fig.add_subplot(grid[0, column])
        axis.set_facecolor(COLORS["white"])
        axis.set_xticks([])
        axis.set_yticks([])
        for spine in axis.spines.values():
            spine.set_color(COLORS["grid"])
        axis.text(0.06, 0.72, label, transform=axis.transAxes, color=COLORS["muted"], fontsize=11, weight="bold")
        axis.text(0.06, 0.24, value, transform=axis.transAxes, color=COLORS["ink"], fontsize=24, weight="bold")
        axis.axvline(0.015, color=accent, linewidth=7)

    category_axis = fig.add_subplot(grid[1, :2])
    style_axis(category_axis)
    category = frame["category"].value_counts().sort_values()
    category_axis.barh(category.index, category.values, color=COLORS["blue"])
    category_axis.set_title("Ticket Volume by Category", loc="left", weight="bold", color=COLORS["ink"], pad=12)
    category_axis.set_xlabel("Tickets", color=COLORS["muted"])

    monthly_axis = fig.add_subplot(grid[1, 2:])
    style_axis(monthly_axis)
    monthly = frame.groupby("month").agg(
        opened=("ticket_id", "count"),
        resolved=("status", lambda values: values.isin(["Resolved", "Closed"]).sum()),
    )
    monthly_axis.plot(monthly.index, monthly["opened"], marker="o", linewidth=2.5, color=COLORS["blue"], label="Opened")
    monthly_axis.plot(monthly.index, monthly["resolved"], marker="o", linewidth=2.5, color=COLORS["green"], label="Resolved")
    monthly_axis.set_title("Monthly Ticket Trend", loc="left", weight="bold", color=COLORS["ink"], pad=12)
    monthly_axis.legend(frameon=False, loc="upper left")
    monthly_axis.tick_params(axis="x", rotation=35)

    sla_axis = fig.add_subplot(grid[2, :2])
    style_axis(sla_axis)
    resolved = frame[frame["status"].isin(["Resolved", "Closed"])]
    sla = resolved.groupby("priority")["sla_met"].apply(lambda values: 100 * (values == "Yes").mean()).reindex(PRIORITY_ORDER)
    bars = sla_axis.bar(sla.index, sla.values, color=[COLORS["red"], COLORS["amber"], COLORS["blue"], COLORS["cyan"]])
    sla_axis.set_ylim(0, 100)
    sla_axis.set_title("SLA Compliance by Priority", loc="left", weight="bold", color=COLORS["ink"], pad=12)
    sla_axis.bar_label(bars, labels=[f"{value:.1f}%" for value in sla.values], padding=3, color=COLORS["ink"])

    status_axis = fig.add_subplot(grid[2, 2:])
    status_axis.set_facecolor(COLORS["white"])
    status = frame["status"].value_counts()
    status_axis.pie(
        status.values,
        labels=status.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=[COLORS["green"], COLORS["blue"], COLORS["amber"], COLORS["red"]],
        textprops={"color": COLORS["ink"], "fontsize": 9},
        wedgeprops={"linewidth": 2, "edgecolor": "white"},
    )
    status_axis.set_title("Ticket Status Distribution", loc="left", weight="bold", color=COLORS["ink"], pad=12)

    fig.suptitle("IT Help Desk Operations Dashboard", x=0.055, y=0.985, ha="left", fontsize=22, weight="bold", color=COLORS["navy"])
    fig.text(0.055, 0.947, "Synthetic portfolio dataset | January-October 2026", fontsize=10, color=COLORS["muted"])
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=170, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)


def image_data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def create_html_dashboard(
    frame: pd.DataFrame,
    kpis: dict[str, float | int],
    chart_paths: dict[str, Path],
    output: Path,
) -> None:
    category_table = frame["category"].value_counts().rename_axis("Category").reset_index(name="Tickets")
    category_rows = "".join(
        f"<tr><td>{row.Category}</td><td>{row.Tickets}</td><td>{row.Tickets / len(frame):.1%}</td></tr>"
        for row in category_table.itertuples(index=False)
    )
    cards = [
        ("Total Tickets", f"{kpis['total_tickets']:,}"),
        ("Resolved", f"{kpis['resolved_tickets']:,}"),
        ("Open Backlog", f"{kpis['open_backlog']:,}"),
        ("SLA Compliance", f"{kpis['sla_compliance_pct']:.1f}%"),
        ("Avg Resolution", f"{kpis['avg_resolution_hours']:.2f} h"),
        ("Average CSAT", f"{kpis['avg_csat']:.2f} / 5"),
    ]
    card_html = "".join(f"<article class='card'><span>{label}</span><strong>{value}</strong></article>" for label, value in cards)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IT Help Desk Dashboard</title>
<style>
body{{margin:0;background:#f7f9fc;color:#172033;font-family:Arial,sans-serif}}main{{max-width:1250px;margin:auto;padding:34px}}
h1{{margin:0;color:#12304a}}.subtitle{{color:#667085;margin:8px 0 28px}}.cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}}
.card,.panel{{background:white;border:1px solid #e4e7ec;border-radius:12px;box-shadow:0 4px 16px rgba(18,48,74,.06)}}
.card{{padding:18px;border-left:6px solid #2563eb}}.card span{{display:block;color:#667085;font-weight:700;font-size:13px}}.card strong{{display:block;font-size:28px;margin-top:8px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:18px}}.panel{{padding:18px}}.panel h2{{font-size:17px;margin:0 0 14px}}img{{width:100%;height:auto}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:10px;border-bottom:1px solid #e4e7ec;text-align:left}}th{{color:#667085;font-size:12px;text-transform:uppercase}}
footer{{color:#667085;margin-top:24px;font-size:12px}}@media(max-width:800px){{.cards,.grid{{grid-template-columns:1fr}}}}
</style></head>
<body><main><h1>IT Help Desk Operations Dashboard</h1><p class="subtitle">Synthetic portfolio dataset | January-October 2026</p>
<section class="cards">{card_html}</section>
<section class="grid">
<article class="panel"><h2>Ticket Volume by Category</h2><img alt="Ticket volume by category" src="{image_data_uri(chart_paths['category'])}"></article>
<article class="panel"><h2>Monthly Ticket Trend</h2><img alt="Monthly ticket trend" src="{image_data_uri(chart_paths['monthly'])}"></article>
<article class="panel"><h2>SLA Compliance</h2><img alt="SLA compliance by priority" src="{image_data_uri(chart_paths['sla'])}"></article>
<article class="panel"><h2>Status Distribution</h2><img alt="Ticket status distribution" src="{image_data_uri(chart_paths['status'])}"></article>
<article class="panel"><h2>Category Summary</h2><table><thead><tr><th>Category</th><th>Tickets</th><th>Share</th></tr></thead><tbody>{category_rows}</tbody></table></article>
<article class="panel"><h2>Project Scope</h2><p>This dashboard demonstrates ticket categorization, prioritization, SLA monitoring, backlog tracking, SQL analysis, and service desk reporting.</p><p>All records are synthetic and contain no personal or production data.</p></article>
</section><footer>Generated by src/analyze.py | IT Help Desk Portfolio Project</footer></main></body></html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")


def write_tables(frame: pd.DataFrame, kpis: dict[str, float | int], reports_dir: Path) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([kpis]).to_csv(reports_dir / "kpis.csv", index=False)
    frame["category"].value_counts().rename_axis("category").reset_index(name="ticket_count").to_csv(
        reports_dir / "category_summary.csv", index=False
    )
    frame.groupby("month").agg(
        opened_tickets=("ticket_id", "count"),
        resolved_tickets=("status", lambda values: values.isin(["Resolved", "Closed"]).sum()),
    ).reset_index().to_csv(reports_dir / "monthly_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/helpdesk_tickets.csv"))
    parser.add_argument("--reports", type=Path, default=Path("reports"))
    parser.add_argument("--screenshot", type=Path, default=Path("screenshots/dashboard_preview.png"))
    args = parser.parse_args()
    frame = load_tickets(args.csv)
    kpis = calculate_kpis(frame)
    chart_paths = save_individual_charts(frame, args.reports / "charts")
    write_tables(frame, kpis, args.reports)
    create_dashboard_preview(frame, kpis, args.screenshot)
    create_html_dashboard(frame, kpis, chart_paths, args.reports / "dashboard.html")
    print(f"Created reports and dashboard for {len(frame)} tickets")


if __name__ == "__main__":
    main()

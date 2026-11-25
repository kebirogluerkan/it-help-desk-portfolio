#!/usr/bin/env python3
"""Validate portfolio data and write a machine-readable quality report."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


ALLOWED_STATUS = {"Open", "In Progress", "Resolved", "Closed"}
ALLOWED_PRIORITY = {"Low", "Medium", "High", "Critical"}
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+?\d[\s().-]*){10,}")


def validate(csv_path: Path) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["ticket_id"] for row in rows]
    if len(rows) < 400:
        errors.append("Dataset must contain at least 400 tickets.")
    if len(ids) != len(set(ids)):
        errors.append("ticket_id values must be unique.")

    for number, row in enumerate(rows, start=2):
        if row["status"] not in ALLOWED_STATUS:
            errors.append(f"Row {number}: invalid status {row['status']!r}.")
        if row["priority"] not in ALLOWED_PRIORITY:
            errors.append(f"Row {number}: invalid priority {row['priority']!r}.")
        if not row["opened_at"].startswith("2026-"):
            errors.append(f"Row {number}: opened_at must be in 2026.")
        if int(row["first_response_minutes"]) < 0 or int(row["sla_target_minutes"]) <= 0:
            errors.append(f"Row {number}: response and SLA values must be positive.")

        resolved = row["status"] in {"Resolved", "Closed"}
        required_when_resolved = ["resolved_at", "resolution_minutes", "sla_met", "satisfaction_score"]
        if resolved and any(not row[field] for field in required_when_resolved):
            errors.append(f"Row {number}: resolved ticket is missing resolution fields.")
        if not resolved and any(row[field] for field in required_when_resolved):
            errors.append(f"Row {number}: open ticket contains completed-resolution fields.")
        if resolved:
            resolution = int(row["resolution_minutes"])
            target = int(row["sla_target_minutes"])
            expected = "Yes" if resolution <= target else "No"
            if row["sla_met"] != expected:
                errors.append(f"Row {number}: sla_met does not match duration and target.")
            if not 1 <= int(row["satisfaction_score"]) <= 5:
                errors.append(f"Row {number}: satisfaction_score is outside 1-5.")

        combined_text = " ".join([row["summary"], row["resolution_note"]])
        if EMAIL_PATTERN.search(combined_text) or PHONE_PATTERN.search(combined_text):
            errors.append(f"Row {number}: possible personal data detected.")

    resolved_count = sum(row["status"] in {"Resolved", "Closed"} for row in rows)
    if resolved_count / max(len(rows), 1) < 0.70:
        warnings.append("Resolution rate is below 70%; confirm that this is intentional.")
    return {
        "status": "PASS" if not errors else "FAIL",
        "row_count": len(rows),
        "unique_ticket_ids": len(set(ids)),
        "resolved_ticket_count": resolved_count,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/helpdesk_tickets.csv"))
    parser.add_argument("--output", type=Path, default=Path("logs/quality_report.json"))
    args = parser.parse_args()
    report = validate(args.csv)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()

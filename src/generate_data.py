#!/usr/bin/env python3
"""Generate a deterministic, privacy-safe IT help desk ticket dataset."""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


SEED = 20261126
DEFAULT_ROWS = 420
START_DATE = datetime(2026, 1, 1, 8, 0)
END_DATE = datetime(2026, 10, 31, 18, 0)

PRIORITIES = {
    "Critical": {"weight": 4, "sla": 240, "response": 15},
    "High": {"weight": 16, "sla": 480, "response": 30},
    "Medium": {"weight": 50, "sla": 1440, "response": 120},
    "Low": {"weight": 30, "sla": 2880, "response": 240},
}

CATEGORIES = {
    "Access & Account": {
        "weight": 22,
        "team": "Service Desk",
        "items": {
            "Password Reset": (
                "User cannot sign in after a password change",
                "Identity verified and password reset guidance completed.",
            ),
            "Account Locked": (
                "Account is locked after repeated sign-in attempts",
                "Account status reviewed and access restored after verification.",
            ),
            "MFA Issue": (
                "Multi-factor authentication prompt cannot be completed",
                "Authentication method reviewed and user re-enrollment completed.",
            ),
        },
    },
    "Software": {
        "weight": 21,
        "team": "Desktop Support",
        "items": {
            "Application Crash": (
                "Business application closes unexpectedly during use",
                "Application logs reviewed; repair and update steps completed.",
            ),
            "Installation Request": (
                "Approved business software installation is requested",
                "Approval confirmed and supported application version installed.",
            ),
            "Update Failure": (
                "Application update fails with an installation error",
                "Temporary files cleared and update reinstalled successfully.",
            ),
        },
    },
    "Hardware": {
        "weight": 17,
        "team": "Desktop Support",
        "items": {
            "Laptop Performance": (
                "Laptop performance is slow during normal business use",
                "Startup items, storage health, and resource usage reviewed.",
            ),
            "Monitor Issue": (
                "External monitor is not detected by the workstation",
                "Cable, port, display settings, and graphics driver checked.",
            ),
            "Peripheral Issue": (
                "Keyboard, mouse, or USB peripheral is not recognized",
                "Device connection and driver status verified; device restored.",
            ),
        },
    },
    "Network": {
        "weight": 18,
        "team": "Network Support",
        "items": {
            "Wi-Fi Connection": (
                "Device connects to Wi-Fi but cannot reach business services",
                "IP configuration, gateway reachability, and adapter state checked.",
            ),
            "LAN Connection": (
                "Wired workstation has no network connectivity",
                "Physical link, adapter, DHCP lease, and switch path checked.",
            ),
            "VPN Connection": (
                "Remote user cannot establish the approved VPN connection",
                "Client configuration and authentication path reviewed and restored.",
            ),
        },
    },
    "Printer": {
        "weight": 10,
        "team": "Desktop Support",
        "items": {
            "Printer Offline": (
                "Shared printer appears offline for the user",
                "Power, connectivity, queue, and printer status checked.",
            ),
            "Print Queue": (
                "Documents remain stuck in the print queue",
                "Queue cleared and print service restarted after validation.",
            ),
            "Driver Issue": (
                "Printer driver is missing or incompatible",
                "Supported driver package installed and test page verified.",
            ),
        },
    },
    "Email & Collaboration": {
        "weight": 12,
        "team": "Service Desk",
        "items": {
            "Email Sync": (
                "Mailbox is not synchronizing recent messages",
                "Connectivity, profile status, and client synchronization reviewed.",
            ),
            "Meeting Audio": (
                "Audio device is unavailable during an online meeting",
                "Application permissions and audio device selection corrected.",
            ),
            "Calendar Access": (
                "Shared calendar access is unavailable",
                "Access request and client refresh steps completed.",
            ),
        },
    },
}

CHANNELS = ["Portal", "Email", "Phone", "Walk-in"]
CHANNEL_WEIGHTS = [44, 27, 22, 7]
DEPARTMENTS = ["Operations", "Finance", "Human Resources", "Sales", "Marketing", "Management"]
DEPARTMENT_WEIGHTS = [26, 16, 14, 20, 14, 10]
ASSIGNEES = {
    "Service Desk": ["SD-Tech-01", "SD-Tech-02", "SD-Tech-03"],
    "Desktop Support": ["DS-Tech-01", "DS-Tech-02", "DS-Tech-03"],
    "Network Support": ["NW-Tech-01", "NW-Tech-02"],
}


def weighted_choice(rng: random.Random, values: list[str], weights: list[int]) -> str:
    return rng.choices(values, weights=weights, k=1)[0]


def random_business_datetime(rng: random.Random) -> datetime:
    span_days = (END_DATE.date() - START_DATE.date()).days
    while True:
        day = START_DATE.date() + timedelta(days=rng.randint(0, span_days))
        if day.weekday() < 5:
            hour = rng.randint(8, 17)
            minute = rng.randint(0, 59)
            return datetime.combine(day, datetime.min.time()).replace(hour=hour, minute=minute)


def duration_for_priority(rng: random.Random, priority: str, sla: int) -> int:
    breach_probability = {"Critical": 0.24, "High": 0.22, "Medium": 0.17, "Low": 0.13}[priority]
    if rng.random() < breach_probability:
        return int(sla * rng.uniform(1.05, 2.6))
    return max(10, int(sla * rng.uniform(0.08, 0.92)))


def build_rows(row_count: int, seed: int) -> list[dict[str, object]]:
    rng = random.Random(seed)
    priority_names = list(PRIORITIES)
    priority_weights = [PRIORITIES[p]["weight"] for p in priority_names]
    category_names = list(CATEGORIES)
    category_weights = [CATEGORIES[c]["weight"] for c in category_names]
    rows: list[dict[str, object]] = []

    for index in range(1, row_count + 1):
        opened_at = random_business_datetime(rng)
        priority = weighted_choice(rng, priority_names, priority_weights)
        category = weighted_choice(rng, category_names, category_weights)
        category_meta = CATEGORIES[category]
        subcategory = rng.choice(list(category_meta["items"]))
        summary, resolution_note = category_meta["items"][subcategory]
        team = str(category_meta["team"])
        assignee = rng.choice(ASSIGNEES[team])
        sla = PRIORITIES[priority]["sla"]
        response_target = PRIORITIES[priority]["response"]
        status = weighted_choice(rng, ["Closed", "Resolved", "In Progress", "Open"], [58, 24, 11, 7])

        if status in {"Closed", "Resolved"}:
            resolution_minutes = duration_for_priority(rng, priority, sla)
            first_response_minutes = min(
                resolution_minutes,
                max(2, int(response_target * rng.uniform(0.15, 1.45))),
            )
            resolved_at = opened_at + timedelta(minutes=resolution_minutes)
            sla_met = "Yes" if resolution_minutes <= sla else "No"
            reopened = "Yes" if rng.random() < 0.075 else "No"
            base_score = 4.35 if sla_met == "Yes" else 3.25
            satisfaction_score = min(5, max(1, round(rng.gauss(base_score, 0.72))))
        else:
            first_response_minutes = max(2, int(response_target * rng.uniform(0.25, 1.8)))
            resolution_minutes = ""
            resolved_at = ""
            sla_met = ""
            reopened = "No"
            satisfaction_score = ""
            resolution_note = ""

        rows.append(
            {
                "ticket_id": f"HD-2026-{index:04d}",
                "opened_at": opened_at.isoformat(timespec="minutes"),
                "resolved_at": resolved_at.isoformat(timespec="minutes") if resolved_at else "",
                "status": status,
                "priority": priority,
                "category": category,
                "subcategory": subcategory,
                "channel": weighted_choice(rng, CHANNELS, CHANNEL_WEIGHTS),
                "requester_department": weighted_choice(rng, DEPARTMENTS, DEPARTMENT_WEIGHTS),
                "assigned_team": team,
                "assignee": assignee,
                "first_response_minutes": first_response_minutes,
                "resolution_minutes": resolution_minutes,
                "sla_target_minutes": sla,
                "sla_met": sla_met,
                "reopened": reopened,
                "satisfaction_score": satisfaction_score,
                "summary": summary,
                "resolution_note": resolution_note,
            }
        )
    return sorted(rows, key=lambda row: (str(row["opened_at"]), str(row["ticket_id"])))


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output", type=Path, default=Path("data/helpdesk_tickets.csv"))
    args = parser.parse_args()
    rows = build_rows(args.rows, args.seed)
    write_csv(rows, args.output)
    print(f"Generated {len(rows)} synthetic tickets: {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Load the generated CSV into a reproducible SQLite database."""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path


FIELDS = [
    "ticket_id", "opened_at", "resolved_at", "status", "priority", "category",
    "subcategory", "channel", "requester_department", "assigned_team", "assignee",
    "first_response_minutes", "resolution_minutes", "sla_target_minutes", "sla_met",
    "reopened", "satisfaction_score", "summary", "resolution_note",
]


def nullable(value: str) -> object:
    return None if value == "" else value


def load(csv_path: Path, db_path: Path, schema_path: Path) -> int:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    try:
        connection.executescript(schema_path.read_text(encoding="utf-8"))
        with csv_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        placeholders = ", ".join("?" for _ in FIELDS)
        statement = f"INSERT INTO tickets ({', '.join(FIELDS)}) VALUES ({placeholders})"
        values = []
        for row in rows:
            prepared = [nullable(row[field]) for field in FIELDS]
            for field in ("first_response_minutes", "resolution_minutes", "sla_target_minutes", "satisfaction_score"):
                position = FIELDS.index(field)
                if prepared[position] is not None:
                    prepared[position] = int(str(prepared[position]))
            values.append(prepared)
        connection.executemany(statement, values)
        connection.commit()
        return connection.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("data/helpdesk_tickets.csv"))
    parser.add_argument("--database", type=Path, default=Path("database/helpdesk.db"))
    parser.add_argument("--schema", type=Path, default=Path("sql/schema.sql"))
    args = parser.parse_args()
    count = load(args.csv, args.database, args.schema)
    print(f"Loaded {count} tickets into {args.database}")


if __name__ == "__main__":
    main()

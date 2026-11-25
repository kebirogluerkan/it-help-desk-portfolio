#!/usr/bin/env python3
"""Small command-line interface for browsing the SQLite help desk dataset."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def connection(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    return db


def list_tickets(db: sqlite3.Connection, status: str | None, limit: int) -> None:
    query = "SELECT ticket_id, opened_at, status, priority, category, summary FROM tickets"
    params: list[object] = []
    if status:
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY opened_at DESC LIMIT ?"
    params.append(limit)
    rows = db.execute(query, params).fetchall()
    for row in rows:
        print(f"{row['ticket_id']} | {row['status']:<11} | {row['priority']:<8} | {row['category']:<22} | {row['summary']}")


def show_ticket(db: sqlite3.Connection, ticket_id: str) -> None:
    row = db.execute("SELECT * FROM tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
    if not row:
        raise SystemExit(f"Ticket not found: {ticket_id}")
    for key in row.keys():
        print(f"{key:24}: {row[key] if row[key] is not None else ''}")


def show_stats(db: sqlite3.Connection) -> None:
    row = db.execute(
        """
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN status IN ('Open','In Progress') THEN 1 ELSE 0 END) AS backlog,
               ROUND(100.0 * SUM(CASE WHEN sla_met='Yes' THEN 1 ELSE 0 END)
                 / NULLIF(SUM(CASE WHEN status IN ('Resolved','Closed') THEN 1 ELSE 0 END),0),1) AS sla_pct,
               ROUND(AVG(satisfaction_score),2) AS csat
        FROM tickets
        """
    ).fetchone()
    print(f"Total tickets : {row['total']}")
    print(f"Open backlog  : {row['backlog']}")
    print(f"SLA compliance: {row['sla_pct']}%")
    print(f"Average CSAT  : {row['csat']} / 5")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=Path("database/helpdesk.db"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List recent tickets")
    list_parser.add_argument("--status", choices=["Open", "In Progress", "Resolved", "Closed"])
    list_parser.add_argument("--limit", type=int, default=10)

    show_parser = subparsers.add_parser("show", help="Show one ticket")
    show_parser.add_argument("ticket_id")
    subparsers.add_parser("stats", help="Show executive KPIs")

    args = parser.parse_args()
    with connection(args.database) as db:
        if args.command == "list":
            list_tickets(db, args.status, args.limit)
        elif args.command == "show":
            show_ticket(db, args.ticket_id)
        else:
            show_stats(db)


if __name__ == "__main__":
    main()

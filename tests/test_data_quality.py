from __future__ import annotations

import csv
import sqlite3
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "helpdesk_tickets.csv"
DB_PATH = ROOT / "database" / "helpdesk.db"


class HelpDeskDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with CSV_PATH.open(newline="", encoding="utf-8") as handle:
            cls.rows = list(csv.DictReader(handle))

    def test_dataset_has_portfolio_scale(self) -> None:
        self.assertGreaterEqual(len(self.rows), 400)

    def test_ticket_ids_are_unique(self) -> None:
        ids = [row["ticket_id"] for row in self.rows]
        self.assertEqual(len(ids), len(set(ids)))

    def test_resolution_fields_are_consistent(self) -> None:
        for row in self.rows:
            resolved = row["status"] in {"Resolved", "Closed"}
            self.assertEqual(bool(row["resolved_at"]), resolved)
            self.assertEqual(bool(row["resolution_minutes"]), resolved)
            self.assertEqual(bool(row["sla_met"]), resolved)

    def test_sla_logic_is_correct(self) -> None:
        for row in self.rows:
            if row["resolution_minutes"]:
                expected = "Yes" if int(row["resolution_minutes"]) <= int(row["sla_target_minutes"]) else "No"
                self.assertEqual(row["sla_met"], expected)

    def test_database_and_csv_counts_match(self) -> None:
        with sqlite3.connect(DB_PATH) as db:
            db_count = db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
            view_count = db.execute("SELECT COUNT(*) FROM v_monthly_volume").fetchone()[0]
        self.assertEqual(db_count, len(self.rows))
        self.assertGreaterEqual(view_count, 10)


if __name__ == "__main__":
    unittest.main()

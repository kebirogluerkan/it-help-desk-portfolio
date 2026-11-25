PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS v_agent_performance;
DROP VIEW IF EXISTS v_monthly_volume;
DROP VIEW IF EXISTS v_open_backlog;
DROP VIEW IF EXISTS v_sla_summary;
DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
    ticket_id TEXT PRIMARY KEY,
    opened_at TEXT NOT NULL,
    resolved_at TEXT,
    status TEXT NOT NULL CHECK (status IN ('Open', 'In Progress', 'Resolved', 'Closed')),
    priority TEXT NOT NULL CHECK (priority IN ('Low', 'Medium', 'High', 'Critical')),
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    channel TEXT NOT NULL,
    requester_department TEXT NOT NULL,
    assigned_team TEXT NOT NULL,
    assignee TEXT NOT NULL,
    first_response_minutes INTEGER NOT NULL CHECK (first_response_minutes >= 0),
    resolution_minutes INTEGER,
    sla_target_minutes INTEGER NOT NULL CHECK (sla_target_minutes > 0),
    sla_met TEXT CHECK (sla_met IN ('Yes', 'No') OR sla_met IS NULL),
    reopened TEXT NOT NULL CHECK (reopened IN ('Yes', 'No')),
    satisfaction_score INTEGER CHECK (satisfaction_score BETWEEN 1 AND 5 OR satisfaction_score IS NULL),
    summary TEXT NOT NULL,
    resolution_note TEXT
);

CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_category ON tickets(category);
CREATE INDEX idx_tickets_opened_at ON tickets(opened_at);

CREATE VIEW v_sla_summary AS
SELECT
    priority,
    COUNT(*) AS resolved_tickets,
    SUM(CASE WHEN sla_met = 'Yes' THEN 1 ELSE 0 END) AS sla_met_tickets,
    ROUND(100.0 * SUM(CASE WHEN sla_met = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_compliance_pct,
    ROUND(AVG(resolution_minutes) / 60.0, 2) AS avg_resolution_hours
FROM tickets
WHERE status IN ('Resolved', 'Closed')
GROUP BY priority;

CREATE VIEW v_open_backlog AS
SELECT priority, category, COUNT(*) AS open_tickets
FROM tickets
WHERE status IN ('Open', 'In Progress')
GROUP BY priority, category;

CREATE VIEW v_monthly_volume AS
SELECT
    SUBSTR(opened_at, 1, 7) AS month,
    COUNT(*) AS opened_tickets,
    SUM(CASE WHEN status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS resolved_tickets
FROM tickets
GROUP BY SUBSTR(opened_at, 1, 7);

CREATE VIEW v_agent_performance AS
SELECT
    assignee,
    assigned_team,
    COUNT(*) AS assigned_tickets,
    SUM(CASE WHEN status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS resolved_tickets,
    ROUND(AVG(CASE WHEN status IN ('Resolved', 'Closed') THEN resolution_minutes END) / 60.0, 2) AS avg_resolution_hours,
    ROUND(AVG(CASE WHEN status IN ('Resolved', 'Closed') THEN satisfaction_score END), 2) AS avg_csat
FROM tickets
GROUP BY assignee, assigned_team;

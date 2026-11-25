-- 1. Executive KPI summary
SELECT
    COUNT(*) AS total_tickets,
    SUM(CASE WHEN status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS resolved_tickets,
    SUM(CASE WHEN status IN ('Open', 'In Progress') THEN 1 ELSE 0 END) AS open_backlog,
    ROUND(100.0 * SUM(CASE WHEN sla_met = 'Yes' THEN 1 ELSE 0 END)
        / NULLIF(SUM(CASE WHEN status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END), 0), 1) AS sla_compliance_pct,
    ROUND(AVG(CASE WHEN status IN ('Resolved', 'Closed') THEN resolution_minutes END) / 60.0, 2) AS avg_resolution_hours,
    ROUND(AVG(satisfaction_score), 2) AS avg_csat
FROM tickets;

-- 2. SLA performance by priority
SELECT * FROM v_sla_summary
ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END;

-- 3. Most frequent ticket categories
SELECT category, COUNT(*) AS ticket_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM tickets), 1) AS share_pct
FROM tickets
GROUP BY category
ORDER BY ticket_count DESC;

-- 4. Top recurring issues
SELECT category, subcategory, COUNT(*) AS occurrences
FROM tickets
GROUP BY category, subcategory
ORDER BY occurrences DESC
LIMIT 10;

-- 5. Open backlog by priority and category
SELECT * FROM v_open_backlog
ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END,
         open_tickets DESC;

-- 6. Monthly ticket volume and resolution count
SELECT * FROM v_monthly_volume ORDER BY month;

-- 7. Support team workload and performance
SELECT assigned_team,
       COUNT(*) AS assigned_tickets,
       SUM(CASE WHEN status IN ('Resolved', 'Closed') THEN 1 ELSE 0 END) AS resolved_tickets,
       ROUND(AVG(CASE WHEN status IN ('Resolved', 'Closed') THEN resolution_minutes END) / 60.0, 2) AS avg_resolution_hours,
       ROUND(AVG(satisfaction_score), 2) AS avg_csat
FROM tickets
GROUP BY assigned_team
ORDER BY assigned_tickets DESC;

-- 8. Reopen rate by category
SELECT category,
       COUNT(*) AS resolved_tickets,
       SUM(CASE WHEN reopened = 'Yes' THEN 1 ELSE 0 END) AS reopened_tickets,
       ROUND(100.0 * SUM(CASE WHEN reopened = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS reopen_rate_pct
FROM tickets
WHERE status IN ('Resolved', 'Closed')
GROUP BY category
ORDER BY reopen_rate_pct DESC;

-- 9. Average first-response time by channel
SELECT channel,
       COUNT(*) AS ticket_count,
       ROUND(AVG(first_response_minutes), 1) AS avg_first_response_minutes
FROM tickets
GROUP BY channel
ORDER BY avg_first_response_minutes;

-- 10. Technician-level performance view
SELECT * FROM v_agent_performance
ORDER BY resolved_tickets DESC, avg_csat DESC;

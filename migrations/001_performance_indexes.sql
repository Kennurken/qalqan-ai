-- Qalqan AI — performance indexes + geo columns
-- Run ONCE in Supabase → SQL Editor. Safe to re-run (IF NOT EXISTS).
-- Speeds up /dashboard, /trends, /stats, /community as data grows
-- (those order by created_at and aggregate by domain).

-- Geo columns for the KZ regional threat map (captured from Vercel headers).
alter table check_logs add column if not exists country text;
alter table check_logs add column if not exists region  text;

-- check_logs: analytics ordering + domain/verdict aggregation
create index if not exists idx_check_logs_created_at on check_logs (created_at desc);
create index if not exists idx_check_logs_domain     on check_logs (domain);
create index if not exists idx_check_logs_verdict    on check_logs (verdict);

-- reports: crowd-intelligence ordering + dedup/aggregation
create index if not exists idx_reports_created_at on reports (created_at desc);
create index if not exists idx_reports_domain     on reports (domain);
create index if not exists idx_reports_category   on reports (category);

-- appeals: admin dashboard ordering
create index if not exists idx_appeals_created_at on appeals (created_at desc);

-- Optional: partial index for the federated feed query (category ilike 'federated%')
create index if not exists idx_reports_federated on reports (domain)
  where category like 'federated%';

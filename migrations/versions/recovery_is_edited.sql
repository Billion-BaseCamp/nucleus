-- Run ONLY if alembic left is_edited nullable or partially applied.
-- Check state first:
--   SELECT version_num FROM alembic_version;
--   SELECT table_name, column_name, is_nullable, column_default
--   FROM information_schema.columns
--   WHERE table_name IN ('itr_tds_salary','itr_tds_non_salary','itr_tds_property','itr_tcs')
--     AND column_name = 'is_edited';

-- Backfill NULLs then enforce NOT NULL + default
UPDATE itr_tds_salary SET is_edited = FALSE WHERE is_edited IS NULL;
UPDATE itr_tds_non_salary SET is_edited = FALSE WHERE is_edited IS NULL;
UPDATE itr_tds_property SET is_edited = FALSE WHERE is_edited IS NULL;
UPDATE itr_tcs SET is_edited = FALSE WHERE is_edited IS NULL;

ALTER TABLE itr_tds_salary
    ALTER COLUMN is_edited SET DEFAULT FALSE,
    ALTER COLUMN is_edited SET NOT NULL;
ALTER TABLE itr_tds_non_salary
    ALTER COLUMN is_edited SET DEFAULT FALSE,
    ALTER COLUMN is_edited SET NOT NULL;
ALTER TABLE itr_tds_property
    ALTER COLUMN is_edited SET DEFAULT FALSE,
    ALTER COLUMN is_edited SET NOT NULL;
ALTER TABLE itr_tcs
    ALTER COLUMN is_edited SET DEFAULT FALSE,
    ALTER COLUMN is_edited SET NOT NULL;

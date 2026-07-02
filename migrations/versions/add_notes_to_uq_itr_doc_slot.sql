-- Add `notes` to the itr_document_slots unique key so a client can hold
-- multiple custom/"Other" broker slots (one per note) under the same
-- (financial_year_id, client_id, doc_type, sub_type, source, region).
--
-- NULLS NOT DISTINCT keeps normal slots (notes IS NULL) de-duplicated exactly
-- as before. Requires PostgreSQL 15+.
--
-- Apply with:  psql "$DATABASE_URL" -f add_notes_to_uq_itr_doc_slot.sql

BEGIN;

ALTER TABLE itr_document_slots
    DROP CONSTRAINT IF EXISTS uq_itr_doc_slot;

ALTER TABLE itr_document_slots
    ADD CONSTRAINT uq_itr_doc_slot
    UNIQUE NULLS NOT DISTINCT
    (financial_year_id, client_id, doc_type, sub_type, source, region, notes);

COMMIT;

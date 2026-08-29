CREATE TABLE pdf_file (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    uuid VARCHAR(40) NOT NULL UNIQUE,

    uploaded_at TIMESTAMPTZ NOT NULL,

    document_name VARCHAR(255) NOT NULL,

    signature VARCHAR(64),

    storage_key TEXT,

    status VARCHAR(20) NOT NULL
        DEFAULT 'INCOMPLETE',

    CONSTRAINT chk_pdf_file_status
        CHECK (status IN ('INCOMPLETE', 'PENDING', 'COMPLETE'))
);

CREATE TABLE pdf_content (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    uuid_pdf  VARCHAR(40) NOT NULL UNIQUE,

    content BYTEA NOT NULL,

    CONSTRAINT fk_pdf_content_pdf_file
        FOREIGN KEY (uuid_pdf)
        REFERENCES pdf_file(uuid)
        ON DELETE CASCADE
);

ALTER TABLE pdf_file
ADD COLUMN file_size BIGINT;


BEGIN;

ALTER TABLE pdf_file
RENAME COLUMN uploaded_at TO upload_at;

ALTER TABLE pdf_file
RENAME COLUMN document_name TO file_name;

ALTER TABLE pdf_file
DROP COLUMN storage_key;

COMMIT;
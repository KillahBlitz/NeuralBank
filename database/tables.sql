CREATE TABLE pdf_file (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid        VARCHAR(40)  NOT NULL UNIQUE,
    upload_at   TIMESTAMPTZ  NOT NULL,
    file_name   VARCHAR(255) NOT NULL,
    signature   VARCHAR(64),
    status      VARCHAR(20)  NOT NULL DEFAULT 'INCOMPLETE',
    file_size   BIGINT,
    pages       INT,

    CONSTRAINT chk_pdf_file_status
        CHECK (status IN ('INCOMPLETE', 'PENDING', 'COMPLETE'))
);


CREATE TABLE pdf_content (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid_pdf    VARCHAR(40) NOT NULL UNIQUE,
    content     BYTEA       NOT NULL,
    pages       INT,

    CONSTRAINT fk_pdf_content_pdf_file
        FOREIGN KEY (uuid_pdf)
        REFERENCES pdf_file(uuid)
        ON DELETE CASCADE
);


CREATE TABLE image_file (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uuid        VARCHAR(40)  NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ  NOT NULL,
    file_name   VARCHAR(255) NOT NULL,
    file_bytes  BYTEA        NOT NULL,
    signature   VARCHAR(64)  NOT NULL,
    page_number INT          NOT NULL,
    uuid_pdf    VARCHAR(40)  NOT NULL,

    CONSTRAINT fk_image_file_pdf_file
        FOREIGN KEY (uuid_pdf)
        REFERENCES pdf_file(uuid)
        ON DELETE CASCADE
);

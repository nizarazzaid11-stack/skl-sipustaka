-- ============================================================
-- SIPUSTAKA — Script Pembuatan Tabel PostgreSQL
-- Jalankan script ini sebelum menjalankan aplikasi Django
-- ============================================================

-- Buat database (jalankan sebagai superuser di psql):
-- CREATE DATABASE sipustaka_db;
-- \c sipustaka_db

-- ── Tabel Buku ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS buku (
    id          SERIAL PRIMARY KEY,
    judul       VARCHAR(255) NOT NULL,
    pengarang   VARCHAR(255) NOT NULL,
    kategori    VARCHAR(50)  NOT NULL,
    penerbit    VARCHAR(255) NOT NULL,
    tahun_terbit INTEGER     NOT NULL,
    rak         VARCHAR(20)  NOT NULL,
    stok        INTEGER      NOT NULL DEFAULT 0,
    deskripsi   TEXT
);

-- ── Tabel Siswa ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS siswa (
    id        SERIAL PRIMARY KEY,
    nama      VARCHAR(255) NOT NULL,
    kelas     VARCHAR(50)  NOT NULL,
    nis       VARCHAR(20)  NOT NULL UNIQUE,
    is_active BOOLEAN      NOT NULL DEFAULT TRUE
);

-- ── Tabel Peminjaman ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS peminjaman (
    id             SERIAL PRIMARY KEY,
    siswa_id       INTEGER      NOT NULL REFERENCES siswa(id) ON DELETE CASCADE,
    buku_id        INTEGER      NOT NULL REFERENCES buku(id)  ON DELETE CASCADE,
    tanggal_pinjam DATE         NOT NULL,
    jatuh_tempo    DATE         NOT NULL,
    keperluan      TEXT,
    status         VARCHAR(20)  NOT NULL DEFAULT 'Dipinjam'
);

-- ── Tabel Sessions Django (wajib untuk messages) ────────────
CREATE TABLE IF NOT EXISTS django_session (
    session_key  VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data TEXT        NOT NULL,
    expire_date  TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS django_session_expire_date ON django_session(expire_date);

-- ── Data Contoh ─────────────────────────────────────────────
INSERT INTO buku (judul, pengarang, kategori, penerbit, tahun_terbit, rak, stok, deskripsi) VALUES
    ('Laskar Pelangi',  'Andrea Hirata', 'Novel',      'Bentang Pustaka',       2005, 'Rak A-01', 5, 'Novel tentang semangat belajar anak-anak Belitung.'),
    ('Bumi',            'Tere Liye',     'Novel',      'Gramedia Pustaka Utama', 2014, 'Rak A-02', 7, 'Serial fantasi anak-anak bumi.'),
    ('Negeri 5 Menara', 'A. Fuadi',      'Novel',      'Gramedia Pustaka Utama', 2009, 'Rak A-03', 2, 'Kisah inspiratif tentang pesantren.')
ON CONFLICT DO NOTHING;

INSERT INTO siswa (nama, kelas, nis, is_active) VALUES
    ('Roni',          'XI IPA 1', '2026001', TRUE),
    ('Sinta',         'XI IPS 2', '2026002', TRUE),
    ('Dewi Anggraini','X IPA 3',  '2026003', TRUE),
    ('Bima Pratama',  'XII IPS 1','2026004', TRUE)
ON CONFLICT DO NOTHING;

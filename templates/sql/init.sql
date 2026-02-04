CREATE TABLE IF NOT EXISTS user(
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    qid             INTEGER NOT NULL,
    permitted_group TEXT    NOT NULL
);
#EOS
CREATE TABLE IF NOT EXISTS announces(
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    sender          INTEGER NOT NULL,
    target_group    TEXT    NOT NULL,
    ann_type        TEXT    NOT NULL,
    content         BLOB
);
#EOS
CREATE TABLE IF NOT EXISTS username_cache(
    id              INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    qid             INTEGER NOT NULL UNIQUE,
    username        TEXT    NOT NULL,
    last_update     DATE
);
#EOF
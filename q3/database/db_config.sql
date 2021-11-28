DROP TABLE IF EXISTS vote;
DROP TABLE IF EXISTS candidate;

CREATE TABLE vote (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    candidate_id INTEGER NOT NULL,
    opinion TEXT,
    FOREIGN KEY (candidate_id)
    REFERENCES candidate (id)
       ON UPDATE RESTRICT
       ON DELETE RESTRICT
);

CREATE TABLE candidate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

INSERT INTO candidate (name)
VALUES
   ('薯片'),
   ('林林'),
   ('正氣');
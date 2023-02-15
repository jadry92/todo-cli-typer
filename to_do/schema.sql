CREATE TABLE IF NOT EXISTS to_do (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(200) NOT NULL,
  date timestamp,
  done_by timestamp,
  done BOOL
);

CREATE TABLE IF NOT EXISTS sub_task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  description TEXT,
  to_do_id INTEGER NOT NULL,
  FOREIGN KEY(to_do_id) REFERENCES to_do(id) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE
);
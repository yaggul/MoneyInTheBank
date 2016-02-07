CREATE TABLE IF NOT EXISTS clients(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT,
   password TEXT,
   salt TEXT,
   balance REAL DEFAULT 0,
   message TEXT);


CREATE TABLE IF NOT EXISTS login_attempts(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   client_id INTEGER,
   attempt_status TEXT,
   time_stamp DATETIME,
   FOREIGN KEY(client_id) REFERENCES clients(id));

CREATE TABLE IF NOT EXISTS blocked_users(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   client_id INTEGER,
   block_start DATETIME,
   block_end DATETIME,
   FOREIGN KEY(client_id) REFERENCES clients(id));

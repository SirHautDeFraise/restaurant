DROP TABLE users;
DROP TABLE tables;
DROP TABLE reservations;

CREATE TABLE IF NOT EXISTS users (
	id INTEGER Primary Key AutoIncrement,
	firstname TEXT,
	lastname TEXT,
	mail TEXT,
	password TEXT
);

CREATE TABLE IF NOT EXISTS tables (
	id INTEGER,
    period TEXT,
	status TEXT NOT NULL,
	seats INTEGER NOT NULL,
	PRIMARY KEY (id, period)
);

CREATE TABLE IF NOT EXISTS reservations (
	id INTEGER PRIMARY KEY,
	id_table INTEGER,
	date DATE,
	id_user INTEGER,
	Foreign key (id_table) References tables(id),
	Foreign key (id_user) References users(id)
);

INSERT INTO users(firstname, lastname, mail, password) VALUES
	('thibault', 'laude', 'thibou@gmail.com', 'mdp');


INSERT INTO tables(id,period,status,seats) VALUES
	(1,'midi','libre',2),
	(1,'soir','libre',2),
	(2,'midi','occupé',4),
	(2,'soir','occupé',4),
	(3,'midi','libre',6),
	(3,'soir','libre',6),
	(4,'soir','libre',10);.
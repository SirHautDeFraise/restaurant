DROP TABLE users;
DROP TABLE tables;
DROP TABLE reservations;

CREATE TABLE users (
	id INTEGER Primary Key AutoIncrement,
	firstname TEXT,
	lastname TEXT,
	mail TEXT,
	password TEXT
);

CREATE TABLE tables (
	id INTEGER,
    periode TEXT,
	status TEXT NOT NULL,
	seats INTEGER NOT NULL,
	PRIMARY KEY (id, periode)
);

CREATE TABLE reservations (
	id INTEGER PRIMARY KEY,
	id_table INTEGER,
	date DATE,
	id_user INTEGER,
	Foreign key (id_table) References tables(id),
	Foreign key (id_user) References users(id)
);

INSERT INTO users(firstname, lastname) VALUES
	('olivier', 'giroud'),
	('michel', 'taleur'),
	('lucas', 'titou');

INSERT INTO tables(id,periode,status,seats) VALUES
	(1,'Midi','Libre',2),
	(1,'Soir','Libre',2),
	(2,'Midi','Occupé',4),
	(2,'Soir','Occupé',4),
	(3,'Midi','Libre',6),
	(3,'Soir','Libre',6),
	(4,'Soir','Libre',10);
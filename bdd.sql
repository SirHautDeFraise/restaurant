CREATE TABLE users (
	id INTEGER Primary Key AutoIncrement,
	firstname TEXT,
	lastname TEXT,
	mail TEXT,
	password TEXT
);

CREATE TABLE tables (
	id INTEGER PRIMARY KEY AutoIncrement,
	seats INTEGER NOT NULL	
);

CREATE TABLE reservations (
	id INTEGER PRIMARY KEY AutoIncrement,
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

INSERT INTO tables(seats) VALUES
	(2),
	(6),
	(5),
	(4),
	(6),
	(8),
	(6),
	(4),
	(4),
	(6),
	(5);




	






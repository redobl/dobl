-- items definition

CREATE TABLE items (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	look TEXT NOT NULL,
	"type" TEXT NOT NULL,
	"attributes" TEXT NOT NULL,
	durability INTEGER,
	weight INTEGER,
	slot TEXT
);

-- abilities definition

CREATE TABLE abilities (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"type" TEXT NOT NULL,
	"text" TEXT NOT NULL
);
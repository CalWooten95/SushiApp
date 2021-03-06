DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orderedItems;
DROP TABLE IF EXISTS refills;
DROP TABLE IF EXISTS help;
DROP TABLE IF EXISTS sales;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  type INTEGER NOT NULL

);

CREATE TABLE items (
  iid INTEGER PRIMARY KEY AUTOINCREMENT,
  price FLOAT NOT NULL,
  itemName TEXT NOT NULL,
  description TEXT NOT NULL,
  type TEXT NOT NULL,
  link TEXT

);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  custID INTEGER NOT NULL,
  total FLOAT NOT NULL,
  comments TEXT NULL,
  FOREIGN KEY (custID) REFERENCES user(id)
);

CREATE TABLE orderedItems (
    iid INTEGER NOT NULL,
    uid INTEGER NOT NULL,
    active INTEGER NOT NULL,
    completed INTEGER,
    timePlaced INTEGER,
    comments TEXT,
    FOREIGN KEY (uid) REFERENCES user(id),
    FOREIGN KEY (iid) REFERENCES items(iid)
);

CREATE TABLE refills(
	iid INTEGER PRIMARY KEY AUTOINCREMENT,
	tablenumber INTEGER NOT NULL,
	seatnumber INTEGER NOT NULL,
	beverage TEXT NOT NULL
);

CREATE TABLE help(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	tablenumber INTEGER NOT NULL
);

CREATE TABLE sales (
  uid INTEGER NOT NULL,
  timePlaced INTEGER,
  total FLOAT NOT NULL,
	tip FLOAT NOT NULL,
  refunded INTEGER,
  FOREIGN KEY (uid) REFERENCES user(id)
);

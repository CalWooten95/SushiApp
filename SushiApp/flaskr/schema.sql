DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS refills;

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
  type TEXT NOT NULL

);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  seatnum INTEGER NOT NULL,
  ordernum INTEGER NOT NULL,
  tablenum INTEGER NOT NULL,
  custID INTEGER NOT NULL,
  total FLOAT NOT NULL,
  itemName TEXT NOT NULL,
  orderItems TEXT NOT NULL,
  comments TEXT NOT NULL

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
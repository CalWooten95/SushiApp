DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS orderedItems;
DROP TABLE IF EXISTS refills;
DROP TABLE IF EXISTS help;

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

INSERT INTO items (iid, price, itemName, description, type, link)
VALUES
(203, 10.99, 'California Sushi Roll', 'Standard California roll', 'entree', 'https://anyrecipe.net/asian/recipes/images/californiaroll/done_l.jpg' ),
(204, 10.99, 'Tuna Tower', 'Hawaiian Bigeye tuna tower with sesame wonton crisps is an elegant recipe created to impress. Bold flavors of delicious fish with the crunchy baked spiced crackers will leave you wanting more!', 'entree', 'https://www.goodtaste.tv/wp-content/uploads/2020/10/Neches_River_Wheelhouse_Tuna_Tower.png' ),
(105, 9.99, 'Miso Soup', 'Normal miso soup', 'Appetizer', 'https://i0.wp.com/www.crowdedkitchen.com/wp-content/uploads/2020/08/vegan-miso-soup.jpg' ),
(301, 10.99, 'Cheesecake', 'New York style cheesecake', 'desert', 'https://www.thespruceeats.com/thmb/YRKAj_euVwJoZRM9KX9CF8jKk3w=/3105x3105/smart/filters:no_upscale()/juniors-original-new-york-cheesecake-recipe-1135432-hero-01-663eea27a7344bc885a8a7a401190355.jpg')

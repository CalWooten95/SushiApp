import sqlite3

import click

from flask import current_app, g
from flask.cli import  with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        
    svr = 'server'
    svrpasscode = '1234'
    db.execute('INSERT INTO user (username,password,id,type) VALUES (?, ?, 5, 2)', (svr, svrpasscode,))
    db.commit()
    #db.execute('INSERT INTO items (iid, price, itemName, Description, type, link) VALUES (203, 10.99, 'California Sushi Roll', 'Standard California roll', 'entree', 'https://anyrecipe.net/asian/recipes/images/californiaroll/done_l.jpg' )')
    #,(204, 10.99, 'Tuna Tower', 'Hawaiian Bigeye tuna tower with sesame wonton crisps is an elegant recipe created to impress. Bold flavors of delicious fish with the crunchy baked spiced crackers will leave you wanting more!', 'entree', 'https://www.goodtaste.tv/wp-content/uploads/2020/10/Neches_River_Wheelhouse_Tuna_Tower.png' ),(105, 9.99, 'Miso Soup', 'Normal miso soup', 'Appetizer', 'https://i0.wp.com/www.crowdedkitchen.com/wp-content/uploads/2020/08/vegan-miso-soup.jpg' ),(301, 10.99, 'Cheesecake', 'New York style cheesecake', 'desert', 'https://www.thespruceeats.com/thmb/YRKAj_euVwJoZRM9KX9CF8jKk3w=/3105x3105/smart/filters:no_upscale()/juniors-original-new-york-cheesecake-recipe-1135432-hero-01-663eea27a7344bc885a8a7a401190355.jpg' )')


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
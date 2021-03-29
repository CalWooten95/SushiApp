from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('customer', __name__)

def get_item(id):
    item = get_db().execute(
        #"" SELECT i.id, i.price, i.itemName, i.description, i.type
            #FROM items i JOIN


    )


@bp.route('/')
def index():
    db = get_db()
    table = db.execute('SELECT * FROM items').fetchall()


    return render_template('customer/index.html', table=table)



@bp.route('/checkout/')
def checkout():
    return render_template('customer/checkout.html')

@bp.route('/<int:id>/addItem', methods=('GET','POST'))
@login_required
def addItem(id):

    return render_template('customer/checkout.html')

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('customer', __name__)


@bp.route('/')
def index():
    db = get_db()
    table = db.execute('SELECT * FROM items').fetchall()


    #Get orders
    #order = db.execute(
    # 'SELECT o.id, price, itemName, description'
    # ' FROM orders o JOIN user u ON o.custID = u.id'
    # ' ORDER BY created DESC'
    #).fetchall()

    return render_template('customer/index.html', table=table)

@bp.route('/checkout')
def checkout():
    return render_template('customer/checkout.html')
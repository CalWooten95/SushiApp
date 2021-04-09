from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('customer', __name__)


#Luhn credit card algorithm function taken from user K246
#https://stackoverflow.com/questions/39272087/validate-credit-card-number-using-luhn-algorithm-python
def luhn(ccn):
    c = [int(x) for x in ccn[::-2]]
    u2 = [(2*int(y))//10+(2*int(y))%10 for y in ccn[-2::-2]]
    return sum(c+u2)%10 == 0

@bp.route('/')
def index():
    db = get_db()
    table = db.execute('SELECT * FROM items').fetchall()


    return render_template('customer/index.html', table=table)



@bp.route('/checkout/')
@login_required
def checkout():
    db = get_db()

    user_id = session.get('user_id')
    table = db.execute(
                    'SELECT i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1', (user_id,)
                 ).fetchall()


    return render_template('customer/checkout.html', order=table)

@bp.route('/<int:id>/addItem/', methods=('GET','POST'))
@login_required
def addItem(id):
    db = get_db()
    user_id = session.get('user_id')
    db.execute('INSERT INTO orderedItems (iid, uid, active) VALUES (?, ?, 1)', (id, user_id))
    db.commit()
    flashItem = db.execute(
                    'SELECT itemName FROM items WHERE iid= ?', (id,)).fetchone()

    flashString = flashItem['itemName'] + " Added to Order"
    table = db.execute(
                    'SELECT i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1', (user_id,)
                 ).fetchall()

    flash(flashString)

    return render_template('customer/checkout.html', order=table)


@bp.route('/<int:id>/remove', methods=('GET','POST'))
@login_required
def remove(id):
    db = get_db()
    user_id = session.get('user_id')
    flashItem = db.execute(
                    'SELECT i.iid, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid  WHERE oi.iid= ? AND oi.uid= ? AND oi.active= 1', (id, user_id, )).fetchone()

    flashString = flashItem['itemName'] + " Removed from Order"
    removeItem = db.execute(
        'SELECT ROWID FROM orderedItems WHERE iid= ? AND uid= ? AND active= 1', (id, user_id, )).fetchone()

    db.execute('DELETE FROM orderedItems WHERE ROWID=?', (removeItem['ROWID'],))
    db.commit()
    table = db.execute(
                    'SELECT i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1', (user_id,)
                 ).fetchall()

    flash(flashString)
    return render_template('customer/checkout.html', order=table)


@bp.route('/complete/', methods=['GET','POST'])
@login_required
def complete():
    db = get_db()

    user_id = session.get('user_id')
    table = db.execute(
                    'SELECT i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1', (user_id,)
                 ).fetchall()
    total = 0
    for i in table:
        total += i['price']

    tax = round(total*0.0625, 2)
    total += tax



    return render_template('customer/complete.html', order=table, tax=tax, total=total)

#@bp.route('/pay/', methods=['GET,POST'])
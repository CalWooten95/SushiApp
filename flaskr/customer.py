import time
import random
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('customer', __name__)


def comp_order(i, ordered, new_ordered):
    for j in range(len(new_ordered)):
        print("errtest j = ", new_ordered[j]['uid'])
        if ordered[i]['uid'] == new_ordered[j]['uid'] and ordered[i]['timePlaced'] == new_ordered[j]['timePlaced']:
            return j

    return None

#Luhn credit card algorithm function taken from user K246
#https://stackoverflow.com/questions/39272087/validate-credit-card-number-using-luhn-algorithm-python
def luhn(ccn):
    c = [int(x) for x in ccn[::-2]]
    u2 = [(2*int(y))//10+(2*int(y))%10 for y in ccn[-2::-2]]
    return sum(c+u2)%10 == 0

@bp.route('/')
def index():
    user_id = session.get('user_id')
    db = get_db()

    ordered = db.execute(
        'SELECT *, items.itemName FROM orderedItems LEFT JOIN items ON orderedItems.iid = items.iid'
    ).fetchall()


    table = db.execute('SELECT * FROM items').fetchall()


    return render_template('customer/index.html', table=table, uid=user_id)


@bp.route('/checkout/', methods=('GET','POST'))
@login_required
def checkout():
    db = get_db()
    user_id = session.get('user_id')

    if request.method == 'POST':
        rowid = request.form['rowid']
        comments = [request.form['comments']]

        db.execute(
            'UPDATE orderedItems SET comments=? WHERE ROWID=?', (comments[0], int(rowid),)
        )
        db.commit()
    table = db.execute(
                    'SELECT oi.ROWID, oi.comments, i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1 AND oi.completed IS NULL', (user_id,)
                 ).fetchall()

    if len(table) == 0:
        hasItems = False
    else:
        hasItems = True

    total = 0
    for i in table:
        total += i['price']

    return render_template('customer/checkout.html', order=table, hasItems=hasItems, total=total)

#Request help
@bp.route('/<int:id>/help', methods=('GET', 'POST'))
def help(id):
    db = get_db()

    db.execute('INSERT INTO help (id, tablenumber) VALUES (?, ?)', (id, id,)) #tablenum and id wound up being the same thing
    db.commit()

    return redirect(url_for('customer.index'))

#Request drink refill
@bp.route('/<int:id>/refill', methods=('GET', 'POST'))
def refill(id):
    db = get_db()
    d = 'drinks'
    drinks = db.execute('SELECT * FROM items WHERE type=?', (d,)).fetchall()

    return render_template('customer/refills.html', uid=id, drinks=drinks)

@bp.route('/<int:id>/<int:iid>/refill', methods=('GET', 'POST'))
def do_refill(id, iid):
    db = get_db()
    db.execute('INSERT INTO refills (iid, tablenumber, seatnumber, beverage) VALUES (?, ?, 0, ?)', (iid, id, id)) #tablenum and id wound up being the same thing
    db.commit()
    return redirect(url_for('customer.index'))

@bp.route('/<int:id>/addItem/', methods=('GET','POST'))
@login_required
def addItem(id):
    db = get_db()

    if request.method == 'POST':
        rowid = request.form['rowid']
        comments = [request.form['comments']]

        db.execute(
            'UPDATE orderedItems SET comments=? WHERE ROWID=?', (comments[0], int(rowid),)
        )
        db.commit()
        return redirect(url_for('customer.checkout', code=307))
    db = get_db()
    user_id = session.get('user_id')


    db.execute('INSERT INTO orderedItems (iid, uid, active, completed, timePlaced) VALUES (?, ?, 1, NULL, 0)', (id, user_id,))
    db.commit()
    flashItem = db.execute(
                    'SELECT itemName FROM items WHERE iid= ?', (id,)).fetchone()

    flashString = flashItem['itemName'] + " Added to Order"
    table = db.execute(
                    'SELECT oi.ROWID, oi.comments, i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1 AND oi.completed IS NULL', (user_id,)
                 ).fetchall()



    flash(flashString)

    if len(table) == 0:
        hasItems = False
    else:
        hasItems = True

    total = 0
    for i in table:
        total += i['price']

    return render_template('customer/checkout.html', order=table, hasItems=hasItems, total=total)


@bp.route('/<int:id>/remove', methods=('GET','POST'))
@login_required
def remove(id):

    db = get_db()

    if request.method == 'POST':
        rowid = request.form['rowid']
        comments = [request.form['comments']]

        db.execute(
            'UPDATE orderedItems SET comments=? WHERE ROWID=?', (comments[0], int(rowid),)
        )
        db.commit()
        return redirect(url_for('customer.checkout', code=307))

    user_id = session.get('user_id')
    flashItem = db.execute(
                    'SELECT i.iid, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid  WHERE oi.iid= ? AND oi.uid= ? AND oi.active= 1 AND oi.completed IS NULL', (id, user_id, )).fetchone()

    flashString = flashItem['itemName'] + " Removed from Order"
    removeItem = db.execute(
        'SELECT ROWID FROM orderedItems WHERE iid= ? AND uid= ? AND active= 1', (id, user_id, )).fetchone()

    db.execute('DELETE FROM orderedItems WHERE ROWID=?', (removeItem['ROWID'],))
    db.commit()
    table = db.execute(
                    'SELECT oi.ROWID, oi.comments, i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1 AND oi.completed IS NULL', (user_id,)
                 ).fetchall()

    flash(flashString)
    if len(table) == 0:
        hasItems = False
    else:
        hasItems = True

    total = 0
    for i in table:
        total += i['price']

    return render_template('customer/checkout.html', order=table, hasItems=hasItems, total=total)


@bp.route('/complete/', methods=['GET','POST'])
@login_required
def complete():
    db = get_db()
    if request.method == 'POST':
        tip = request.form['tip']
        return redirect(url_for('customer.pay', tip=tip))
    user_id = session.get('user_id')
    table = db.execute(
                    'SELECT i.iid, i.price, i.itemName '
                    'From items i '
                    'JOIN orderedItems oi ON i.iid = oi.iid '
                    'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1 AND oi.completed IS NULL', (user_id,)
                 ).fetchall()
    subtotal = 0
    for i in table:
        subtotal += i['price']

    total = subtotal
    tax = round(total * 0.0625, 2)
    total += tax

    return render_template('customer/complete.html', order=table, tax=tax, total=total, subtotal=subtotal)

@bp.route('/pay/<float:tip>', methods=['GET','POST'])
@login_required
def pay(tip):
    if request.method == 'POST':
        if luhn(request.form['ccnum']):
            return redirect(url_for('customer.finish', tip=tip))
        else:
            flash("Card Error: Try Again")
    db = get_db()
    user_id = session.get('user_id')
    table = db.execute(
        'SELECT i.iid, i.price, i.itemName '
        'From items i '
        'JOIN orderedItems oi ON i.iid = oi.iid '
        'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1 AND oi.completed IS NULL', (user_id,)
    ).fetchall()

    subtotal = 0
    for i in table:
        subtotal += i['price']

    tax = round(subtotal * 0.0625, 2)
    total = subtotal
    total += tax
    total += tip

    return render_template('customer/pay.html', order=table, total=total, tax=tax, tip=tip, subtotal=subtotal)

@bp.route('/finish/<int:tip>')
@login_required
def finish(tip):
    db = get_db()
    user_id = session.get('user_id')
    flash("Card Accepted. Thank you for your order!")
    table = db.execute(
        'SELECT oi.ROWID, i.iid, i.price, i.itemName '
        'From items i '
        'JOIN orderedItems oi ON i.iid = oi.iid '
        'JOIN user u ON oi.uid = u.id WHERE u.id = ? AND oi.active = 1 AND oi.completed IS NULL', (user_id,)
    ).fetchall()
    total = 0
    for i in table:
        total += i['price']

    tax = round(total * 0.0625, 2)
    total += tax

    total_withtax = total #save for sales

    total += tip

    if time.localtime().tm_hour > 12:
        hour = time.localtime().tm_hour % 12
        ampm = "P.M."
    elif time.localtime().tm_hour < 12:
        ampm = "A.M."
        hour = time.localtime().tm_hour
    elif time.localtime().tm_hour == 12:
        ampm = "P.M."
        hour = time.localtime().tm_hour

    if time.localtime().tm_min < 10:
        min = str(time.localtime().tm_min).zfill(2)
    else:
        min = time.localtime().tm_min

    t =time.time()

    #save tips for manager sales
    db.execute('INSERT INTO sales (uid, timePlaced, total, tip, refunded) VALUES (?, ?, ?, ?, 0)', (user_id, t, total, tip,))
    db.commit()

    #active = 1, completed = 0 for kitchen
    for item in table:
        db.execute(
          'UPDATE orderedItems SET completed = 0, timePlaced=? WHERE uid=? AND ROWID=?', (t, user_id, item['ROWID'],))
        db.commit()

    freeDessert = random.randint(1,3)

    if freeDessert == 1:
        win = True
    else:
        win = False

    print(win)

    return render_template("customer/finish.html", total=total, tip=tip, order=table, hour=hour, min=min, ampm=ampm, win=win)





@bp.route('/entree/')
def entree():
    db = get_db()

    table = db.execute('SELECT * FROM items').fetchall()


    return render_template('customer/entree.html', table=table)


@bp.route('/drinks/')
def drinks():
    db = get_db()


    table = db.execute('SELECT * FROM items').fetchall()


    return render_template('customer/drinks.html', table=table)


@bp.route('/desserts/')
def desserts():
    db = get_db()


    table = db.execute('SELECT * FROM items').fetchall()


    return render_template('customer/desserts.html', table=table)

@bp.route('/games/')
def games():
    return render_template('customer/games.html')

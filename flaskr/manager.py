import time
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('manager', __name__)

#to upload image for update or additem
ALLOWED_EXTENSIONS = {'png', 'jpg'}

#---------------------------------------------------------------------------
#   manager(): Initializes manager.html
#---------------------------------------------------------------------------
@bp.route('/manager')
@login_required
def manager():
    print("Entered manager view")
    return render_template("manager/manager.html")

#---------------------------------------------------------------------------
#   menu(): Initializes menu.html
#---------------------------------------------------------------------------
@bp.route('/menu')
def menu():
    #display all items on menu
    db = get_db()
    table = db.execute('SELECT * FROM items').fetchall()

    print("Entered menu page")
    return render_template("manager/menu.html", items=table)

#----------------------------------------------------------------------------------
#   add_item(): Add a new item to the menu
#----------------------------------------------------------------------------------
@bp.route('/addmenu', methods=('GET','POST'))
def add_item():
    types = ['entree', 'appetizer', 'dessert', 'drinks']

    #generate new item id
    db = get_db()
    iids = db.execute('SELECT DISTINCT iid FROM items').fetchall()

    iid = 0 #start at 0, and if an item is already id 0, go up
    for id in iids:
        if iid == id['iid']:
            iid +=1

    if request.method == 'POST':
        itemName = request.form['itemName']
        price = request.form['price']
        desc = request.form['description']
        type = request.form['type']
        link = request.form['link']
        error = None

        #if form is empty
        if not itemName:
            error = 'Item must have a name.'
        if not price:
            error = 'Item must have a price'
        if not desc:
            desc = ''
        if not type:
            error = 'there is literally a dropdown menu how did you accomplish not setting a type'
        if not link:
            error = 'Item must have an image link'

        if error is None:
            db = get_db()
            db.execute('INSERT INTO items (iid, price, itemName, Description, type, link) VALUES (?, ?, ?, ?, ?, ?)', (iid, price, itemName, desc, type, link,))
            db.commit()
            return redirect(url_for('manager.menu'))

        flash(error)

    return render_template("manager/addmenu.html", types=types)

#----------------------------------------------------------------------------
#   remove(): remove item at iid
# ---------------------------------------------------------------------------
@bp.route('/remove/<int:iid>', methods=('POST',))
@login_required
def remove(iid):
    db = get_db()
    db.execute('DELETE FROM items WHERE iid = ?', (iid,))
    db.commit()
    return redirect(url_for('manager.menu'))

#----------------------------------------------------------------------------------
#   update(): Update an item at iid.
#----------------------------------------------------------------------------------
@bp.route('/update/<int:iid>', methods=('GET','POST'))
def update(iid):
    db = get_db()
    table = db.execute('SELECT * FROM items WHERE iid = ?', (iid,)).fetchall()
    types = ['entree', 'appetizer', 'dessert', 'drinks']

    if request.method == 'POST':
        price = request.form['price']
        desc = request.form['description']
        type = request.form['type']
        link = request.form['link']

        #if form is empty, leave it as the same thing
        if not price:
            price = table[0]['price']
        if not desc:
            desc = table[0]['description']
        if not type:
            type = table[0]['type']
        if not link:
            link = table[0]['link']

        #update the table
        db = get_db()
        db.execute(
            'UPDATE items SET price=?, description=?, type=?, link=? WHERE iid=?', (price, desc, type, link, iid,))
        db.commit()
        print("Successfully updated ", table[0]['itemName'])
        return redirect(url_for('manager.menu'))

    return render_template("manager/update.html", types=types, items=table)

#--------------------------------------------------------------------------------
#   refund(): Displays orders, their total, and their refund status in refund.html
#--------------------------------------------------------------------------------
@bp.route('/refund')
def refund():
    db = get_db()
    sales = db.execute('SELECT * FROM sales').fetchall()

    totals = []
    for sale in sales:
        total = sale['tip'] + sale['total']
        totals.append(total)

    print("Entered refund view")
    return render_template("manager/refund.html", sales=sales, totals=totals)


#---------------------------------------------------------------------------
#   do_refund: Marks sale as refunded.
#---------------------------------------------------------------------------
@bp.route('/<int:id>/do-refund/', methods=('GET','POST'))
@login_required
def do_refund(id):

    db = get_db()
    db.execute('UPDATE sales SET refunded=1 WHERE uid=?', (id,))
    db.commit()
    print("Order refunded for UID", id)
    return redirect("/refund")


@bp.route('/sales')
def sales():
    #---------------------------------------------------------------------------
    #   Display sales and tips.
    #---------------------------------------------------------------------------

    #<- Only grab orders that are for today (between unix timestamps for beginning and end of day) ->
    today = datetime.datetime.now()

    today_beginning = datetime.datetime(today.year, today.month, today.day, 0, 0, 0, 0)
    today_beginning_unix = int(time.mktime(today_beginning.timetuple()))

    today_end = datetime.datetime(today.year, today.month, today.day, 23, 59, 59, 999)
    today_end_unix = int(time.mktime(today_end.timetuple()))

    db = get_db()
    sales = db.execute('SELECT * FROM sales WHERE timePlaced >= ? AND timePlaced <= ?', (today_beginning_unix, today_end_unix,)).fetchall()

    #<-- Total everything to be displayed -->
    tip_total = 0
    orders_total = 0

    for s in sales:
        tip_total += s['tip']

    for s in sales:
        orders_total += s['total']

    total = tip_total + orders_total

    #<- get date and time (i stole this from cal) ->

    #date
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday

    #time
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

    time_now = {
        'month': month,
        'day': day,
        'hour': hour,
        'min': min
    }

    print("Entered sales view [Manager]")
    return render_template("manager/sales.html", sales=sales, date=time_now, total=total, ototal=orders_total, tips=tip_total, ampm=ampm)

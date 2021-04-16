from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
import time

items_to_delete = []
items_to_add = []
bp = Blueprint('server', __name__)


def get_order(id):
    otd = get_db().execute('SELECT * FROM orders WHERE id = ?', (id,)).fetchone()
    return otd

#---------------------------------------------
# server_main_page(): main page for server.
# Displays orders, refills, and help requests
#---------------------------------------------
@bp.route('/server')
def server_main_page():
    items_to_add.clear()
    items_to_delete.clear()
    orderitems = get_db().execute('SELECT * FROM orderedItems').fetchall()
    users = get_db().execute('SELECT * FROM user').fetchall()
    refilldb = get_db().execute('SELECT * FROM refills LEFT JOIN items ON refills.iid == items.iid').fetchall()
    helpdb = get_db().execute('SELECT * FROM help').fetchall()
    get_db().execute('DELETE FROM orders')
    get_db().commit()
    for u in users:
        db = get_db()
        orderlist = ""
        num = u['id']

        userQuery = db.execute(
            'SELECT DISTINCT uid FROM orderedItems WHERE active=1'
        ).fetchall()

        table = get_db().execute('SELECT *, items.itemName FROM orderedItems LEFT JOIN items ON orderedItems.iid== items.iid WHERE uid = ?', (num,) ).fetchall()

        orders = []
        is_completed = [] # marked 1 if all orders are marked completed

        for i in userQuery:
            table = db.execute('SELECT orderedItems.iid, comments, completed, items.itemName FROM orderedItems LEFT JOIN items ON orderedItems.iid = items.iid WHERE uid=?', (i['uid'],)).fetchall()
            tempnum = 0
            for t in table: #if all items in table are completed, the order is completed
                if t['completed'] == 1:
                    tempnum += 1

            if tempnum == len(table):
                is_completed.append(1)
            else:
                is_completed.append(0)
            orders.append(table)

    return render_template('server/server.html', users=userQuery, table2=refilldb, table3=helpdb, orders=orders, completed=is_completed)

#--------------------------------------------------------------
# additemview():returns information needed for servermenu.html,
# where the server can add items to the order
#--------------------------------------------------------------
@bp.route('/<int:id>/additemview')
def additemview(id):
    table = get_db().execute('SELECT * FROM items').fetchall()
    k = 0
    return render_template('server/servermenu.html',i=id,items=table, key=k)

#---------------------------------------------------------------------
# add_queue(): grabs list of items to add and sends it to edit_order()
#---------------------------------------------------------------------
@bp.route('/<int:id>/<int:iid>/add_queue')
def add_queue(id,iid):
    p = (id,iid)
    items_to_add.append(p)
    return edit_order(id)

#-------------------------------------------------------
# additemaction(): inserts the new order to the table
#------------------------------------------------------
@bp.route('/<int:id>/<int:iid>/<int:key>/additemaction')
def additemaction(id,iid,key):
    item = get_db().execute('SELECT * FROM items WHERE iid = ?', (iid,)).fetchone()
    i = item['iid']
    t0 = time.time()
    get_db().execute('INSERT INTO orderedItems (iid, uid, active, completed, timePlaced, comments) VALUES (?, ?, ?, ?, ?, ?)', (i, id, 1, 0, t0, None))
    get_db().commit()
    if key == 0:
        return edit_order(id)
    else:
        return add_order(id,iid)

#----------------------------------------------------
# edit_order(): fetches table data for editorder.html
#----------------------------------------------------
@bp.route('/<int:id>/editorder')
def edit_order(id):
    table = get_db().execute('SELECT * FROM orderedItems WHERE uid = ?', (id,)).fetchall()
    usr = get_db().execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()
    num = usr['id']
    return render_template('server/editorder.html', u=usr, id=id, oitems=table, n=num)

#---------------------------------------------
#   remove_queue(): retrieves information for editorder.
#   grabs list of items to delete.
#---------------------------------------------
@bp.route('/<int:id>/<int:iid>/<float:mark>/remove_queue')
def remove_queue(id,iid,mark):
    p = (id, iid, mark)
    items_to_delete.append(p)
    table = get_db().execute('SELECT * FROM orderedItems WHERE uid = ?', (id,)).fetchall()
    usr = get_db().execute('SELECT * FROM user WHERE id = ?', (id,)).fetchall()
    return render_template('server/editorder.html', u=usr, oitems=table)

#---------------------------------------------
# remove_item(): deletes order item from table
#---------------------------------------------
@bp.route('/<int:id>/<int:iid>/<float:completed>/removeitem')
def remove_item(id,iid,mark):
    get_db().execute('DELETE FROM orderedItems WHERE uid = ? AND iid = ? AND completed = ?', (id,iid,mark))
    get_db().commit()
    return add_order(id)

#---------------------------------------------
# remove_order_items(): deletes order items from table
#---------------------------------------------
@bp.route('/removeitems')
def remove_order_items():
    for p in items_to_delete:
        get_db().execute('DELETE FROM orderedItems WHERE uid = ? AND iid = ? AND mark = ?', (p[0],p[1],p[2]))
        get_db().commit()
    for e in items_to_add:
        t1 = time.time()
        p1 = get_db().execute('SELECT * FROM items WHERE iid = ?', (e[1],)).fetchone()
        p2 = p1['itemName']
        get_db().execute('INSERT INTO orderedItems (uid,iid,mark,nameofitem,active) VALUES (?, ?, ?, ?, 1)', (e[0],e[1], t1, p2))
        get_db().commit()
    items_to_delete.clear()
    items_to_add.clear()
    return redirect('/server')

#---------------------------------------------
# add_order(): Add new order
#---------------------------------------------
@bp.route('/<int:id>/addorder')
def add_order(id,iid=None):
    itemdb = get_db().execute('SELECT * FROM items').fetchall()
    table = get_db().execute('SELECT * FROM orderedItems WHERE uid = ?', (id,)).fetchall()
    total_price = 0.00
    for i in table:
        num = i['iid']
        p = get_db().execute('SELECT * FROM items WHERE iid = ?', (num,)).fetchone()
        total_price += p['price']

    tax = round(total_price*0.0625, 2)
    total_price += tax
    key1 = 1
    return render_template('server/servermenu.html', items=itemdb, key=key1, price=total_price, oitems=table)

#---------------------------------------------
# delete_order(): deletes order items from both orderedItems and orders
#---------------------------------------------
@bp.route('/<int:id>/deleteorder')
def delete_order(id):
    get_db().execute('DELETE FROM orderedItems WHERE uid = ?', (id,))
    get_db().commit()
    get_db().execute('DELETE FROM orders WHERE custID = ?', (id,))
    get_db().commit()
    items_to_add.clear()
    return redirect('/server')

#---------------------------------------------
# clear_request(): clears refill requests from page
#---------------------------------------------
@bp.route('/<int:iid>/requestfulfilled')
def clear_request(iid):
    get_db().execute('DELETE FROM refills WHERE iid = ?', (iid,))
    get_db().commit()
    return redirect('/server')

#---------------------------------------------
# remove_order_items(): clears help requests from page
#---------------------------------------------
@bp.route('/<int:id>/helpcomplete')
def help_complete(id):
    get_db().execute('DELETE FROM help WHERE id = ?', (id,))
    get_db().commit()
    return redirect('/server')

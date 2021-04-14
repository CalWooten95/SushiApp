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


@bp.route('/server')
def server_main_page():
    items_to_add.clear()
    items_to_delete.clear()
    orderitems = get_db().execute('SELECT * FROM orderedItems').fetchall()
    users = get_db().execute('SELECT * FROM user').fetchall()
    refilldb = get_db().execute('SELECT * FROM refills').fetchall()
    helpdb = get_db().execute('SELECT * FROM help').fetchall()
    get_db().execute('DELETE FROM orders')
    get_db().commit()
    for u in users:
        orderlist = ""
        num = u['id']
        table = get_db().execute('SELECT * FROM orderedItems WHERE uid = ?', (num,) ).fetchall()
        for t in table:
            orderlist = orderlist + t['nameofitem'] + ' '
        if orderlist != "":
            get_db().execute('INSERT INTO orders (custID, comments, total) VALUES (?,?,0)', (num,orderlist,))
            get_db().commit()
    orderdb = get_db().execute('SELECT * FROM orders').fetchall()
        
    return render_template('server/server.html', table2=refilldb, table3=helpdb, table4=orderdb)

@bp.route('/<int:id>/additemview')
def additemview(id):
    table = get_db().execute('SELECT * FROM items').fetchall()
    k = 0
    return render_template('server/servermenu.html',i=id,items=table, key=k)
    
@bp.route('/<int:id>/<int:iid>/add_queue')
def add_queue(id,iid):
    p = (id,iid)
    items_to_add.append(p)
    return edit_order(id)

@bp.route('/<int:id>/<int:iid>/<int:key>/additemaction')
def additemaction(id,iid,key):
    item = get_db().execute('SELECT * FROM items WHERE iid = ?', (iid,)).fetchone()
    u1 = get_db().execute('SELECT username FROM user WHERE id = ?', (id,)).fetchone()
    i = item['iid']
    t = item['itemName']
    u = u1['username']
    t0 = time.time()
    get_db().execute('INSERT INTO orderedItems (iid, uid, nameofitem, username, mark, active) VALUES (?, ?, ?, ?, ?, 1)', (i, id, t, u, t0))
    get_db().commit()
    if key == 0:
        return edit_order(id)
    else:
        return add_order(id,iid)

@bp.route('/<int:id>/editorder')
def edit_order(id):
    table = get_db().execute('SELECT * FROM orderedItems WHERE uid = ?', (id,)).fetchall()
    usr = get_db().execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()
    num = usr['id']
    return render_template('server/editorder.html', u=usr, oitems=table, n=num)
    
    
@bp.route('/<int:id>/<int:iid>/<float:mark>/remove_queue')
def remove_queue(id,iid,mark):
    p = (id, iid, mark)
    items_to_delete.append(p)
    table = get_db().execute('SELECT * FROM orderedItems WHERE uid = ?', (id,)).fetchall()
    usr = get_db().execute('SELECT * FROM user WHERE id = ?', (id,)).fetchall()
    return render_template('server/editorder.html', u=usr, oitems=table)
    

@bp.route('/<int:id>/<int:iid>/<float:mark>/removeitem')
def remove_item(id,iid,mark):
    get_db().execute('DELETE FROM orderedItems WHERE uid = ? AND iid = ? AND mark = ?', (id,iid,mark))
    get_db().commit()
    return add_order(id)


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


@bp.route('/<int:id>/deleteorder')
def delete_order(id):
    get_db().execute('DELETE FROM orderedItems WHERE uid = ?', (id,))
    get_db().commit()
    get_db().execute('DELETE FROM orders WHERE custID = ?', (id,))
    get_db().commit()
    items_to_add.clear()
    return redirect('/server')
    
@bp.route('/<int:iid>/requestfulfilled')
def clear_request(iid):
    get_db().execute('DELETE FROM refills WHERE iid = ?', (iid,))
    get_db().commit()
    return redirect('/server')


@bp.route('/<int:id>/helpcomplete')
def help_complete(id):
    get_db().execute('DELETE FROM help WHERE id = ?', (id,))
    get_db().commit()
    return redirect('/server')
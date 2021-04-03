from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('server', __name__)

def get_order(id):
    otd = get_db().execute('SELECT * FROM orders WHERE id = ?',(id,)).fetchone()
    return otd
    

@bp.route('/server')
def server_main_page():
    orderdb = get_db().execute('SELECT * FROM orders').fetchall()
    refilldb = get_db().execute('SELECT * FROM refills').fetchall()
    helpdb = get_db().execute('SELECT * FROM help').fetchall()
    return render_template('server/server.html', table=orderdb, table2=refilldb, table3=helpdb)

@bp.route('/addorder')
def add_order():
    itemdb = get_db().execute('SELECT * FROM items').fetchall()
    return render_template('customer/index.html',table=itemdb)
    

@bp.route('/<int:id>/deleteorder')
def delete_order(id):
    get_db().execute('DELETE FROM orders WHERE id = ?', (id,))
    get_db().commit()
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





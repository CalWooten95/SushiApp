from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('kitchen', __name__)


@bp.route('/kitchen')
@login_required
def kitchen():
    #---------------------------------------------------------------------------
    #   Read in UIDs with active orders.
    #   Then create a list, parallel to UID, that stores all associated order info.
    #---------------------------------------------------------------------------
    db = get_db()
    userQuery = db.execute(
        'SELECT DISTINCT uid FROM orderedItems WHERE active=1 AND completed=0'
    ).fetchall()

    orders = []

    for i in userQuery:

        table = db.execute('SELECT orderedItems.iid, comments, completed, items.itemName FROM orderedItems LEFT JOIN items ON orderedItems.iid = items.iid WHERE completed=0 AND uid=?', (i['uid'],)).fetchall()
        orders.append(table)

    # Send to kitchen.html
    print("THIS IS THE KITCHEN")
    return render_template("kitchen/kitchen.html", users=userQuery, orders=orders)


@bp.route('/<int:id>/complete', methods=('GET','POST'))
@login_required
def complete(id):
    #---------------------------------------------------------------------------
    #   Sets the items in an order to completed=1 when the button is
    #   pressed in kitchen.html, removing it from view.
    #---------------------------------------------------------------------------
    db = get_db()
    db.execute('UPDATE orderedItems SET completed=1 WHERE uid=?', [id])
    db.commit()
    return redirect("/kitchen")

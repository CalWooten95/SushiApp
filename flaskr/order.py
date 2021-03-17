from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('order', __name__)


@bp.route('/')
def index():
    db = get_db()
    #posts = db.execute(
    #  'SELECT o.id, price, itemName, description'
    #   ' FROM orders o JOIN user u ON o.custID = u.id'
    #    ' ORDER BY created DESC'
    #).fetchall()
    return render_template('order/index.html')#, posts=posts)
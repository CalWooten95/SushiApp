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


    print("THIS IS THE KITCHEN")
    return render_template("kitchen/kitchen.html")
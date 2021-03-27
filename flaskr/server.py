from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint('server', __name__)

@bp.route('/server')
def server_main_page():
   return render_template('server/serverBase.html')

import os

from flask import Flask

def create_app(test_config = None):
    #create configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
        TEMPLATES_AUTO_RELOAD = True
    )

    if test_config is None:
        #load instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass




    #register db
    from . import db
    db.init_app(app)

    #register auth
    from . import auth
    app.register_blueprint(auth.bp)

    #register order
    from . import customer
    app.register_blueprint(customer.bp)
    app.add_url_rule('/', endpoint='index')


    #register checkout
    app.add_url_rule('/', endpoint='checkout')
    app.add_url_rule('/', endpoint='addItem')
    app.add_url_rule('/', endpoint='remove')
    app.add_url_rule('/', endpoint='complete')
    app.add_url_rule('/', endpoint='pay')
    app.add_url_rule('/', endpoint='finish')
    app.add_url_rule('/', endpoint='entree')
    app.add_url_rule('/', endpoint='drinks')
    app.add_url_rule('/', endpoint='dessert')
    app.add_url_rule('/', endpoint='games')

    # register manager
    from . import manager
    app.register_blueprint(manager.bp)
    app.add_url_rule('/', endpoint="manager")
    
    # register server
    from . import server
    app.register_blueprint(server.bp)
    app.add_url_rule('/', endpoint='server')
    app.add_url_rule('/', endpoint='deleteorder')
    app.add_url_rule('/', endpoint='addorder')
    app.add_url_rule('/', endpoint='requestfulfilled')
    app.add_url_rule('/', endpoint='helpcomplete')

    # register kitchen
    from . import kitchen
    app.register_blueprint(kitchen.bp)
    app.add_url_rule('/', endpoint="kitchen")



    return app

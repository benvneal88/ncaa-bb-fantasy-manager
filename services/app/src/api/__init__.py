from flask import Flask
from api import model
#from .config import Default


def create_app(config=None):

    app = Flask(__name__)
    # if config is not None:
    #     app.config.from_pyfile(config)
    # else:
    #     app.config.from_object(Default)

    app.config['SQLALCHEMY_DATABASE_URI'] = model.get_engine().url
    model.db.init_app(app)


    from api.route_blueprint import route_blueprint
    app.register_blueprint(route_blueprint)

    return app

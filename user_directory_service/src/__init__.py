from typing import Dict
from flask.app import Flask

d: Dict = {}
d['data'] = {}

def create_app(coordinator=False) -> Flask:
    app = Flask(__name__)

    from .store import store
    app.register_blueprint(store, url_prefix='/store')
    if coordinator:
        from .coordinator import coordinator
        app.register_blueprint(coordinator, url_prefix='/coordinator')
    else:
        from .worker import worker
        app.register_blueprint(worker, url_prefix='/worker')

    return app

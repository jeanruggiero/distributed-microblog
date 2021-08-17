import os
import requests
import sys

from typing import Dict
from flask import Flask

d: Dict = {}
d['data'] = {}

def create_app(coordinator=False) -> Flask:
    app = Flask(__name__)

    if coordinator:
        from .coordinator import coordinator
        app.register_blueprint(coordinator, url_prefix='/coordinator')
    else:
        from .store import store
        from .worker import worker
        app.register_blueprint(store, url_prefix='/store')
        app.register_blueprint(worker, url_prefix='/worker')

        # Attempt to join the cluster by making a request to the coordinator
        c_host: str = os.environ['COORDINATOR']
        res: Dict = requests.post(f'http://{c_host}/coordinator/join').json()
        if not res.get('success', False):
            print('Failed to join UDS cluster!')
            sys.exit(1)

    return app

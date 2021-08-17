import json
import os
import requests
import threading
import flask

from typing import Dict
from flask import Blueprint, jsonify, request

from . import d

KEY_STRING: str = 'username'
VALUE_STRING: str = 'IP address'

store: Blueprint = Blueprint('store', __name__)
lock: threading.Lock = threading.Lock()

coordinator = os.environ['COORDINATOR']

@store.route('/all', methods=['GET'])
def getAll() -> flask.Response:
    with lock:
        return jsonify({
            'data': d['data'],
            'success': True,
            'msg': f'Retrieved all {VALUE_STRING}\'s'
            })

@store.route('', methods=['GET', 'PUT'])
def get() -> flask.Response:
    req: Dict = json.loads(request.data)
    key: str = req.get('key', '')
    if key == '':
        return jsonify({
            'success': False,
            'msg': f'Empty {KEY_STRING} on request'
            })

    if request.method == 'GET':
        # No need for two-phase commit
        with lock:
            return jsonify(d['data'].get(key, {}))
    elif request.method == 'PUT':
        value: str = json.loads(request.data).get('value', '')
        if value == '':
            return jsonify({
                'success': False,
                'msg': f'Empty {VALUE_STRING} on PUT request'
                })

        # Start two-phase commit
        transaction: Dict = {'key': key, 'value': value}
        res:Dict = requests.post(f'http://{coordinator}/coordinator/start', json=transaction).json()

        if res.get('success', False):
            return jsonify({
                'data': d['data'].get(key, {}),
                'success': True,
                'msg': f'Updated {KEY_STRING}:{key} with {VALUE_STRING}:{value}'
                })
        else:
            return jsonify({
                'data': '',
                'success': False,
                'msg': f'Failed to update {KEY_STRING}:{key}'
                })
    else:
        return jsonify({
            'success': False,
            'msg': 'Invalid action'
            })

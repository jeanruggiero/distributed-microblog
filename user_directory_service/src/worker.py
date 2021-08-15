import json
import threading
from typing import Any, Dict

import flask

from flask import Blueprint, jsonify, request

from . import d

worker: Blueprint = Blueprint('worker', __name__)
lock: threading.Lock = threading.Lock()

history: Dict = {}

@worker.route('/prepare', methods=['POST'])
def prepare() -> flask.Response:
    transaction: Dict = json.loads(request.data)
    tid: Any = transaction.get('tid')
    key: Any = transaction.get('key')
    value: Any = transaction.get('value')
    oldValue: Any = d.get('value', None)

    # record history log
    history[tid] = {'old': oldValue, 'new': value}

    # prepare transaction
    with lock:
        d['data'][key] = d['data'].get(key, {})
        d['data'][key]['value'] = value

    return jsonify({
        'success': True,
        'msg': f'Prepared transaction {tid}'})

@worker.route('/commit', methods=['POST'])
def commit() -> flask.Response:
    transaction: Dict = json.loads(request.data)
    tid: Any = transaction.get('tid')

    # No need to do any operations, transaction already completed; just delete history
    history.pop(tid, None)

    return jsonify({
        'success': True,
        'msg': f'Committed transaction {tid}'
        })

@worker.route('/rollback', methods=['POST'])
def rollback() -> flask.Response:
    transaction: Dict = json.loads(request.data)
    tid: Any = transaction.get('tid')
    key: Any = transaction.get('key')

    with lock:
        changelog: Dict = history.get(tid, {})
        currentValue: Any = d['data'][key]['value']
        # Revert change iif a newer change has not been made
        if currentValue == changelog['old']:
            d['data'][key]['value'] = changelog['old']

    return jsonify({
        'success': True,
        'msg': f'Rolled back transaction {tid}'
        })

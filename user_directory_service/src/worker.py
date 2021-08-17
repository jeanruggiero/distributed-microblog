import json
import threading
import flask

from typing import Any, Dict
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
    oldValue: Any = d.get('value', '')

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

    changelog:Dict = history.pop(tid, None)

    if changelog is not None:
        oldValue: str = changelog['old']
        newValue: str = changelog['new']

        with lock:
            # Check that no newer transaction(s) have been made or prepare
            #   request was made in the first place
            if d['data'][key].get('value', '') == newValue:
                # rollback change
                d['data'][key]['value'] = oldValue

    return jsonify({
        'success': True,
        'msg': f'Rolled back transaction {tid}'
        })

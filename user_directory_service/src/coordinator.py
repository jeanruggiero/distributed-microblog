import json
import os
import requests
import threading
import flask

from typing import Dict
from flask import Blueprint, jsonify, request

from .common import validate_trans

coordinator: Blueprint = Blueprint('coordinator', __name__)
lock: threading.Lock = threading.Lock()

tid: int = 0
nodes = os.environ['NODES']

@coordinator.route('/start', methods=['POST'])
def start() -> flask.Response:
    with lock:
        transaction: Dict = json.loads(request.data)
        if not validate_trans(transaction):
            return jsonify({
                'success': False,
                'msg': 'Invalid transaction'
                })

        # add transaction id to transaction object and increment global id
        transaction['id'] = tid
        tid += 1

        # Prepare Phase
        doCommit: bool = True
        for w in nodes: # TODO: iterate through worker nodes
            res = requests.post(f'{w}/tpc/prepare', json=transaction)
            # if any worker node is unable to prepare, rollback transaction
            if not res.json().get('success', False):
                doCommit = False
                break

        # Commit/Rollback Phase
        if doCommit:
            for w in nodes:
                requests.post(f'{w}/tpc/commit', json=transaction)

            return jsonify({
                'success': True,
                'msg': f'Commited transaction {transaction["id"]}'})
        else:
            for w in nodes:
                requests.post(f'{w}/tpc/rollback', json=transaction)

            return jsonify({
                'success': False,
                'msg': f'Rolled back transaction {transaction[""]}'})

import json
import threading
import flask

from typing import Dict, Set
from requests.exceptions import ConnectTimeout
from flask import Blueprint, jsonify, request

from .common import mb_post, validate_trans

coordinator: Blueprint = Blueprint('coordinator', __name__)
lock: threading.Lock = threading.Lock()

tid: int = 0
n_replica = 0
nodes: Set[str] = set()

@coordinator.route('/join', methods=['POST'])
def join() -> flask.Response:
    global n_replica, nodes

    replica_address:str = request.remote_addr
    n_replica += 1
    nodes.add(f'{replica_address}:8080')

    return jsonify({
        'success': True,
         'msg': f''           
        })

@coordinator.route('/start', methods=['POST'])
def start() -> flask.Response:
    global tid, nodes
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
        for w in nodes:
            # res:Dict = requests.post(f'http://{w}/worker/prepare',
            #         json=transaction).json()
            try:
                res:Dict = mb_post(f'http://{w}/worker/prepare', json=transaction)
            except ConnectTimeout:
                # worker node down or unresponsive
                doCommit = False
                break
            
            # if any worker node is unable to prepare, rollback transaction
            if not res.get('success', False):
                doCommit = False
                break

        # Commit/Rollback Phase
        if doCommit:
            for w in nodes:
                # requests.post(f'http://{w}/worker/commit', json=transaction)
                try:
                    mb_post(f'http://{w}/worker/commit', json=transaction)
                except ConnectTimeout:
                    pass

            return jsonify({
                'success': True,
                'msg': f'Commited transaction {transaction["id"]}'})
        else:
            for w in nodes:
                # requests.post(f'http://{w}/worker/rollback', json=transaction)
                try:
                    mb_post(f'http://{w}/worker/rollback', json=transaction)
                except ConnectTimeout:
                    pass

            return jsonify({
                'success': False,
                'msg': f'Rolled back transaction {transaction["id"]}'})

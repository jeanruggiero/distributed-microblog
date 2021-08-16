import json
import os
import requests
import threading
import flask

from typing import Dict
from requests.exceptions import ConnectTimeout
from flask import Blueprint, jsonify, request

from .common import mb_post, validate_trans

coordinator: Blueprint = Blueprint('coordinator', __name__)
lock: threading.Lock = threading.Lock()

tid: int = 0
nodes = os.environ['NODES'].split(',')

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

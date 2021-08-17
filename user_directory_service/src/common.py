import requests

from typing import Dict

def mb_post(*args, **kwargs) -> Dict:
    return requests.post(*args, **kwargs, timeout=(3.05, 10)).json()

def validate_trans(transaction: Dict) -> bool:
    return transaction.get('key', False) and transaction.get('value', False)

from typing import *
import json

class Transaction:
    def __init__(self, coinbase: List[Dict] = [], trans: List[Dict] = []):

        # [{"amt": 100, "account": "David"}]
        self.coinbase = coinbase
        # [{"from": "David", "to": "Lindsay", "amt": 20}, ...]
        self.trans = trans

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        arg_dict = json.loads(json_str)
        trans_obj = cls(**arg_dict)
        return trans_obj

    def add_transfer(self, from_act, to_act, amt):
        self.trans.append({"from": from_act, "to": to_act, "amt": amt})

    def add_coinbase(self, account, amt):
        self.coinbase.append({"account": account, "amt": amt})

    def __str__(self):
        return self.to_json()

    
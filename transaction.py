from typing import *
import json

class Transaction:
    def __init__(self, coinbase: List[Dict] = None, trans: List[Dict] = None):


        # [{"amt": 100, "account": "David"}]
        if coinbase is None:
            self.coinbase = []
        else:
            self.coinbase = coinbase

        # [{"from": "David", "to": "Lindsay", "amt": 20}, ...]
        if trans is None:
            self.trans = []
        else:
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

    def print(self):
        print("Coinbase:")
        for item in self.coinbase:
            print("    $" + str(item["amt"]) + " -> " + item["account"])
        print("Transactions:")
        for item in self.trans:
            print("    $" + str(item["amt"]) + " From: " + item["from"] + " -> " + item["to"])


    def __str__(self):
        return self.to_json()

    
from typing import *
import json
import uuid


class Transaction:
    def __init__(self, coinbase: Dict = None, transfer: Dict = None, id=None):

        # {"amt": 100, "account": "David"}
        self.coinbase = coinbase

        # {"from": "David", "to": "Lindsay", "amt": 20}
        self.transfer = transfer

        if id is None:
            self.id = str(uuid.uuid4())
        else:
            self.id = id


    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        arg_dict = json.loads(json_str)
        trans_obj = cls(**arg_dict)
        return trans_obj

    def add_transfer(self, from_act, to_act, amt):
        self.transfer = {"from": from_act, "to": to_act, "amt": amt}

    def add_coinbase(self, account, amt):
        self.coinbase = {"account": account, "amt": amt}

    def print(self):
        print("UUID: " + self.id)
        if self.coinbase is not None:
            print("Coinbase:")
            print("    $" + str(self.coinbase["amt"]) + " -> " + self.coinbase["account"])
        if self.transfer is not None:
            print("Transactions:")
            print("    $" + str(self.transfer["amt"]) + " From: " +
                  self.transfer["from"] + " -> " + self.transfer["to"])

    # def __str__(self):
    #     return self.to_json()

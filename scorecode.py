#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018 theloop Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import json
from os.path import dirname, join, abspath

from loopchain.tools.score_helper import ScoreHelper

dir_path = dirname(abspath(__file__))
sys.path.append(dir_path)

# Basic SCORE helper classes.
from scoretool import ScoreHelperDatabase, SCOREResponse


class SCOREBusinessLogic:
    """User own SCORE implementation.
    DO NOT CHANGE THIS MODULE NAME.
    Implement your module in this class.
    """

    # User can use several DB instances.
    __db = None
    __db_contract = None
    __db_person = None

    def __init__(self):
        # User can use several DB instances.
        self.__db = ScoreHelperDatabase("MY_OWN_DB", ScoreHelper())
        self.__db_contract = ScoreHelperDatabase("Contract", ScoreHelper())
        self.__db_person = ScoreHelperDatabase("Person", ScoreHelper())


    def invoke_contract(self, log_func, id, params: dict, block=None):
        contract_key = params["key"]
        contract_value = params["value"]
        contract = json.loads(params["value"])
        farmer_key = contract["farmer"]

        orginal_farmer_data = self.__db_person.get_in_invoke(farmer_key.encode())
        farmer = json.loads(orginal_farmer_data)

        if farmer["token"] < contract["reward"]:
            return SCOREResponse.exception("Not Enough Token.")

        farmer["token"] -= contract["reward"]
        farmer["binded_token"] += contract["reward"]

        farmer_value = json.dumps(farmer)

        farmer_response = self.put_to_db(self.__db_person,farmer_key, farmer_value)
        contract_response = self.put_to_db(self.__db_contract,contract_key,contract_value)

        if farmer_response["code"] == 0 and contract_response["code"] == 0:
            return SCOREResponse.succeed()
        else:
            return SCOREResponse.exception("exception while writing db")

    def invoke_done(self, log_func, id, params: dict, block=None):
        contract_key = params["key"]
        done_contract = json.loads(params["value"])

        contract = json.loads(self.__db_contract.get_in_invoke(contract_key.encode()))
        contract["fulfillment"] = done_contract

        farmer_key = contract["farmer"]
        farmer = json.loads(self.__db_person.get_in_invoke(farmer_key.encode()))

        farmer["binded_token"] -= contract["reward"]

        farmer_value = json.dumps(farmer)

        citizen_key = contract["citizen"]
        citizen = json.loads(self.__db_person.get_in_invoke(citizen_key.encode()))

        citizen["token"] += contract["reward"]

        citizen_value = json.dumps(citizen)
        contract_value = json.dumps(contract)

        farmer_response = self.put_to_db(self.__db_person, farmer_key, farmer_value)
        citizen_response = self.put_to_db(self.__db_person, citizen_key, citizen_value)
        contract_response = self.put_to_db(self.__db_contract, contract_key, contract_value)

        if farmer_response["code"] == 0 and citizen_response["code"] == 0 and contract_response["code"] == 0:
            return SCOREResponse.succeed()
        else:
            return SCOREResponse.exception("exception while writing db")

    def invoke_cancel(self, log_func, id, params: dict, block=None):
        contract_key = params["key"]
        canceled_contract = params["value"]

        contract = json.loads(self.__db_contract.get_in_invoke(contract_key.encode()))
        contract["fulfillment"] = canceled_contract

        contract_value = json.dumps(contract)

        farmer_key = contract["farmer"]
        farmer = json.loads(self.__db_person.get_in_invoke(farmer_key.encode()))

        farmer["binded_token"] -= contract["reward"]
        farmer["token"] += contract["reward"]

        farmer_value = json.dumps(farmer)

        farmer_response = self.put_to_db(self.__db_person, farmer_key, farmer_value)
        contract_response = self.put_to_db(self.__db_contract, contract_key, contract_value)

        if farmer_response["code"] == 0 and contract_response["code"] == 0:
            return SCOREResponse.succeed()
        else:
            return SCOREResponse.exception("exception while writing db")

    def invoke_person(self, log_func, id, params: dict, block=None):
        key = params["key"]

        person = {}
        person["token"] = 0
        person["binded_token"] = 0
        person["rating"] = 0
        person["rating_count"] = 0

        value = json.dumps(person)

        return self.put_to_db(self.__db_person, key, value)


    def invoke_rating(self, log_func, id, params: dict, block=None):
        key = params["key"]
        rating = params["rating"]

        person = json.loads(self.__db_person.get_in_invoke(key.encode()))
        person["rating"] += rating
        person["rating_count"] += 1

        value = json.dumps(person)

        return self.put_to_db(self.__db_person, key, value)

    def invoke_purchase_token(self, log_func, id, params: dict, block=None):
        key = params["key"]
        purchasing_amount = int(params["purchasing_amount"])

        person = json.loads(self.__db_person.get_in_invoke(key.encode()))
        person["token"] += purchasing_amount

        value = json.dumps(person)

        return self.put_to_db(self.__db_person, key, value)

    def invoke_spend_token(self, log_func, id, params: dict, block=None):
        key = params["key"]
        spending_amount = int(params["spending_amount"])

        person = json.loads(self.__db_person.get_in_invoke(key.encode()))
        person["token"] -= spending_amount

        value = json.dumps(person)

        return self.put_to_db(self.__db_person, key, value)

    def put_to_db(self, db, key, value):
        try:
            # Store string as value. And key and value must be BYTE type, not only string or object.
            db.put(key.encode(), value.encode())
        except TypeError:
            return SCOREResponse.exception("key or value is not byte-like data.")

        # Validate key and value.
        try:
            value_from_db = db.get_in_invoke(key.encode())
            if value != value_from_db.decode():
                return SCOREResponse.exception("Internal DB error.")

        # Handle exceptions.
        except TypeError:
            return SCOREResponse.exception("Key or value is not byte-like data.")

        except KeyError:
            return SCOREResponse.exception("DB do not Have such a key.")

        # Succeed to operate. Return successful message.
        #log_func("Succeed to execute invoke_foo1.")
        return SCOREResponse.succeed()



    def query_contract(self, log_func, id, params):
        key = params["key"]

        try:
            data = self.__db__contract.get_in_query(key.encode())

            result = {"data": data.decode("utf-8")}
            log_func('Queried data: {result}')
            return SCOREResponse.succeed("Succeed to query.", result)

        except TypeError:
            return SCOREResponse.exception("Key or value is not byte-like data.")

        except KeyError:
            return SCOREResponse.exception("DB do not Have such a key.")

    def query_person(self, log_func, id, params):
        key = params["key"]

        try:
            data = self.__db__person.get_in_query(key.encode())

            result = {"data": data.decode("utf-8")}
            log_func('Queried data: {result}')
            return SCOREResponse.succeed("Succeed to query.", result)

        except TypeError:
            return SCOREResponse.exception("Key or value is not byte-like data.")

        except KeyError:
            return SCOREResponse.exception("DB do not Have such a key.")
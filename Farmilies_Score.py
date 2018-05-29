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
from functools import partial
from os.path import dirname, join, abspath

from loopchain.blockchain import ScoreBase
from loopchain.tools.score_helper import ScoreHelper


dir_path = dirname(abspath(__file__))
sys.path.append(dir_path)

# SCORE Business logic class. TODO: YOU HAVE TO MODIFY THIS CLASS.
from scorecode import SCOREBusinessLogic
from scoretool import SCOREResponse

class UserScore(ScoreBase):
    """ Basic module of SCORE.
    DO NOT CHANGE THE NAME OF THIS MODULE.
    """
    __score_info = None
    __db_name = ""
    __score_helper = None
    __channel_name = ""
    __my_business_logic = None
    __invoke_function_map = {}
    __query_function_map = {}

    def __init__(self, score_info=None):

        # TODO:Change 'YOUR_SCORE_DB' your own DB name.
        self.__db_name = "YOUR_SCORE_DB"

        # Call base class's __init__.
        ScoreBase.__init__(self, score_info)

        # DO NOT CHANGE THIS BLOCK.
        # ====================================
        # Load package.json file for info() function.
        self.__score_info = None
        if self.__score_info is None:
            with open(join(dirname(__file__), ScoreBase.PACKAGE_FILE), "r") as f:
                self.__score_info = json.loads(f.read())
                f.close()
        else:
            self.__score_info = score_info

        # Initialize ScoreBase module.
        self.__score_helper = ScoreHelper()

        # Initialize SCOREBusinessLogic module.
        self.__my_business_logic = SCOREBusinessLogic()

        # Map functions in package.json.
        for e in self.__score_info["function"]["invoke"]:
            function_name = e["method"]
            self.__invoke_function_map[function_name] = getattr(self.__my_business_logic, function_name)

        for e in self.__score_info["function"]["query"]:
            function_name = e["method"]
            self.__query_function_map[function_name] = getattr(self.__my_business_logic, function_name)

        # DO NOT CHANGE THIS BLOCK.
        # ====================================

    def invoke(self, transaction, block=None):
        """ Handler of 'Invoke' requests.

        Event handler of invoke request. You need to implement this handler like below.
        0. Define the interface of functions in 'invoke' field of package.json.
        1. Parse transaction data and get the name of function by reading 'method' field of transaction.
        2. Call that function.

        How to test:
        1. Launch loopchain with SCORE.
        2. Call '/api/v1/transactions' with following JSON request to call function belonging to invoke requests.
        {
            "jsonrpc":"2.0",
            "id": ~~, <== Must be number.
            "method":"method name",
            "params": {
            }
        }
        Then you can get the following response.

        {
            "response_code": "0", <== 'Success' is 0.  'Exception' is 9000.
            "tx_hash": "~~~",
            "more_info": ""
        }

        3. Call '/api/v1/transactions/result?{tx_hash}' to get the result. Response is like following.

        {
            "response_code": "0", <== 'Success' is 0.  'Exception' is 9000.
            "response": {
                "code": 0,
                "jsonrpc": "2.0"
            }
        }



        :param transaction: transaction data.
        :param block: block data has transaction data.
        :return: response : Invoke result as following. Recommend to use SCOREResponse class.
        """
        if block is None:
            return SCOREResponse.exception("No block!!!")

        # Simplify log function with channel name.
        log_func = partial(self.__score_helper.log, block.channel_name)
        self.__channel_name = block.channel_name

        # Begin to call invoke function.
        log_func("Invoke() begin.")
        try:
            tx_data = json.loads(transaction.get_data_string())
            id = tx_data["id"]
            function_name = tx_data["method"]
            params = tx_data["params"]

            # Run the mapped invoke function in function map.
            r = self.__invoke_function_map[function_name](log_func, id, params)

            # End to call invoke function.
            log_func("End Invoke()")

            return r
        except:
            log_func("Unknown function call requested!! Cannot run invoke(). ")
            raise

    def query(self, query_request):
        """ Handler of 'Query' requests.
           It's event handler of query request. You need to implement this handler like below.
           0. Define the interface of functions in 'query' field of package.json.
           1. Parse transaction data and get the name of function by reading 'method' field of transaction.
           2. Call that function.

            How to test:
            1. Launch loopchain with SCORE.
            2. Call '/api/v1/query' with following JSON request to call function belonging to invoke requests.
            {
                "jsonrpc":"2.0",
                "id": ~~, <== Must be string in Query.
                "method":"method name",
                "params": {
                }
            }

            Then you can get the following response.
            {
                "response_code": "0",
                "response": {
                    "code": 0,  <== 'Success' is 0.  'Exception' is 9000.
                    "message": "Succeed to query.",
                    "result": {
                        "data": ""
                    }
                }
            }


           :param block: block data has transaction data.
           :return: response : Query result as following. Recommend to use SCOREResponse class.
           {
                 'code' : integer value.
                   * 'Success' is 0.
                   * 'Exception' is 9000.
                 'result' : result of query.
            }

        """

        # Simplify log function with channel name.
        log_func = partial(self.__score_helper.log, self.__channel_name)

        # Begin to call invoke function.
        log_func("Query() begin.")
        try:
            req = json.loads(query_request)
            function_name = req["method"]
            id = req['id']
            params = req['params']

            # Run the mapped query function in function map.
            r = self.__query_function_map[function_name](log_func, id, params)

            # End to call invoke function.
            log_func("End Query()")

            # Encode python object as string.
            return json.dumps(r)
        except:
            log_func("Unknown error happen!! Cannot run query().")
            raise

        # Encode python object as string.
        return json.dumps(r)


    def info(self):
        return self.__score_info

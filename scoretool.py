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
from enum import Enum

JSON_RPC_VERSION = "2.0"


class SCOREResponse:
    """ Just response utility for SCORE.
    """
    def __init__(self):
        pass

    @classmethod
    def __msg(cls, code:int, message:str="", result:object=None)-> object:
        """ Message data structure generation function.
        :param code: error code
        :param message: message string
        :return: dictionary with code and message.
        """
        data = {'code': code}
        if message != "":
            data["message"] = message

        if result is not None:
            data["result"] = result

        return data

    @classmethod
    def succeed(cls, message:str= "", result:object=None)-> object:
        """Return the successful message object.

        :param message: message string
        :return: dictionary with code and message.
        """
        return cls.__msg(0, message, result)


    @classmethod
    def exception(cls, message:str="") -> object:
        """Return the message, exception raised, object.

        :param message: message string
        :return: dictionary with code and message.
        """
        return cls.__msg(9000, message)


class ScoreHelperDatabase(object):
    """ Utility class for SCORE DB operation.
    """

    def __init__(self, db_name, score_helper):
        """DB 생성자

        Args:
            score_helper(object): loopchain에서 제공하는 db 관리 객체
        """
        self.__db_name = db_name
        self.__db = score_helper

    def get_in_invoke(self, key: bytes)-> object:
        """Get data from DB.
        loopchain invoke에서만 사용해야 한다.

        Args:
            key(bytes): db key

        Return:
            bytes: key가 가리키는 데이터. otherwise None
        """
        try:
            return self.__db.Get(self.__db_name, key)
        except Exception as e:
            return None

    def get_in_query(self, key: bytes) -> object:
        """"Get data from DB in query().

        :param key:
        :return: bytes: key가 가리키는 데이터. otherwise None
        """
        try:
            return self.__db.Query(self.__db_name, key)
        except Exception as e:
            return None



    def put(self, key: bytes, value: bytes):
        """db에 데이터를 저장한다.

        Args:
            key(bytes): db key
            value(bytes): db에 저장할 데이터
        """
        self.__db.Put(self.__db_name, key, value)

    def delete(self, key: bytes):
        """db에서 데이터를 삭제한다.

        Args:
            key(bytes): db에서 key가 가리키는 데이터 삭제
        """
        self.__db.Delete(self.__db_name, key)

    def close(self):
        """db를 닫는다.
        score_helper에서는 제공하지 않는 메소드
        """
        pass

#!/usr/bin/python3
# coding=utf-8
# pylint: disable=C0116,W0201

#   Copyright 2025 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Method """

from pylon.core.tools import web, log  # pylint: disable=E0401,E0611,W0611

from tools import auth_core  # pylint: disable=E0401


class Method:  # pylint: disable=E1101,R0903
    """
        Method Resource

        self is pointing to current Module instance

        web.method decorator takes zero or one argument: method name
        Note: web.method decorator must be the last decorator (at top)

    """

    @web.method()
    def have_requirement(self, auth_type, auth_id, req_scope, req_permissions):
        try:
            auth_id = int(auth_id)
        except:  # pylint: disable=W0702
            auth_id = "-"
        #
        if auth_type == "user":
            auth_permissions = auth_core.get_user_permissions(auth_id, req_scope)
        elif auth_type == "token":
            auth_permissions = auth_core.get_token_permissions(auth_id, req_scope)
        else:
            auth_permissions = []
        #
        req_permissions = set(req_permissions)
        auth_permissions = set(auth_permissions)
        #
        return req_permissions.issubset(auth_permissions)

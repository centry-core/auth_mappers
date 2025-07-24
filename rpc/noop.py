#!/usr/bin/python3
# coding=utf-8
# pylint: disable=C0115,C0116

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

""" RPC """

import json

from pylon.core.tools import web, log  # pylint: disable=E0401,E0611,W0611

from plugins.auth_core.tools import rpc_tools  # pylint: disable=E0401


class RPC:  # pylint: disable=R0903

    @web.rpc("auth_noop_info_mapper")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def noop_info_mapper(self, auth_ctx, scope):  # pylint: disable=W0613
        mimetype = "application/json"
        data = json.dumps(auth_ctx, default=str)
        #
        return mimetype, data

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

import flask  # pylint: disable=E0401
import jsonpath_rw  # pylint: disable=E0401

from pylon.core.tools import web, log  # pylint: disable=E0401,E0611,W0611

from plugins.auth_core.tools import rpc_tools  # pylint: disable=E0401

from tools import auth_core  # pylint: disable=E0401


class RPC:  # pylint: disable=R0903,E1101

    @web.rpc("auth_json_success_mapper")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def json_success_mapper(self, source, auth_type, auth_id, auth_reference):  # pylint: disable=W0613
        mapper_config = self.descriptor.config.get("json", {})
        endpoint = mapper_config.get("endpoint", None)
        #
        if endpoint is None:
            with self.context.app.app_context():
                endpoint = flask.url_for(
                    "auth_core.info",
                    target=source["target"],
                    scope=source["scope"],
                )
        #
        headers = {}
        #
        headers["X-Auth-Session-Endpoint"] = endpoint
        headers["X-Auth-Session-Name"] = auth_core.get_session_cookie_name()
        headers["X-Auth-Session-Id"] = auth_reference
        #
        return True, headers

    @web.rpc("auth_json_info_mapper")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def json_info_mapper(self, auth_ctx, scope):
        mapper_config = self.descriptor.config.get("json", {})
        scopes_config = mapper_config.get("scopes", {})
        scope_config = scopes_config.get(scope, {})
        #
        #
        result = {"raw": auth_ctx}
        for key, path in scope_config.items():
            try:
                result[key] = jsonpath_rw.parse(path).find(auth_ctx)[0].value
            except:  # pylint: disable=W0702
                log.exception("Failed to set scope data: %s -> %s", key, path)
        #
        mimetype = "application/json"
        data = json.dumps(result, default=str)
        #
        return mimetype, data

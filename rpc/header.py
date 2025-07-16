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

import jsonpath_rw  # pylint: disable=E0401

from pylon.core.tools import web, log  # pylint: disable=E0401,E0611,W0611

from plugins.auth_core.tools import rpc_tools  # pylint: disable=E0401

from tools import auth_core  # pylint: disable=E0401


class RPC:  # pylint: disable=R0903,E1101

    @web.rpc("auth_header_success_mapper")
    @rpc_tools.wrap_exceptions(RuntimeError)
    def header_success_mapper(self, source, auth_type, auth_id, auth_reference):
        auth_ctx = auth_core.get_referenced_auth_context(auth_reference)
        #
        mapper_config = self.descriptor.config.get("header", {})
        scopes_config = mapper_config.get("scopes", {})
        scope_config = scopes_config.get(source["scope"], {})
        scope_require = scope_config.get("require", [])
        #
        headers = {}
        #
        for requirement in scope_require:
            if not self.have_requirement(
                auth_type, auth_id,
                requirement.get("scope", 1),
                requirement.get("permissions", []),
            ):
                return False, headers
        #
        for key, path in scope_config.get("headers", {}).items():
            try:
                headers[key] = jsonpath_rw.parse(path).find(auth_ctx)[0].value
            except:  # pylint: disable=W0702
                log.exception("Failed to set scope data: %s -> %s", key, path)
        #
        return True, headers

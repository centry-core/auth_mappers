#!/usr/bin/python3
# coding=utf-8

#   Copyright 2022 getcarrier.io
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

""" Module """

from pylon.core.tools import log  # pylint: disable=E0401,E0611
from pylon.core.tools import module  # pylint: disable=E0401,E0611

from tools import auth_core  # pylint: disable=E0401


class Module(module.ModuleModel):
    """ Pylon module """

    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor

    #
    # Module
    #

    def init(self):
        """ Init module """
        log.info("Initializing module")
        # Init
        self.descriptor.init_all()
        # Register test info mapper
        auth_core.register_info_mapper(None, "auth_noop_info_mapper")
        # Register JSON mappers
        auth_core.register_success_mapper("json", "auth_json_success_mapper")
        auth_core.register_info_mapper("json", "auth_json_info_mapper")
        # Register header mapper
        auth_core.register_success_mapper("header", "auth_header_success_mapper")

    def deinit(self):
        """ De-init module """
        log.info("De-initializing module")
        # Unregister header mapper
        auth_core.unregister_success_mapper("header")
        # Unregister JSON mappers
        auth_core.unregister_info_mapper("json")
        auth_core.unregister_success_mapper("json")
        # Unregister test info mapper
        auth_core.unregister_info_mapper(None)
        # De-init
        self.descriptor.deinit_all()

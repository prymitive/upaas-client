# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from plumbum import cli

from upaas.cli.base import UPaaSApplication

from upaas_client import __version__ as UPAAS_VERSION
from upaas_client.return_codes import ExitCodes


class ClientApplication(UPaaSApplication):

    VERSION = UPAAS_VERSION

    @cli.switch(["c", "config"], str, help="Configuration file path",
                mandatory=True)
    def set_config_path(self, path):
        self.config_path = path

    def main(self, *args):
        self.setup_logger()

        if args:
            self.log.error("Unknown command '%s'" % args)
            return ExitCodes.command_error

        if not self.nested_command:
            self.log.error("No command given")
            return ExitCodes.command_error

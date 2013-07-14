# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from os.path import expanduser

from upaas.cli.base import UPaaSApplication
from upaas.config.base import load_config

from upaas_client.main import ClientApplication
from upaas_client import __version__ as UPAAS_VERSION
from upaas_client.return_codes import ExitCodes
from upaas_client.config import ClientConfig


@ClientApplication.subcommand('app')
class AppApplication(UPaaSApplication):

    VERSION = UPAAS_VERSION
    DESCRIPTION = "Application related commands"

    def main(self, *args):
        self.setup_logger()

        self.config = load_config(ClientConfig, ".upaas.yml",
                                  directories=[".", expanduser("~")])
        if not self.config:
            self.log.error("Missing config file")
            return ExitCodes.missing_config

        if args:
            self.log.error("Unknown command '%s'" % ' '.join(args))
            return ExitCodes.command_error

        if not self.nested_command:
            self.log.error("No command given")
            return ExitCodes.command_error

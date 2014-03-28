# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013-2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from os.path import expanduser, basename, dirname, exists

from upaas.cli.base import UPaaSApplication
from upaas.config.base import load_config

from plumbum import cli

from upaas_client import __version__ as UPAAS_VERSION
from upaas_client.return_codes import ExitCodes
from upaas_client.config import ClientConfig


class ClientApplication(UPaaSApplication):

    VERSION = UPAAS_VERSION

    config = None
    config_path = None

    @cli.switch(["c", "config"], str, help="Config file to use")
    def set_config_path(self, config_path):
        self.config_path = config_path

    def main(self, *args):
        self.setup_logger()

        if self.config_path:
            if exists(self.config_path):
                config_name = basename(self.config_path)
                config_dir = dirname(self.config_path)
                self.config = load_config(ClientConfig, config_name,
                                          directories=[config_dir])
            else:
                self.log.error("Config not found: %s" % self.config_path)
        else:
            self.config = load_config(ClientConfig, ".upaas.yml",
                                      directories=[".", expanduser("~")])
        if not self.config:
            self.log.error("Missing config file")
            return ExitCodes.missing_config

        if args:
            self.log.error("Unknown command '%s'" % ' '.join(args))
            return ExitCodes.command_error

        if not self.nested_command:
            self.help()
            return ExitCodes.command_error

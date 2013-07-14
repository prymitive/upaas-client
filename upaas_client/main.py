# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from upaas.cli.base import UPaaSApplication

from upaas_client import __version__ as UPAAS_VERSION
from upaas_client.return_codes import ExitCodes


class ClientApplication(UPaaSApplication):

    VERSION = UPAAS_VERSION

    def main(self, *args):
        self.setup_logger()

        if args:
            self.log.error("Unknown command '%s'" % ' '.join(args))
            return ExitCodes.command_error

        if not self.nested_command:
            self.log.error("No command given")
            return ExitCodes.command_error

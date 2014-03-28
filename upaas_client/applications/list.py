# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013-2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from upaas.cli.base import UPaaSApplication

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('list')
class List(UPaaSApplication):

    DESCRIPTION = "List registered applications"

    def main(self):
        self.setup_logger()
        self.log.info("Getting list of registered applications")

        self.api_connect(self.parent.config.server.login,
                         self.parent.config.server.apikey,
                         self.parent.config.server.url)

        try:
            resp = self.api.application.get()
            self.print_msg("%d application(s) "
                           "registered:" % resp['meta']['total_count'])
            for app in resp['objects']:
                self.print_msg(app['name'], prefix='*')
        except Exception as e:
            self.handle_error(e)
            return ExitCodes.command_error

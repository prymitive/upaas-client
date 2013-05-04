# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from plumbum import cli

from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('show')
class Show(UPaaSApplication):

    DESCRIPTION = "Show application details"

    @cli.switch(["n", "name"], str, help="Application name", mandatory=True)
    def set_name(self, name):
        self.name = name

    def main(self):
        self.setup_logger()
        self.log.info("Getting app '%s' details" % self.name)

        self.api_connect(self.parent.config.server.login,
                         self.parent.config.server.apikey,
                         self.parent.config.server.url)

        try:
            resp = self.api.application.get(name=self.name)
        except SlumberHttpBaseException, e:
            self.handle_error(e)
        else:
            if not resp.get('objects'):
                self.log.error("No such application registered: %s" % self.name)
                return ExitCodes.notfound_error

            app = resp['objects'][0]
            self.print_msg("Name: %s" % app['name'])
            self.print_msg("Created: %s" % app['date_created'])

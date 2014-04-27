# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013-2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('show')
class Show(UPaaSApplication):

    DESCRIPTION = "Show application details"

    def main(self, name):
        self.setup_logger()
        self.log.info("Getting app '%s' details" % name)

        self.api_connect(self.parent.config.server.login,
                         self.parent.config.server.apikey,
                         self.parent.config.server.url)

        try:
            resp = self.api.application.get(name=name)
        except SlumberHttpBaseException as e:
            self.handle_error(e)
        else:
            if not resp.get('objects'):
                self.log.error("No such application registered: %s" % name)
                return ExitCodes.notfound_error

            app = resp['objects'][0]
            self.print_msg("Name: %s" % app['name'])
            self.print_msg("Created: %s" % app['date_created'])
            self.print_msg("Packages: %d" % len(app['packages']))
            self.print_msg("Metadata:")
            for line in app['metadata'].splitlines():
                self.print_msg("| %s" % line)

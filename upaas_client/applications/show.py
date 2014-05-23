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
            self.print_msg("Running instances: %s" % app['instance_count'])
            self.print_msg("Running tasks: %s" % len(app['running_tasks']))
            pkg = app.get('current_package')
            if pkg:
                self.print_msg("Current package:")
                self.print_msg("Created: %s" % pkg['date_created'],
                               prefix='*')
                self.print_msg(
                    "Interpreter name: %s" % pkg['interpreter_name'],
                    prefix='*')
                self.print_msg(
                    "Interpreter version: %s" % pkg['interpreter_version'],
                    prefix='*')
                self.print_msg("Revision ID: %s" % pkg['revision_id'],
                               prefix='*')
                self.print_msg("Revision date: %s" % pkg['revision_date'],
                               prefix='*')
                self.print_msg("Revision author: %s" % pkg['revision_author'],
                               prefix='*')
                self.print_msg("Revision description:", prefix='*')
                for line in pkg['revision_description'].splitlines():
                    self.print_msg(line, prefix='')

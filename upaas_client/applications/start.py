# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('start')
class Start(UPaaSApplication):

    DESCRIPTION = "Start application"

    def main(self, name, worker_limit, memory_limit):
        self.setup_logger()
        self.log.info("Getting app '%s' details" % name)

        self.api_connect(self.parent.config.server.login,
                         self.parent.config.server.apikey,
                         self.parent.config.server.url)

        try:
            resp = self.api.application.get(name=name)
        except SlumberHttpBaseException, e:
            self.handle_error(e)
        else:
            if not resp.get('objects'):
                self.log.error("No such application registered: %s" % name)
                return ExitCodes.notfound_error

            app = resp['objects'][0]

            try:
                self.api.run_plan.post({
                    'application': app['id'], 'worker_limit': worker_limit,
                    'memory_limit': memory_limit})
            except SlumberHttpBaseException, e:
                self.handle_error(e)
                return ExitCodes.command_error

            try:
                self.api.application(app['id']).start.put(
                    {'name': app['name']})
            except SlumberHttpBaseException, e:
                self.handle_error(e)
            else:
                self.log.info("Start task queued")

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


@ClientApplication.subcommand('start')
class Start(UPaaSApplication):

    DESCRIPTION = "Start application"

    ha_enabled = False
    worker_limit = 0
    memory_limit = 0

    @cli.switch(["H", "enable-ha"], help="Enable high availability")
    def set_ha_enabled(self):
        self.ha_enabled = True

    @cli.switch(["w", "workers"], int, mandatory=True,
                help="Maximum number of workers")
    def set_worker_limit(self, workers):
        self.worker_limit = workers

    @cli.switch(["m", "memory"], int, mandatory=True,
                help="Memory limit (MB)")
    def set_memory_limit(self, memory):
        self.memory_limit = memory

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
                    'application': app['id'],
                    'worker_limit': self.worker_limit,
                    'memory_limit': self.memory_limit,
                    'ha_enabled': self.ha_enabled})
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

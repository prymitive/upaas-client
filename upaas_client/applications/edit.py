# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013-2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from plumbum import cli

from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('edit')
class Edit(UPaaSApplication):

    DESCRIPTION = "Edit running application settings"

    workers_min = 0
    workers_max = 0

    @cli.switch(["w", "--workers-min"], int, help="Minimum number of workers")
    def set_workers_min(self, value):
        self.workers_min = value

    @cli.switch(["W", "--workers-max"], int, help="Maximum number of workers")
    def set_workers_max(self, value):
        self.workers_max = value

    def main(self, name):
        self.setup_logger()

        if not self.workers_min and not self.workers_max:
            self.log.error("To edit application provide new minimum or "
                           "maximum workers count")
            return ExitCodes.user_error
        if self.workers_min and self.workers_max \
                and self.workers_min > self.workers_max:
            self.log.error("Maximum number of workers must be higher than "
                           "minimum")
            return ExitCodes.user_error

        self.log.info("Getting app '%s' details" % name)

        self.api_connect(self.parent.config.server.login,
                         self.parent.config.server.apikey,
                         self.parent.config.server.url)

        try:
            resp = self.api.application.get(name=name)
        except SlumberHttpBaseException as e:
            self.handle_error(e)
            if e.response.status_code == 401:
                return ExitCodes.auth_error
        else:
            if not resp.get('objects'):
                self.log.error("No such application registered: %s" % name)
                return ExitCodes.notfound_error
        app = resp['objects'][0]

        try:
            resp = self.api.run_plan.get(application=app['id'])
        except SlumberHttpBaseException as e:
            self.handle_error(e)
        else:
            if not resp.get('objects'):
                self.log.error("Application is stopped")
                return ExitCodes.user_error
        run_plan = resp['objects'][0]

        payload = {}
        if self.workers_min:
            payload['workers_min'] = self.workers_min
        if self.workers_max:
            payload['workers_max'] = self.workers_max
        try:
            self.api.run_plan(run_plan['id']).patch(payload)
        except SlumberHttpBaseException as e:
            self.handle_error(e)
            return ExitCodes.command_error

        try:
            self.api.application(app['id']).update.put(
                {'name': app['name']})
        except SlumberHttpBaseException as e:
            self.handle_error(e)
        else:
            self.log.info("Update task queued")

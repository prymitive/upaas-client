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


@ClientApplication.subcommand('edit')
class Edit(UPaaSApplication):

    DESCRIPTION = u"Edit running application settings"

    workers_min = 0
    workers_max = 0

    @cli.switch(["w", "--workers-min"], int, help=u"Minimum number of workers")
    def set_workers_min(self, value):
        self.workers_min = value

    @cli.switch(["W", "--workers-max"], int, help=u"Maximum number of workers")
    def set_workers_max(self, value):
        self.workers_max = value

    def main(self, name):
        self.setup_logger()

        if not self.workers_min and not self.workers_max:
            self.log.error(u"To edit application provide new minimum or "
                           u"maximum workers count")
            return ExitCodes.user_error
        if self.workers_min and self.workers_max \
                and self.workers_min > self.workers_max:
            self.log.error(u"Maximum number of workers must be higher than "
                           u"minimum")
            return ExitCodes.user_error

        self.log.info(u"Getting app '%s' details" % name)

        self.api_connect(self.parent.config.server.login,
                         self.parent.config.server.apikey,
                         self.parent.config.server.url)

        try:
            resp = self.api.application.get(name=name)
        except SlumberHttpBaseException, e:
            self.handle_error(e)
        else:
            if not resp.get('objects'):
                self.log.error(u"No such application registered: %s" % name)
                return ExitCodes.notfound_error
        app = resp['objects'][0]

        try:
            resp = self.api.run_plan.get(application=app['id'])
        except SlumberHttpBaseException, e:
            self.handle_error(e)
        else:
            if not resp.get('objects'):
                self.log.error(u"Application is stopped")
                return ExitCodes.user_error
        run_plan = resp['objects'][0]

        payload = {}
        if self.workers_min:
            payload['workers_min'] = self.workers_min
        if self.workers_max:
            payload['workers_max'] = self.workers_max
        try:
            self.api.run_plan(run_plan['id']).patch(payload)
        except SlumberHttpBaseException, e:
            self.handle_error(e)
            return ExitCodes.command_error

        try:
            self.api.application(app['id']).update.put(
                {'name': app['name']})
        except SlumberHttpBaseException, e:
            self.handle_error(e)
        else:
            self.log.info(u"Update task queued")

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


@ClientApplication.subcommand('build')
class Build(UPaaSApplication):

    DESCRIPTION = "Build new application package"

    force_fresh = False

    @cli.switch(["f", "force-fresh"], help="Force building fresh package")
    def set_force_fresh(self):
        self.force_fresh = True

    def main(self, name):
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
                if self.force_fresh:
                    self.api.application(app['id']).build_fresh.put(
                        {'name': app['name']})
                else:
                    self.api.application(app['id']).build.put(
                        {'name': app['name']})
            except SlumberHttpBaseException, e:
                self.handle_error(e)
            else:
                self.log.info("Build task queued (fresh: "
                              "%s)" % self.force_fresh)

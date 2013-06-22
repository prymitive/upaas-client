# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from plumbum import cli

from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication
from upaas.config.metadata import MetadataConfig

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('update')
class Update(UPaaSApplication):

    DESCRIPTION = "Update application metadata"

    @cli.switch(["m", "metadata"], str, help="Application metadata file path",
                mandatory=True)
    def set_metadata_path(self, path):
        self.metadata_path = path

    @cli.switch(["n", "name"], str, help="Application name", mandatory=True)
    def set_name(self, name):
        self.name = name

    def main(self):
        self.setup_logger()
        self.log.info("Registering new application using metadata at "
                      "%s" % self.metadata_path)

        meta = MetadataConfig.from_file(self.metadata_path)

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

            try:
                self.api.application(app['id']).put(
                    {'name': app['name'], 'metadata': meta.dump_string()})
            except SlumberHttpBaseException, e:
                self.handle_error(e)
            else:
                self.log.info("Application '%s' metadata updated "
                              "successfully" % self.name)

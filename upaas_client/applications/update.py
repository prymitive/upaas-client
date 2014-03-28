# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013-2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from __future__ import unicode_literals

from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication
from upaas.config.metadata import MetadataConfig

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('update')
class Update(UPaaSApplication):

    DESCRIPTION = "Update application metadata"

    def main(self, name, metadata_path):
        self.setup_logger()
        self.log.info("Registering new application using metadata at "
                      "%s" % metadata_path)

        meta = MetadataConfig.from_file(metadata_path)

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

            try:
                self.api.application(app['id']).patch(
                    {'metadata': meta.dump_string()})
            except SlumberHttpBaseException as e:
                self.handle_error(e)
            else:
                self.log.info("Application '%s' metadata updated "
                              "successfully" % name)

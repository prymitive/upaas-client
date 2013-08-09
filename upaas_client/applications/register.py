# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication
from upaas.config.metadata import MetadataConfig

from upaas_client.main import ClientApplication
from upaas_client.return_codes import ExitCodes


@ClientApplication.subcommand('register')
class Register(UPaaSApplication):

    DESCRIPTION = "Register new application"

    def main(self, name, metadata_path):
        self.setup_logger()
        self.log.info("Registering new application using metadata at "
                      "%s" % metadata_path)

        meta = MetadataConfig.from_file(metadata_path)

        self.api_connect(self.parent.config.server.login,
                         self.parent.config.server.apikey,
                         self.parent.config.server.url)

        try:
            self.api.application.post({'name': name,
                                       'metadata': meta.dump_string()})
        except SlumberHttpBaseException, e:
            self.handle_error(e)
            return ExitCodes.command_error
        else:
            self.log.info("Application '%s' created successfully" % name)

# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from plumbum import cli

from slumber.exceptions import SlumberHttpBaseException

from upaas.cli.base import UPaaSApplication
from upaas.metadata import MetadataConfig

from upaas_client.main import ClientApplication


@ClientApplication.subcommand('register')
class Register(UPaaSApplication):

    DESCRIPTION = "Register new application"

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
            self.api.application.post({'name': self.name,
                                       'metadata': meta.dump_string()})
        except SlumberHttpBaseException, e:
            self.log.error(e.content)
        else:
            self.log.info("Application '%s' created successfully" % self.name)

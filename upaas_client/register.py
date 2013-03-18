# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from plumbum import cli

from upaas.cli.base import UPaaSApplication

from upaas_client.main import ClientApplication


@ClientApplication.subcommand('register')
class Register(UPaaSApplication):

    DESCRIPTION = "Register new application"

    @cli.switch(["m", "metadata"], str, help="Application metadata file path",
                mandatory=True)
    def set_metadata_path(self, path):
        self.metadata_path = path

    def main(self):
        self.setup_logger()
        self.log.info("Registering new application using metadata at "
                      "%s" % self.metadata_path)

# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from upaas import config


class ClientConfig(config.Config):

    schema = {
        "server": {
            "url": config.StringEntry(required=True),
            "login": config.StringEntry(required=True),
            "apikey": config.StringEntry(required=True),
        }
    }

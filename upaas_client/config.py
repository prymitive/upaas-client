# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013-2014 by Łukasz Mierzwa
    :contact: l.mierzwa@gmail.com
"""


from upaas.config import base


class ClientConfig(base.Config):

    schema = {
        "server": {
            "url": base.StringEntry(required=True),
            "login": base.StringEntry(required=True),
            "apikey": base.StringEntry(required=True),
        }
    }

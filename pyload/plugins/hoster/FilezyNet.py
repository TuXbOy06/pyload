# -*- coding: utf-8 -*-

from pyload.plugins.internal.DeadHoster import DeadHoster, create_getInfo


class FilezyNet(DeadHoster):
    __name    = "FilezyNet"
    __type    = "hoster"
    __version = "0.20"

    __pattern = r'http://(?:www\.)?filezy\.net/\w{12}'

    __description = """Filezy.net hoster plugin"""
    __license     = "GPLv3"
    __authors     = []


getInfo = create_getInfo(FilezyNet)

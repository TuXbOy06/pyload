# -*- coding: utf-8 -*-

import re

from pyload.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class DropboxCom(SimpleHoster):
    __name    = "DropboxCom"
    __type    = "hoster"
    __version = "0.03"

    __pattern = r'https?://(?:www\.)?dropbox\.com/.+'

    __description = """Dropbox.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zapp-brannigan", "fuerst.reinje@web.de")]


    NAME_PATTERN = r'<title>Dropbox - (?P<N>.+?)<'
    SIZE_PATTERN = r'&nbsp;&middot;&nbsp; (?P<S>[\d.,]+) (?P<U>[\w^_]+)'

    OFFLINE_PATTERN = r'<title>Dropbox - (404|Shared link error)<'

    COOKIES = [("dropbox.com", "lang", "en")]


    def setup(self):
        self.multiDL = True
        self.chunkLimit = 1
        self.resumeDownload = True


    def handleFree(self):
        self.download(self.pyfile.url, get={'dl': "1"})

        check = self.checkDownload({'html': re.compile("html")})
        if check == "html":
            self.error(_("Downloaded file is an html page"))


getInfo = create_getInfo(DropboxCom)

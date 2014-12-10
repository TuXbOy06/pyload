# -*- coding: utf-8 -*-

import re

from pyload.plugins.internal.captcha import ReCaptcha
from pyload.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo


class CatShareNet(SimpleHoster):
    __name    = "CatShareNet"
    __type    = "hoster"
    __version = "0.08"

    __pattern = r'http://(?:www\.)?catshare\.net/\w{16}'

    __description = """CatShare.net hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("z00nx", "z00nx0@gmail.com"),
                       ("prOq", None),
                       ("Walter Purcaro", "vuolter@gmail.com")]


    TEXT_ENCODING = True

    INFO_PATTERN = r'<title>(?P<N>.+) \((?P<S>[\d.,]+) (?P<U>[\w^_]+)\)<'
    OFFLINE_PATTERN = ur'Podany plik został usunięty\s*</div>'

    IP_BLOCKED_PATTERN = ur'>Nasz serwis wykrył że Twój adres IP nie pochodzi z Polski.<'
    SECONDS_PATTERN = 'var\scount\s=\s(\d+);'
    LINK_PATTERN = r'<form action="(.+?)" method="GET">'


    def setup(self):
        self.multiDL        = self.premium
        self.resumeDownload = True


    def getFileInfo(self):
        m = re.search(self.IP_BLOCKED_PATTERN, self.html)
        if m:
            self.fail(_("Only connections from Polish IP address are allowed"))
        return super(CatShareNet, self).getFileInfo()


    def handleFree(self):
        m = re.search(self.SECONDS_PATTERN, self.html)
        if m:
            wait_time = int(m.group(1))
            self.wait(wait_time, True)

        recaptcha = ReCaptcha(self)

        challenge, response = recaptcha.challenge()
        self.html = self.load(self.pyfile.url,
                              post={'recaptcha_challenge_field': challenge,
                                    'recaptcha_response_field' : response})

        m = re.search(self.LINK_PATTERN, self.html)
        if m is None:
            self.invalidCaptcha()
            self.retry(reason=_("Wrong captcha entered"))

        dl_link = m.group(1)
        self.download(dl_link, disposition=True)


getInfo = create_getInfo(CatShareNet)

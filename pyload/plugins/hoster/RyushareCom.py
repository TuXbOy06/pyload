# -*- coding: utf-8 -*-
#
# Test links:
# http://ryushare.com/cl0jy8ric2js/random.bin

import re

from pyload.plugins.internal.XFSHoster import XFSHoster, create_getInfo
from pyload.plugins.internal.captcha import SolveMedia


class RyushareCom(XFSHoster):
    __name    = "RyushareCom"
    __type    = "hoster"
    __version = "0.20"

    __pattern = r'http://(?:www\.)?ryushare\.com/\w+'

    __description = """Ryushare.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("zoidberg", "zoidberg@mujmail.cz"),
                       ("stickell", "l.stickell@yahoo.it"),
                       ("quareevo", "quareevo@arcor.de")]


    HOSTER_DOMAIN = "ryushare.com"

    SIZE_PATTERN = r'You have requested <font color="red">[^<]+</font> \((?P<S>[\d.,]+) (?P<U>[\w^_]+)'

    WAIT_PATTERN = r'You have to wait ((?P<hour>\d+) hour[s]?, )?((?P<min>\d+) minute[s], )?(?P<sec>\d+) second[s]'
    LINK_PATTERN = r'<a href="([^"]+)">Click here to download<'


    def getDownloadLink(self):
        retry = False
        self.html = self.load(self.pyfile.url)
        action, inputs = self.parseHtmlForm(input_names={"op": re.compile("^download")})
        if "method_premium" in inputs:
            del inputs['method_premium']

        self.html = self.load(self.pyfile.url, post=inputs)
        action, inputs = self.parseHtmlForm('F1')

        self.setWait(65)
        # Wait 1 hour
        if "You have reached the download-limit" in self.html:
            self.setWait(1 * 60 * 60, True)
            retry = True

        m = re.search(self.WAIT_PATTERN, self.html)
        if m:
            wait = m.groupdict(0)
            waittime = int(wait['hour']) * 60 * 60 + int(wait['min']) * 60 + int(wait['sec'])
            self.setWait(waittime, True)
            retry = True

        self.wait()
        if retry:
            self.retry()

        for _i in xrange(5):
            solvemedia = SolveMedia(self)
            challenge, response = solvemedia.challenge()

            inputs['adcopy_challenge'] = challenge
            inputs['adcopy_response'] = response

            self.html = self.load(self.pyfile.url, post=inputs)
            if "WRONG CAPTCHA" in self.html:
                self.invalidCaptcha()
            else:
                self.correctCaptcha()
                break
        else:
            self.fail(_("You have entered 5 invalid captcha codes"))

        if "Click here to download" in self.html:
            return re.search(r'<a href="([^"]+)">Click here to download</a>', self.html).group(1)


getInfo = create_getInfo(RyushareCom)

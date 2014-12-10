# -*- coding: utf-8 -*-

import re
from time import mktime, strptime

from pycurl import REFERER

from pyload.plugins.Account import Account


class FilefactoryCom(Account):
    __name    = "FilefactoryCom"
    __type    = "account"
    __version = "0.14"

    __description = """Filefactory.com account plugin"""
    __license     = "GPLv3"
    __authors     = [("zoidberg", "zoidberg@mujmail.cz"),
                       ("stickell", "l.stickell@yahoo.it")]


    VALID_UNTIL_PATTERN = r'Premium valid until: <strong>(?P<d>\d{1,2})\w{1,2} (?P<m>\w{3}), (?P<y>\d{4})</strong>'


    def loadAccountInfo(self, user, req):
        html = req.load("http://www.filefactory.com/account/")

        m = re.search(self.VALID_UNTIL_PATTERN, html)
        if m:
            premium = True
            validuntil = re.sub(self.VALID_UNTIL_PATTERN, '\g<d> \g<m> \g<y>', m.group(0))
            validuntil = mktime(strptime(validuntil, "%d %b %Y"))
        else:
            premium = False
            validuntil = -1

        return {"premium": premium, "trafficleft": -1, "validuntil": validuntil}


    def login(self, user, data, req):
        req.http.c.setopt(REFERER, "http://www.filefactory.com/member/login.php")

        html = req.load("http://www.filefactory.com/member/signin.php", post={
            "loginEmail": user,
            "loginPassword": data['password'],
            "Submit": "Sign In"})

        if req.lastEffectiveURL != "http://www.filefactory.com/account/":
            self.wrongPassword()

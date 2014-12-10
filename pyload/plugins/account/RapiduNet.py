# -*- coding: utf-8 -*-

import re

from pyload.plugins.Account import Account
from pyload.utils import json_loads


class RapiduNet(Account):
    __name = "RapiduNet"
    __type = "account"
    __version = "0.01"

    __description = """Rapidu.net account plugin"""
    __license = "GPLv3"
    __authors = [("prOq", None)]


    ACCOUNT_INFO_PATTERN = '<a href="premium/" style="padding-left: 0px;">Account: <b>(.*?)</b></a>'


    def loadAccountInfo(self, user, req):
	premium = False

        req.load('https://rapidu.net/ajax.php?a=getChangeLang', post={"_go": "", "lang": "en"})
	self.html = req.load('https://rapidu.net/', decode=True)

	m = re.search(self.ACCOUNT_INFO_PATTERN, self.html)
	if m:
	    if m.group(1) == "Premium":
		premium = True

        return {"validuntil": None, "trafficleft": None, "premium": premium}


    def login(self, user, data, req):
        try:
            json = req.load('https://rapidu.net/ajax.php?a=getUserLogin', post={"_go": "", "login": user, "pass": data['password'], "member": "1"})
            json = json_loads(json)
            self.logDebug(json)

            if not json['message'] == "success":
		self.wrongPassword()
        except Exception, e:
            self.logError(e)


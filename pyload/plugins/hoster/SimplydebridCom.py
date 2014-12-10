# -*- coding: utf-8 -*-

import re

from pyload.plugins.Hoster import Hoster


class SimplydebridCom(Hoster):
    __name    = "SimplydebridCom"
    __type    = "hoster"
    __version = "0.10"

    __pattern = r'http://(?:www\.)?\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/sd\.php/*'

    __description = """Simply-debrid.com hoster plugin"""
    __license     = "GPLv3"
    __authors     = [("Kagenoshin", "kagenoshin@gmx.ch")]


    def setup(self):
        self.resumeDownload = True
        self.multiDL        = True
        self.chunkLimit     = 1


    def process(self, pyfile):
        if not self.account:
            self.logError(_("Please enter your %s account or deactivate this plugin") % "simply-debrid.com")
            self.fail(_("No simply-debrid.com account provided"))

        self.logDebug("Old URL: %s" % pyfile.url)

        #fix the links for simply-debrid.com!
        new_url = pyfile.url
        new_url = new_url.replace("clz.to", "cloudzer.net/file")
        new_url = new_url.replace("http://share-online", "http://www.share-online")
        new_url = new_url.replace("ul.to", "uploaded.net/file")
        new_url = new_url.replace("uploaded.com", "uploaded.net")
        new_url = new_url.replace("filerio.com", "filerio.in")
        new_url = new_url.replace("lumfile.com", "lumfile.se")
        if('fileparadox' in new_url):
            new_url = new_url.replace("http://", "https://")

        if re.match(self.__pattern, new_url):
            new_url = new_url

        self.logDebug("New URL: %s" % new_url)

        if not re.match(self.__pattern, new_url):
            page = self.load("http://simply-debrid.com/api.php", get={'dl': new_url})  # +'&u='+self.user+'&p='+self.account.getAccountData(self.user)['password'])
            if 'tiger Link' in page or 'Invalid Link' in page or ('API' in page and 'ERROR' in page):
                self.fail(_("Unable to unrestrict link"))
            new_url = page

        self.setWait(5)
        self.wait()
        self.logDebug("Unrestricted URL: " + new_url)

        self.download(new_url, disposition=True)

        check = self.checkDownload({"bad1": "No address associated with hostname", "bad2": "<html"})

        if check == "bad1" or check == "bad2":
            self.retry(24, 3 * 60, "Bad file downloaded")

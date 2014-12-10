# -*- coding: utf-8 -*-

from pyload.plugins.internal.DeadCrypter import DeadCrypter, create_getInfo


class C1neonCom(DeadCrypter):
    __name    = "C1neonCom"
    __type    = "crypter"
    __version = "0.05"

    __pattern = r'http://(?:www\.)?c1neon\.com/.*?'
    __config  = []

    __description = """C1neon.com decrypter plugin"""
    __license     = "GPLv3"
    __authors     = [("godofdream", "soilfiction@gmail.com")]


getInfo = create_getInfo(C1neonCom)

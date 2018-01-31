# -*- coding: utf-8 -*-

import collections


class Argument(object):

    def __init__(self, sid, tid, rep, flag=None):
        assert isinstance(tid, int)
        assert isinstance(rep, str)
        self.sid = sid
        self.tid = tid
        self.rep = rep
        self.flag = flag


class Pas(object):

    def __init__(self, val=None, knpstyle=False):
        assert isinstance(knpstyle, bool)
        self.cfid = None
        self.arguments = collections.defaultdict(list)
        if val is None:
            return
        if knpstyle:
            self._parseKnpStyle(val)
            return
        raise ValueError

    def _parseKnpStyle(self, val):
        assert isinstance(val, str)
        c0 = val.find(':')
        c1 = val.find(':', c0 + 1)
        self.cfid = val[:c0] + ":" + val[c0 + 1:c1]

        if val.count(":") < 2:  # For copula
            return

        for k in val[c1 + 1:].split(';'):
            items = k.split("/")
            caseflag = items[1]
            if caseflag == "U" or caseflag == "-":
                continue

            mycase = items[0]
            rep = items[2]
            tid = int(items[3])
            sid = items[5]
            arg = Argument(sid, tid, rep, caseflag)

            self.arguments[mycase].append(arg)

if __name__ == '__main__':
    pass

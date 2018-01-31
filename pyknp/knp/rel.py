# -*- coding: utf-8 -*-

import re

REL_PAT = r"rel type=\"([^\s]+?)\"(?: mode=\"([^>]+?)\")? target=\"([^\s]+?)\"(?: sid=\"(.+?)\" id=\"(.+?)\")?/"
WRITER_READER_LIST = ["著者", "読者"]
WRITER_READER_CONV_LIST = {"一人称": "著者", "二人称": "読者"}


class Rel(object):

    def __init__(self, fstring):
        self.atype = None
        self.target = None
        self.sid = None
        self.tid = None
        self.mode = None
        self.ignore = False

        match = re.findall(REL_PAT, fstring)
        if not match:
            self.ignore = True
            return
        atype, mode, target, sid, tid = match[0]
        if mode == "？":
            self.ignore = True
        if target == "なし":
            self.ignore = True

        if not sid:
            sid = None  # dummy
            if target in WRITER_READER_CONV_LIST:
                target = WRITER_READER_CONV_LIST[target]
        if not tid:
            tid = None  # dummy
        if tid is not None:
            tid = int(tid)

        self.atype = atype
        self.target = target
        self.sid = sid
        self.tid = tid
        self.mode = mode

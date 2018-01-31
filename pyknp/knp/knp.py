#-*- encoding: utf-8 -*-
import os
import sys
import re
import unittest
from functools import partial
from pyknp import Juman, Jumanpp
from pyknp import Socket, Subprocess
from pyknp import BList


class KNP(object):
    """
    KNP を用いて構文解析を行うモジュールである．
    """

    def __init__(self, command='knp', option='-tab', rcfile='',
                 server=None, port=31000, timeout=30,
                 pattern=r'(?:^|\n)EOS($|\n)',
                 jumanrcfile='', juman_option='-e2 -B', juman_port=32000,
                 juman_command='juman', jumanpp=False):

        self.use_jumanpp = (juman_command == "jumanpp") or jumanpp
        assert 'EOS' in pattern
        self.pattern = pattern
        self.EOS = 'EOS'
        # tab形式しかパースしない
        assert '-tab' in option

        if rcfile and not os.path.isfile(os.path.expanduser(rcfile)):
            sys.stderr.write("Can't read rcfile (%s)!\n" % rcfile)
            quit(1)

        # Setup Juman(++)
        assert port != juman_port
        juman_args = {'option': juman_option, 'rcfile': jumanrcfile,
                      'server':server, 'port':juman_port}
        if self.use_jumanpp:
            self.juman = Jumanpp(**juman_args)
        else:
            self.juman = Juman(**juman_args)
        # Setup KNP
        if server is not None:
            self.socket = Socket(server, port, option=option, timeout=timeout)
            self.query = partial(self.socket.query, pattern=pattern)
        else:
            if rcfile:
                option += " -r {}".format(rcfile)
            self.subprocess = Subprocess(command, option=option)
            self.query = partial(self.subprocess.query, pattern=pattern)

    def parse_sentence(self, sentence):
        assert isinstance(sentence, str)
        juman_lines = self.juman.juman_lines(sentence)
        if self.EOS not in juman_lines:
            juman_lines += self.EOS
        return self.query(juman_lines)

    def knp(self, sentence):
        assert isinstance(sentence, str)
        result = BList(self.parse_sentence(sentence))
        return result

    def parse(self, sentence):
        """
        文字列 sentence を対象として構文解析を行い，構文解析結果オブジェクトを返す．
        """
        return self.knp(sentence)

    def result(self, input_str):
        return BList(input_str, self.EOS)


class KNPTest(unittest.TestCase):

    def setUp(self):
        self.knp = KNP()

    def test_dpnd(self):
        result = self.knp.parse("赤い花が咲いた。")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].parent.bnst_id, 1)
        self.assertEqual(len(result[1].children), 1)
        self.assertEqual(result[1].children[0].bnst_id, 0)
        self.assertEqual(result[1].parent.bnst_id, 2)
        self.assertEqual(result[2].parent, None)

    def test_mrph(self):
        result = self.knp.parse("赤い花が咲いた。")
        self.assertEqual(
            ''.join([mrph.midasi for mrph in result[0].mrph_list()]), '赤い')
        self.assertEqual(
            ''.join([mrph.midasi for mrph in result[1].mrph_list()]), '花が')
        self.assertEqual(
            ''.join([mrph.midasi for mrph in result[2].mrph_list()]), '咲いた。')

if __name__ == '__main__':
    unittest.main()

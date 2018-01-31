#-*- encoding: utf-8 -*-
import os
import sys
import unittest
from functools import partial
from pyknp import MList
from pyknp import Socket, Subprocess


class Jumanpp(object):
    """
    形態素解析器 JUMAN++ を Python から利用するためのモジュールである．
    """

    def __init__(self, command='jumanpp', option='-e2 -B', rcfile='',
                 server=None, port=32000, timeout=30,
                 pattern=r'(?:^|\n)EOS($|\n)'):

        if rcfile and not os.path.isfile(os.path.expanduser(rcfile)):
            sys.stderr.write("Can't read rcfile (%s)!\n" % rcfile)
            quit(1)

        if server is not None:
            self.socket = Socket(server, port, option=option, timeout=timeout)
            self.query = partial(self.socket.query, pattern=pattern)
        else:
            if rcfile:
                option = "{} -r {}".format(option, rcfile).lstrip()
            self.subprocess = Subprocess(command, option=option)
            self.query = partial(self.subprocess.query, pattern=pattern)

    # method for passing output string to KNP
    def juman_lines(self, input_str):
        return self.jumanpp_lines(input_str)

    def jumanpp_lines(self, input_str):
        return self.query(input_str)

    def jumanpp(self, input_str):
        assert isinstance(input_str, str)
        result = MList(self.jumanpp_lines(input_str))
        return result

    def juman(self, input_str):
        return self.jumanpp(input_str)

    def analysis(self, input_str):
        """
        指定された文字列 input_str を形態素解析し，その結果を MList オブジェクトとして返す．
        """
        return self.jumanpp(input_str)

    def result(self, input_str):
        return MList(input_str)


class JumanppTest(unittest.TestCase):

    def setUp(self):
        self.jumanpp = Jumanpp()

    def test_normal(self):
        test_str = "この文を解析してください。"
        result = self.jumanpp.analysis(test_str)
        self.assertEqual(len(result), 7)
        self.assertEqual(''.join(mrph.midasi for mrph in result), test_str)
        self.assertGreaterEqual(len(result.spec().split("\n")), 7)

    def test_nominalization(self):
        test_str = "音の響きを感じる。"
        result = self.jumanpp.analysis(test_str)
        self.assertEqual(len(result), 6)
        self.assertEqual(''.join(mrph.midasi for mrph in result), test_str)
        self.assertGreaterEqual(len(result.spec().split("\n")), 6)
        self.assertEqual(result[2].midasi, "響き")
        self.assertEqual(result[2].hinsi, "名詞")

    def test_whitespace(self):
        test_str = "半角 スペース"
        result = self.jumanpp.analysis(test_str)
        self.assertEqual(len(result), 3)
        self.assertEqual((result[1].bunrui == '空白'), True)
        self.assertEqual(''.join(mrph.midasi for mrph in result), r"半角 スペース")
        self.assertGreaterEqual(len(result.spec().split("\n")), 3)

if __name__ == '__main__':
    unittest.main()

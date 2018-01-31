#-*- encoding: utf-8 -*-

import re
import socket
from subprocess import Popen, PIPE, TimeoutExpired


class Socket(object):

    def __init__(self, hostname, port, option=None, timeout=30):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._BS = 1024
        try:
            self.sock.connect((hostname, port))
        except ConnectionRefusedError:
            raise Exception("No server: hostname={}, port={}".format(hostname, port))
        if option is not None:
            send_option = "RUN {}".format(option).encode("utf8") + b'\n'
            self.sock.send(send_option)
        self.sock.settimeout(timeout)

        data = b""
        while "OK".encode('utf8') not in data:
            data = self.sock.recv(self._BS)

    def __del__(self):
        if self.sock:
            self.sock.close()

    def query(self, sentence, pattern=r'(?:^|\n)EOS\n'):
        assert(isinstance(sentence, str))
        input_bytes = sentence.strip().encode('utf-8')+b'\n'

        self.sock.sendall(input_bytes)
        data = self.sock.recv(self._BS)
        out = data.decode('utf8')
        while not re.search(pattern, out):
            data = self.sock.recv(self._BS)
            out += data.decode('utf8')

        return out.strip()


class Subprocess(object):

    def __init__(self, command, option='', timeout=30):
        options = option.split(' ')
        self.subprocess_args = [command] + options
        self.timeout = timeout

    def query(self, sentence, pattern=r'(?:^|\n)EOS\n'):
        assert(isinstance(sentence, str))
        input_bytes = sentence.strip().encode('utf-8')+b'\n'
            
        # 呼び出しごとに子プロセス生成
        process = Popen(self.subprocess_args, stdin=PIPE, stdout=PIPE)
        try:
            out, _ = process.communicate(input_bytes, self.timeout)
        except TimeoutExpired:
            process.kill()
            out, _ = process.communicate(input_bytes)

        return out.decode('utf8').strip()
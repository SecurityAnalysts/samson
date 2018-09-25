#!/usr/bin/python3
import zlib
from Crypto.Cipher import AES
from samson.block_ciphers.modes.cbc import CBC
from samson.block_ciphers.modes.ctr import CTR

from samson.utilities.general import rand_bytes
from samson.attacks.compression_ratio_side_channel_attack import CompressionRatioSideChannelAttack
from samson.attacks.crime_attack import CRIMEAttack
import unittest

import logging
logging.basicConfig(format='%(asctime)s - %(name)s [%(levelname)s] %(message)s', level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

block_size = 16
secret = b"Cookie: sessionid=TmV2ZXIgcmV2ZWFsIHRoZSBXdS1UYW5nIFNlY3JldCE="

def aes_ctr_oracle(message):
    aes = AES.new(rand_bytes(block_size), AES.MODE_ECB)
    ciphertext = CTR(aes.encrypt, rand_bytes(block_size // 2), block_size).encrypt(zlib.compress(message))
    return len(ciphertext)


def aes_cbc_oracle(message):
    aes = AES.new(rand_bytes(block_size), AES.MODE_ECB)
    ciphertext = CBC(aes.encrypt, aes.decrypt, rand_bytes(block_size), block_size).encrypt(zlib.compress(message))
    return len(ciphertext)


def format_req(message):
    return """
POST / HTTP/1.1
Host: hapless.com
{}
Content-Length: {}
{}
""".format(secret.decode(), len(message), message).encode()


class CompressionRatioSideChannelTestCase(unittest.TestCase):
    def setUp(self):
        self.request = None

    def test_ctr(self):
        self.request = lambda msg: aes_ctr_oracle(format_req(msg))
        self._execute()

    
    def test_cbc(self):
        self.request = lambda msg: aes_cbc_oracle(format_req(msg))
        self._execute()


    def _execute(self):
        known_plaintext = b'Cookie: '
        attack = CRIMEAttack(self)

        recovered_plaintext = attack.execute(known_plaintext)

        print(recovered_plaintext)
        self.assertEqual(recovered_plaintext, secret)
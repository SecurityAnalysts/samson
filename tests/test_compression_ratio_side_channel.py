#!/usr/bin/python3
import zlib
from samson.primitives.aes_ctr import AES_CTR
from samson.primitives.aes_cbc import encrypt_aes_cbc
from samson.utilities import gen_rand_key
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
    ciphertext = AES_CTR(gen_rand_key(block_size), gen_rand_key(block_size // 2)).encrypt(zlib.compress(message))
    return len(ciphertext)


def aes_cbc_oracle(message):
    ciphertext = encrypt_aes_cbc(gen_rand_key(block_size), gen_rand_key(block_size), zlib.compress(message), block_size=block_size)
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
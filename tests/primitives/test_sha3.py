from samson.hashes.sha3 import SHA3
from samson.utilities.bytes import Bytes
import hashlib
import unittest

class SHA3TestCase(unittest.TestCase):
    def test_sha3(self):
        for hash_type, reference_method in [(SHA3.K224, hashlib.sha3_224), (SHA3.K256, hashlib.sha3_256), (SHA3.K384, hashlib.sha3_384), (SHA3.K512, hashlib.sha3_512)]:
            for _ in range(10):
                in_bytes = Bytes.random(128)
                sha3 = hash_type()
                self.assertEqual(sha3.hash(in_bytes), reference_method(in_bytes).digest())
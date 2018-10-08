#!/usr/bin/python3
import base64
from samson.block_ciphers.rijndael import Rijndael
from samson.block_ciphers.modes.ecb import ECB

from samson.utilities.general import rand_bytes
from samson.oracles.stateless_block_encryption_oracle import StatelessBlockEncryptionOracle
from samson.attacks.ecb_prepend_attack import ECBPrependAttack
import unittest

import logging
logging.basicConfig(format='%(asctime)s - %(name)s [%(levelname)s] %(message)s', level=logging.DEBUG)

key_size = 16
block_size = 16


key = rand_bytes(key_size)
unknown_string = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'.encode())


def encrypt_rand_ecb(message):
    mod_plain = message + unknown_string
    return ECB(Rijndael(key).encrypt, None, block_size).encrypt(mod_plain)


class ECBPrependAttackTestCase(unittest.TestCase):
    def test_prepend_attack(self):
        attack = ECBPrependAttack(StatelessBlockEncryptionOracle(encrypt_rand_ecb))
        recovered_plaintext = attack.execute()

        self.assertEqual(unknown_string, recovered_plaintext)
        print(recovered_plaintext)

#!/usr/bin/python3
from samson.utilities.general import rand_bytes
from Crypto.Cipher import AES
from samson.block_ciphers.modes.cbc import CBC
from samson.attacks.cbc_iv_key_equivalence_attack import CBCIVKeyEquivalenceAttack
import base64
import unittest

import logging
logging.basicConfig(format='%(asctime)s - %(name)s [%(levelname)s] %(message)s', level=logging.DEBUG)

block_size = 32
key = rand_bytes(block_size)
iv = key

aes = AES.new(key, AES.MODE_ECB)
cbc = CBC(aes.encrypt, aes.decrypt, iv, block_size)

def sender_encrypt(data):
    return cbc.encrypt(data)


def receiver_decrypt(ciphertext):
    plaintext = cbc.decrypt(ciphertext, unpad=False)
    if any(int(byte) > 127 for byte in plaintext):
        raise Exception('Bad characters in {}'.format(base64.b64encode(plaintext)))



class CBCIVEquivalenceTestCase(unittest.TestCase):
    def test_equivalence_attack(self):
        plaintext = b'-Super secret message! Hope no one cracks this!-'
        ciphertext = sender_encrypt(plaintext)

        attack = CBCIVKeyEquivalenceAttack(self, block_size)
        key_iv = bytes(attack.execute(ciphertext))

        self.assertEqual(key_iv, key)
        recovered_plaintext = CBC(None, AES.new(key_iv, AES.MODE_ECB).decrypt, key_iv, block_size).decrypt(bytes(ciphertext))
        
        print(recovered_plaintext)
        self.assertEqual(plaintext, recovered_plaintext)


    def request(self, ciphertext):
        try:
            receiver_decrypt(ciphertext)
            return None
        except Exception as e:
            prefix = len('Bad characters in b\'')
            return base64.b64decode(str(e)[prefix:-1])

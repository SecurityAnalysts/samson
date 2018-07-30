#!/usr/bin/python3
from samson.utilities import gen_rand_key, pkcs7_pad
from samson.attacks.hmac_forgery_attack import HMACForgeryAttack
from samson.primitives.sha1 import Sha1Hash
import unittest

key = gen_rand_key()

def insecure_hmac(key, data):
    hash_obj = Sha1Hash()
    hash_obj.update(key + data)
    return hash_obj.digest()


class HMACForgeryTestCase(unittest.TestCase):
    def test_forgery_attack(self):
        message = b'comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon'
        original = insecure_hmac(key, message)
        forged_append = b';admin=true'

        attack = HMACForgeryAttack()

        actual_secret_len = -1
        crafted_payload = None
        new_signature = None

        for secret_len in range(64):
            # We attempt a forgery
            payload, signature = attack.execute(original, message, forged_append, secret_len)

            # Server calculates HMAC with secret
            desired = insecure_hmac(key, payload)

            if signature == desired:
                actual_secret_len = secret_len
                crafted_payload = payload
                new_signature = signature
                break

        self.assertEqual(actual_secret_len, len(key))
        self.assertEqual(insecure_hmac(key, crafted_payload), new_signature)
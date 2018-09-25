#!/usr/bin/python3
import urllib.parse
from samson.utilities.general import rand_bytes
from Crypto.Cipher import AES
from samson.block_ciphers.modes.cbc import CBC
from samson.block_ciphers.modes.ctr import CTR

from samson.attacks.xor_bitflipping_attack import XORBitflippingAttack
from samson.oracles.encryption_oracle import EncryptionOracle
import unittest

block_size = 16
key = rand_bytes(block_size)
iv = rand_bytes(block_size)
nonce = rand_bytes(block_size // 2)

aes = AES.new(key, AES.MODE_ECB)
cbc = CBC(aes.encrypt, aes.decrypt, iv, block_size)

def format_data(data):
    return ("comment1=cooking%20MCs;userdata=" + urllib.parse.quote(data) + ";comment2=%20like%20a%20pound%20of%20bacon").encode()


# CBC Functions
def encrypt_data_cbc(data):
    return cbc.encrypt(format_data(data))


def login_cbc(ciphertext):
    print(cbc.decrypt(ciphertext))
    return b';admin=true;' in cbc.decrypt(ciphertext)


# CTR Functions
def encrypt_data_ctr(data):
    return CTR(aes.encrypt, nonce, block_size).encrypt(format_data(data))


def login_ctr(ciphertext):
    return b';admin=true;' in CTR(aes.encrypt, nonce, block_size).encrypt(ciphertext)


class XORBitFlipTestCase(unittest.TestCase):
    def test_bitflip(self):
        oracle = EncryptionOracle(encrypt_data_cbc)
        attack = XORBitflippingAttack(oracle, block_size=block_size)
        forged_request = attack.execute(b'hiya;admin=true;' * (block_size // 16), 16)

        if(login_cbc(bytes(forged_request))):
            print('Success! We\'re admin!')
        
        self.assertTrue(login_cbc(bytes(forged_request)))


    def test_ctr_bitflip(self):
        oracle = EncryptionOracle(encrypt_data_ctr)
        attack = XORBitflippingAttack(oracle, block_size=block_size)
        forged_request = attack.execute(b'hiya;admin=true;' * (block_size // 16), 32)

        if(login_ctr(bytes(forged_request))):
            print('Success! We\'re admin!')

        self.assertTrue(login_ctr(bytes(forged_request)))
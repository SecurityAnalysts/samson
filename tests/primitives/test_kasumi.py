from samson.block_ciphers.kasumi import KASUMI
from samson.utilities.encoding import int_to_bytes
import codecs
import unittest


class KASUMITestCase(unittest.TestCase):
    def _run_test(self, key, plaintext, test_vector, iterations=1):
        kasumi = KASUMI(key)

        to_enc = plaintext
        for _ in range(iterations):
            to_enc = kasumi.encrypt(to_enc)
        
        ciphertext = to_enc
        self.assertEqual(ciphertext, test_vector)

        to_dec = ciphertext
        for _ in range(iterations):
            to_dec = kasumi.decrypt(to_dec)
        
        self.assertEqual(to_dec, plaintext)


    # https://www.cosic.esat.kuleuven.be/nessie/testvectors/bc/kasumi/Kasumi-128-64.verified.test-vectors
    def test_vec0(self):
        key = int_to_bytes(0x80000000000000000000000000000000, 'big')
        plaintext = int.to_bytes(0x0000000000000000, 8, 'big')
        test_vector = int_to_bytes(0x4B58A771AFC7E5E8, 'big')

        self._run_test(key, plaintext, test_vector)

        test_vector = int_to_bytes(0x5A188A5934CA8DEB, 'big')
        self._run_test(key, plaintext, test_vector, 1000)



    def test_vec1(self):
        key = int_to_bytes(0x2BD6459F82C5B300952C49104881FF48, 'big')
        plaintext = int.to_bytes(0x4B1644E60D25344F, 8, 'big')
        test_vector = int_to_bytes(0xEA024714AD5C4D84, 'big')

        self._run_test(key, plaintext, test_vector)
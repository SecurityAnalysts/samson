
from samson.utilities.math import mod_inv, lll, generate_superincreasing_seq, find_coprime
from samson.utilities.bytes import Bytes
import numpy as np

class MerkleHellmanKnapsack(object):
    def __init__(self, priv=None, q=None, r=None, max_diff=2**20):
        super_seq = generate_superincreasing_seq(9, max_diff)
        self.priv = priv or super_seq[:8]
        self.q = q or super_seq[-1]
        self.r = r or find_coprime(self.q, range(2, self.q))

        self.pub = [(w * self.r) % self.q for w in self.priv]


    def __repr__(self):
        return f"<MerkleHellmanKnapsack: priv={self.priv}, pub={self.pub}, q={self.q}, r={self.r}>"
    

    def __str__(self):
        return self.__repr__()


    def encrypt(self, message):
        bin_str = ''
        for byte in message:
            bin_str += bin(byte)[2:].zfill(8)

        all_sums = []
        
        for i in range(len(bin_str) // 8):
            byte_str = bin_str[i * 8:(i + 1) * 8]
            all_sums.append(sum([int(byte_str[j]) * self.pub[j] for j in range(8)]))

        return all_sums


    def decrypt(self, sums):
        r_inv = mod_inv(self.r, self.q)
        inv_sums = [(byte_sum * r_inv) % self.q for byte_sum in sums]
        plaintext = Bytes(b'')

        for inv_sum in inv_sums:
            curr = inv_sum
            bin_string = ''

            for i in range(7, -1, -1):
                if self.priv[i] <= curr:
                    curr -= self.priv[i]
                    bin_string += '1'
                else:
                    bin_string += '0'

            plaintext += int.to_bytes(int(bin_string[::-1], 2), 1, 'big')

        return plaintext


    @staticmethod
    def recover_plaintext(ciphertext, pub):
        ident = np.identity(len(pub))
        pub_matrix = np.append(ident, [pub], axis=0)
        problem_matrix = np.append(pub_matrix, np.array([[0] * len(pub) + [-ciphertext]]).T, axis=1)

        solution_matrix = lll(problem_matrix.T, 0.99)

        for row in solution_matrix:
            new_row = row[row[:] >= 0]
            new_row = new_row[new_row[:] <= 1]

            if len(new_row) == len(row):
                return row[:-1]
from samson.utilities.math import random_int, crt, pollards_kangaroo, mod_inv
from samson.utilities.runtime import RUNTIME
from samson.oracles.default_oracle import DefaultOracle
from functools import reduce
from sympy import factorint
import math

import logging
log = logging.getLogger(__name__)


class DiffieHellmanSubgroupConfinementAttack(object):
    """
    The Diffie-Hellman Subgroup Confinement attack takes advantage of smooth multiplicative group orders of unsafe primes used in Diffie-Hellman.
    There are two phases to this attack:
        1) Finding residues modulo the small factors of the multiplicative group order
        2) Probablistically solving the discrete logarithm of the remaining factors

    Conditions:
    * Diffie-Hellman is being used
    * The user has access to an oracle that accepts arbitrary public keys and returns the residue
    * The left over key space is small enough to solve DLP
    """

    def __init__(self, oracle: DefaultOracle, p: int, g: int, order: int):
        """
        Parameters:
            oracle (DefaultOracle): Oracle that accepts (public_key: int, factor: int) and returns (residue: int).
            p                (int): Prime modulus.
            g                (int): Generator.
            order            (int): Order of multiplicative group.
        """
        self.oracle = oracle
        self.p = p
        self.g = g
        self.order = order


    @RUNTIME.report
    def execute(self, public_key: int, max_factor_size: int=2**16) -> int:
        """
        Executes the attack.

        Parameters:
            public_key      (int): Diffie-Hellman public key to crack.
            max_factor_size (int): Max factor size to prevent attempting to factor forever.
        
        Returns:
            int: Private key.
        """
        # Factor as much as we can
        factors = [r for r,_ in factorint((self.p - 1) // self.order, limit=max_factor_size).items() if r < max_factor_size]
        log.debug(f'Found factors: {factors}')

        residues = []
        moduli   = []

        # Request residues from crafted public keys
        for factor in RUNTIME.report_progress(factors, desc='Sending malicious public keys', unit='factor'):
            h = 1
            while h == 1:
                h = pow(max(1, random_int(self.p)), (self.p-1) // factor, self.p)

            residue = self.oracle.request(h, factor)
            residues.append(residue)
            moduli.append(factor)


        # Build partials using CRT
        n, r = crt(residues, moduli)

        # Oh, I guess we already found it...
        if r > self.order:
            return n

        g_prime = pow(self.g, r, self.p)
        y_prime = (public_key * mod_inv(pow(self.g, n, self.p), self.p)) % self.p

        log.info(f'Recovered {"%.2f"%math.log(reduce(int.__mul__, factors, 1), 2)}/{"%.2f"%math.log(self.order, 2)} bits')
        log.info(f'Found relation: x = {n} + m*{r}')
        log.debug(f"g' = {g_prime}")
        log.debug(f"y' = {y_prime}")
        log.info('Attempting to catch a kangaroo...')

        # Probablistically solve DLP
        m = pollards_kangaroo(self.p, g_prime, y_prime, a=0, b=(self.order - 1) // r)
        return n + m*r

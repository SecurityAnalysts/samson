from samson.utilities.general import rand_bytes
from sympy.matrices import Matrix, GramSchmidt
from sympy import sieve
from sympy.abc import x
from types import FunctionType
from copy import deepcopy
import math

def int_to_poly(integer: int, modulus: int=2) -> object:
    """
    Encodes an integer as a polynomial.

    Parameters:
        integer (int): Integer to encode.
        modulus (int): Modulus to reduce the integer over.
    
    Returns:
        object: Polynomial representation.
    
    Examples:
        >>> from samson.math.general import int_to_poly
        >>> int_to_poly(100)
        <Polynomial: x**6 + x**5 + x**2, coeff_ring=ZZ/ZZ(2)>

        >>> int_to_poly(128, 3)
        <Polynomial: x**4 + x**3 + ZZ(2)*x**2 + ZZ(2), coeff_ring=ZZ/ZZ(3)>

    """
    from samson.math.all import ZZ, Polynomial
    base_coeffs = []

    # Use != to handle negative numbers
    while integer != 0 and integer != -1:
        integer, r = divmod(integer, modulus)
        base_coeffs.append(r)

    return Polynomial(base_coeffs, ZZ/ZZ(modulus))


def poly_to_int(poly: object) -> int:
    """
    Encodes an polynomial as a integer.

    Parameters:
        poly (Polynomial): Polynomial to encode.
        modulus     (int): Modulus to reconstruct the integer with.
    
    Returns:
        int: Integer representation.
    
    Examples:
        >>> from samson.math.general import int_to_poly, poly_to_int
        >>> poly_to_int(int_to_poly(100))
        100

        >>> poly_to_int(int_to_poly(100, 3))
        100

    """
    modulus = int(poly.coeff_ring.quotient.val)
    value   = 0
    for idx, coeff in poly.coeffs:
        value += int(coeff) * modulus**idx

    return value


def frobenius_monomial_base(poly: object) -> list:
    """
    Generates a list of monomials of x**(i*p) % g for range(poly.degrees()). Used with Frobenius map.

    Adapted from https://github.com/sympy/sympy/blob/d1301c58be7ee4cd12fd28f1c5cd0b26322ed277/sympy/polys/galoistools.py

    Parameters:
        poly (Polynomial): Polynomial to generate bases for.

    Returns:
        list: List of monomial bases mod g.
    """
    n = poly.degree()
    if n == 0:
        return []

    P = poly.ring
    q = poly.coeff_ring.order if hasattr(poly.coeff_ring, 'order') else poly.coeff_ring.characteristic
    bases = [None]*n
    bases[0] = P.one()

    if q < n:
        for i in range(1, n):
            bases[i] = (bases[i-1] << q) % poly

    elif n > 1:
        R = P/poly
        bases[1] = R(x)**q

        for i in range(2, n):
            bases[i] = bases[i-1] * bases[1]

        # Peel off the quotient ring
        for i in range(1, n):
            bases[i] = bases[i].val

    return bases


def frobenius_map(f: object, g: object, bases: list=None) -> object:
    """
    Computes f**p % g using the Frobenius map.

    https://en.wikipedia.org/wiki/Finite_field#Frobenius_automorphism_and_Galois_theory

    Parameters:
        f (Polynomial): Base.
        g (Polynomial): Modulus.
        bases   (list): Frobenius monomial bases. Will generate if not provided.
    
    Returns:
        Polynomial: f**p % g
    """
    if not bases:
        bases = frobenius_monomial_base(g)

    dg = g.degree()
    df = f.degree()
    P  = f.ring

    if df >= dg:
        f %= g
        df = f.degree()

    if not f:
        return f

    sf = P([f.coeffs[0]])

    for i in range(1, df+1):
        sf += bases[i] * P([f.coeffs[i]])

    return sf



def gcd(a: int, b: int) -> int:
    """
    Recursively computes the greatest common denominator.

    Parameters:
        a (int): First integer.
        b (int): Second integer.
    
    Returns:
        int: GCD of `a` and `b`.
    
    Examples:
        >>> from samson.math.general import gcd
        >>> gcd(256, 640)
        128

        >>> from samson.math.algebra.all import FF
        >>> from sympy.abc import x
        >>> P = FF(2, 8)[x]
        >>> gcd(P(x**2), P(x**5))
        <Polynomial: x**2, coeff_ring=F_(2**8)>

    """
    while True:
        if not b:
            return a
        else:
            a, b = b, a % b


# https://anh.cs.luc.edu/331/notes/xgcd.pdf
def xgcd(a: int, b: int, zero: int=0, one: int=1) -> (int, int, int):
    """
    Extended Euclidean algorithm form of GCD.
    `ax + by = gcd(a, b)`

    Parameters:
        a (int): First integer.
        b (int): Second integer.
    
    Returns:
        (int, int, int): Formatted as (GCD, x, y).
    
    Examples:
        >>> from samson.math.general import xgcd
        >>> xgcd(10, 5)
        (5, 0, 1)

        >>> from samson.math.algebra.all import FF
        >>> from sympy.abc import x
        >>> P = FF(2, 8)[x]
        >>> xgcd(P(x**2), P(x**5), P.zero(), P.one())
        (<Polynomial: x**2, coeff_ring=F_(2**8)>, <Polynomial: F_(2**8)(ZZ(1)), coeff_ring=F_(2**8)>, <Polynomial: F_(2**8)(ZZ(0)), coeff_ring=F_(2**8)>)

    """
    prevx, x = one, zero; prevy, y = zero, one
    while b:
        q = a // b
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, a % b
    return a, prevx, prevy



def lcm(a: int, b: int) -> int:
    """
    Calculates the least common multiple of `a` and `b`.

    Parameters:
        a (int): First integer.
        b (int): Second integer.
    
    Returns:
        int: Least common multiple.
    
    Examples:
        >>> from samson.math.general import lcm
        >>> lcm(2, 5)
        10

        >>> from samson.math.algebra.all import FF
        >>> from sympy.abc import x
        >>> P = FF(2, 8)[x]
        >>> lcm(P(x**2 + 5), P(x-6))
        <Polynomial: x**3 + F_(2**8)(x)*x**2 + F_(2**8)(x**2 + ZZ(1))*x + F_(2**8)(x**3 + x), coeff_ring=F_(2**8)>

    """
    return a // gcd(a, b) * b



def mod_inv(a: int, n: int, zero: int=0, one: int=1) -> int:
    """
    Calculates the modular inverse according to
    https://en.wikipedia.org/wiki/Euclidean_algorithm#Linear_Diophantine_equations
    and https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm.

    Parameters:
        a (int): Integer.
        n (int): Modulus.
    
    Returns:
        int: Modular inverse of `a` over `n`.
    
    Examples:
        >>> from samson.math.general import mod_inv
        >>> mod_inv(5, 11)
        9

    """
    _, x, _ = xgcd(a, n, zero=zero, one=one)

    if (a * x) % n != one:
        raise Exception("'a' is not invertible")

    if type(x) is int and x < zero:
        x = x + n

    return x


def square_and_mul(g: int, u: int, s: int=None) -> int:
    """
    Computes `s = g ^ u` over arbitrary rings.

    Parameters:
        g (int): Base.
        u (int): Exponent.
        s (int): The 'one' value of the ring.
    
    Returns:
        int: `g ^ u` within its ring.
    
    Examples:
        >>> from samson.math.general import mod_inv
        >>> square_and_mul(5, 10, 1)
        9765625

        >>> from samson.math.algebra.all import FF
        >>> from sympy.abc import x
        >>> P = FF(2, 8)[x]
        >>> square_and_mul(P(x+5), 32)
        <Polynomial: x**32 + F_(2**8)(x**6 + x**3 + x**2), coeff_ring=F_(2**8)>

    """
    s = s or g.ring.one()
    while u != 0:
        if u & 1:
            s = (s * g)
        u >>= 1
        g = (g * g)
    return s


def fast_mul(a: int, b: int, s: int=None) -> int:
    """
    Computes `s = a * b` over arbitrary rings.

    Parameters:
        a (int): Element `a`.
        b (int): Multiplier.
        s (int): The 'zero' value of the ring.
    
    Returns:
        int: `a * b` within its ring.
    
    Examples:
        >>> from samson.math.general import fast_mul
        >>> fast_mul(5, 12, 0)
        60

        >>> from samson.math.algebra.all import FF
        >>> from sympy.abc import x
        >>> P = FF(2, 8)[x]
        >>> fast_mul(P(x+5), 5)
        <Polynomial: x + F_(2**8)(x**2 + ZZ(1)), coeff_ring=F_(2**8)>

    """
    s = s if s is not None else a.ring.zero()
    if b < 0:
        b = -b
        a = -a

    while b != 0:
        if b & 1:
            s = (s + a)
        b >>= 1
        a = (a + a)
    return s


# https://stackoverflow.com/questions/23621833/is-cube-root-integer
def kth_root(n: int, k: int) -> int:
    """
    Calculates the `k`-th integer root of `n`.

    Parameters:
        n (int): Integer.
        k (int): Root (e.g. 2).
    
    Returns:
        int: `k`-th integer root of `n
    
    Examples:
        >>> from samson.math.general import kth_root
        >>> kth_root(1000, 3)
        10

        >>> kth_root(129, 7)
        3

    """
    lb, ub = 0, n #lower bound, upper bound
    while lb < ub:
        guess = (lb + ub) // 2
        if pow(guess, k) < n:
            lb = guess + 1
        else:
            ub = guess

    return lb


def crt(residues: list, moduli: list=None) -> (int, int):
    """
    Performs the Chinese Remainder Theorem and returns the computed `x` and modulus.

    Parameters:
        residues (list): Residues of `x` in order relative to `moduli`.
        moduli   (list): Moduli of the residues.
    
    Returns:
        (int, int): Formatted as (computed `x`, modulus).
    
    Examples:
        >>> from samson.math.general import crt
        >>> moduli = [5,7,11]
        >>> residues = [366 % modulus for modulus in moduli]
        >>> crt(residues, moduli)
        (366, 385)

        >>> from samson.math.algebra.all import ZZ
        >>> residues = [ring(366) for ring in [ZZ/ZZ(5), ZZ/ZZ(7), ZZ/ZZ(11)]]
        >>> crt(residues)
        (366, 385)

    """
    if moduli:
        assert len(residues) == len(moduli)
    else:
        moduli   = [int(residue.ring.quotient) for residue in residues]
        residues = [int(residue) for residue in residues]

    x  = residues[0]
    Nx = moduli[0]

    for i in range(1, len(residues)):
        x  = (mod_inv(Nx, moduli[i]) * (residues[i] - x)) * Nx + x
        Nx = Nx * moduli[i]

    return x % Nx, Nx



def legendre(a: int, p: int) -> int:
    """
    Calculates the Legendre symbol of `a` mod `p`. Nonzero quadratic residues mod `p` return 1 and nonzero, non-quadratic residues return -1. Zero returns 0.

    Parameters:
        a (int): Possible quadatric residue.
        p (int): Modulus.
    
    Returns:
        int: Legendre symbol.
    
    Examples:
        >>> from samson.math.general import legendre
        >>> legendre(4, 7)
        1

        >>> legendre(5, 7)
        6

    """
    return pow(a, (p - 1) // 2, p)


def generalized_eulers_criterion(a: int, k: int, p: int) -> int:
    """
    Determines if `a` is a `k`-th root over `p`.

    Parameters:
        a (int): Possible `k`-th residue.
        k (int): Root.
        p (int): Modulus.
    
    Returns:
        int: Legendre symbol (basically).

    Examples:
        >>> from samson.math.general import generalized_eulers_criterion
        >>> generalized_eulers_criterion(4, 2, 7)
        1

        >>> generalized_eulers_criterion(5, 2, 7)
        6

        >>> generalized_eulers_criterion(4, 3, 11)
        1
    """
    return pow(a, (p-1) // gcd(k, p-1), p)


# https://crypto.stackexchange.com/questions/22919/explanation-of-each-of-the-parameters-used-in-ecc
# https://www.geeksforgeeks.org/find-square-root-modulo-p-set-2-shanks-tonelli-algorithm/
# https://rosettacode.org/wiki/Tonelli-Shanks_algorithm#Python


def tonelli(n: int, p: int) -> int:
    """
    Performs the Tonelli-Shanks algorithm for calculating the square root of `n` mod `p`.

    Parameters:
        n (int): Integer.
        p (int): Modulus.
    
    Returns:
        int: Square root of `n` mod `p`.
    
    Examples:
        >>> from samson.math.general import tonelli
        >>> tonelli(4, 7)
        2

        >>> tonelli(2, 7)
        4

    """
    assert legendre(n, p) == 1, "not a square (mod p)"
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    if s == 1:
        return pow(n, (p + 1) // 4, p)

    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break

    c = pow(z, q, p)
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)

    m  = s
    t2 = 0
    while (t - 1) % p != 0:
        t2 = (t * t) % p

        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break

            t2 = (t2 * t2) % p

        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i

    return r



def tonelli_q(a: int, p: int, q: int) -> int:
    """
    Performs the Tonelli-Shanks algorithm for calculating the `q`th-root of `n` mod `p`.

    From "On Taking Roots in Finite Fields" (https://www.cs.cmu.edu/~glmiller/Publications/AMM77.pdf)

    Parameters:
        n (int): Integer.
        p (int): Modulus.
        q (int): Root to take.
    
    Returns:
        int: `q`th-root of `n` mod `p`.

    Examples:
        >>> from samson.math.general import tonelli_q
        >>> tonelli_q(4, 7, 2)
        2

        >>> tonelli_q(2, 7, 2)
        4

        >>> tonelli_q(8, 67, 3)
        58

        >>> 58**3 % 67
        8

    """
    # Step 1 & 2
    assert generalized_eulers_criterion(a, q, p) == 1, "not a power (mod p)"

    # Step 3
    for g in range(2, p):
        if generalized_eulers_criterion(g, q, p) == p-1:
            break

    # Step 4
    p_1 = p - 1
    k   = 0

    # The algorithm only works if q | p-1
    assert p_1 % q == 0

    n = q
    div = gcd(q, p-1)
    while div != 1 and div != n:
        n   = n // div
        div = gcd(n, p-1)


    if p_1 % n == 0:
        k = 1
        p_1 //= n

    N, N_prime = divmod(p_1, n)

    # Step 5
    l = 1

    while True:
        # Step 6
        for j in range(k):
            if pow(a, q**j*(q*N+N_prime), p) == 1:
                break

        # Step 7
        if j == 0:
            # Step 8
            return pow(a, mod_inv(n, n*N+N_prime), p) * mod_inv(l, p)
        else:
            for lamb in range(1, n):
                if gcd(lamb, n) == 1:
                    if (pow(a, pow(2, j-1)*pow(2, N+N_prime), p) * pow(g, lamb*pow(2, k-1)*(2*N+N_prime), p)) % p == 1:
                        break

            a = (a * pow(g, pow(2, (k-j  )*lamb), p)) % p
            l = (l * pow(g, pow(2, (k-j-1)*lamb), p)) % p



# https://github.com/orisano/olll/blob/master/olll.py
# https://en.wikipedia.org/wiki/Lenstra%E2%80%93Lenstra%E2%80%93Lov%C3%A1sz_lattice_basis_reduction_algorithm
def lll(in_basis: list, delta: float=0.75) -> Matrix:
    """
    Performs the Lenstra–Lenstra–Lovász lattice basis reduction algorithm.

    Parameters:
        in_basis (list): List of Matrix objects representing the original basis.
        delta   (float): Minimum optimality of the reduced basis.

    Returns:
        Matrix: Reduced basis.
    """
    basis = deepcopy(in_basis)
    n     = len(basis)
    ortho = GramSchmidt(basis)

    def mu(i, j):
        return ortho[j].dot(basis[i]) / ortho[j].dot(ortho[j])

    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            mu_kj = mu(k, j)
            if abs(mu_kj) > 0.5:
                basis[k] = basis[k] - basis[j] * round(mu_kj)
                ortho = GramSchmidt(basis)


        if ortho[k].dot(ortho[k]) >= (delta - mu(k, k - 1)**2) * (ortho[k - 1].dot(ortho[k - 1])):
            k += 1
        else:
            basis[k], basis[k - 1] = deepcopy(basis[k - 1]), deepcopy(basis[k])
            ortho = GramSchmidt(basis)
            k = max(k - 1, 1)

    return Matrix([list(map(int, b)) for b in basis])



def generate_superincreasing_seq(length: int, max_diff: int, starting: int=0) -> list:
    """
    Generates a superincreasing sequence.

    Parameters:
        length   (int): Number of elements to generate.
        max_diff (int): Maximum difference between the sum of all elements before and the next element.
        starting (int): Minimum starting integer.
    
    Returns:
        list: List of the superincreasing sequence.
    
    Examples:
        >>> from samson.math.general import generate_superincreasing_seq
        >>> generate_superincreasing_seq(10, 2)
        [...]

    """
    seq = []

    last_sum = starting
    for _ in range(length):
        delta = int.from_bytes(rand_bytes(math.ceil(math.log(max_diff, 256))), 'big') % max_diff
        seq.append(last_sum + delta)
        last_sum = sum(seq)

    return seq



def find_coprime(p: int, search_range: list) -> int:
    """
    Attempts to find an integer coprime to `p`.

    Parameters:
        p             (int): Integer to find coprime for.
        search_range (list): Range to look in.
    
    Returns:
        int: Integer coprime to `p`.
    
    Examples:
        >>> from samson.math.general import find_coprime
        >>> find_coprime(10, range(500, 1000))
        501

    """
    for i in search_range:
        if gcd(p, i) == 1:
            return i



def random_int(n: int) -> int:
    """
    Finds a unbiased, uniformly-random integer between 0 and `n`-1.

    Parameters:
        n (int): Upper bound.
    
    Returns:
        int: Random integer.
    
    Example:
        >>> from samson.math.general import random_int
        >>> random_int(1000) < 1000
        True

    """
    byte_length = math.ceil(n.bit_length() / 8)
    max_bit = 2**n.bit_length()
    q = max_bit // n
    max_num = n * q - 1
    while True:
        attempt = int.from_bytes(rand_bytes(byte_length), 'big') % max_bit
        if attempt <= max_num:
            return attempt % n



def find_prime(bits: int, ensure_halfway: bool=True) -> int:
    """
    Finds a prime of `bits` bits.

    Parameters:
        bits            (int): Bit length of prime.
        ensure_halfway (bool): Ensures the prime is at least halfway into the bitspace to prevent multiplications being one bit short (e.g. 256-bit int * 256-bit int = 511-bit int).
    
    Returns:
        int: Random prime number.
    
    Examples:
        >>> from samson.math.general import find_prime
        >>> find_prime(512) < 2**512
        True

    """
    rand_num = random_int(2**bits)
    rand_num |= 2**(bits - 1)

    if ensure_halfway:
        rand_num |= 2**(bits - 2)

    return next_prime(rand_num)



def next_prime(start_int: int) -> int:
    """
    Finds the next prime.

    Parameters:
        start_int (int): Integer to start search at.
    
    Returns:
        int: Prime.
    
    Examples:
        >>> from samson.math.general import next_prime
        >>> next_prime(8)
        11

        >>> next_prime(11+1)
        13

    """
    start_int |= 1
    while not is_prime(start_int):
        start_int += 2

    return start_int



# https://en.wikipedia.org/wiki/Berlekamp%E2%80%93Massey_algorithm
def berlekamp_massey(output_list: list) -> object:
    """
    Performs the Berlekamp-Massey algorithm to find the shortest LFSR for a binary output sequence.

    Parameters:
        output_list (list): Output of LFSR.
    
    Returns:
        Polynomial: Polyomial that represents the shortest LFSR.
    
    Examples:
        >>> from samson.prngs.flfsr import FLFSR
        >>> from samson.math.general import berlekamp_massey
        >>> from samson.math.all import Polynomial, ZZ
        >>> lfsr = FLFSR(3, Polynomial(x**25 + x**20 + x**12 + x**8  + 1, coeff_ring=ZZ/ZZ(2)))
        >>> outputs = [lfsr.generate() for _ in range(50)]
        >>> berlekamp_massey(outputs)
        <Polynomial: x**25 + x**17 + x**13 + x**5 + ZZ(1), coeff_ring=ZZ/ZZ(2)>

    """
    from samson.math.algebra.rings.integer_ring import ZZ
    from samson.math.polynomial import Polynomial
    n = len(output_list)
    b = [1] + [0] * (n - 1)
    c = [1] + [0] * (n - 1)

    L = 0
    m = -1

    i  = 0
    while i < n:
        out_vec = output_list[i - L:i][::-1]
        c_vec = c[1:L+i]
        d = output_list[i] + sum([s_x * c_x for s_x, c_x in zip(out_vec, c_vec)]) % 2

        if d == 1:
            t = deepcopy(c)
            p = [0] * n
            for j in range(L):
                if b[j] == 1:
                    p[j + i - m] = 1

            c = [(c_x + p_x) % 2 for c_x, p_x in zip(c, p)]

            if L <= i / 2:
                L = i + 1 - L
                m = i
                b = t

        i += 1

    return Polynomial(c[:L + 1][::-1], coeff_ring=ZZ/ZZ(2))


def is_power_of_two(n: int) -> bool:
    """
    Determines if `n` is a power of two.

    Parameters:
        n (int): Integer.
    
    Returns:
        bool: Whether or not `n` is a power of two.
    
    Examples:
        >>> from samson.math.general import is_power_of_two
        >>> is_power_of_two(7)
        False

        >>> is_power_of_two(8)
        True

    """
    return n != 0 and (n & (n - 1) == 0)



def pollards_kangaroo(p: int, g: int, y: int, a: int, b: int, iterations: int=30, f: FunctionType=None) -> int:
    """
    Probablistically finds the discrete logarithm of base `g` in GF(`p`) of `y` in the interval [`a`, `b`].

    Parameters:
        p          (int): Prime modulus.
        g          (int): Generator.
        y          (int): Number to find the discrete logarithm of.
        a          (int): Interval start.
        b          (int): Interval end.
        iterations (int): Number of times to run the outer loop. If `f` is None, it's used in the pseudorandom map.
        f         (func): pseudorandom map function.
    
    Returns:
        int: The discrete logarithm. Possibly None if it couldn't be found.
    
    Examples:
        >>> from samson.math.general import pollards_kangaroo
        >>> g, x, p = 5, 13, 67
        >>> y = pow(g, x, p)
        >>> pollards_kangaroo(p, g, y, 0, 20)
        585

        >>> pow(5, 585, 67) == y
        True

    """
    k = iterations

    if not f:
        f = lambda y: pow(2, y % k, p)

    while k > 1:
        N = (f(0) + f(b)) // 2  * 4

        # Tame kangaroo
        xT = 0
        yT = pow(g, b, p)

        for _ in range(N):
            f_yT  = f(yT)
            xT   += f_yT
            yT    = (yT * pow(g, f_yT, p)) % p


        # Wild kangaroo
        xW = 0
        yW = y

        while xW < b - a + xT:
            f_yW = f(yW)
            xW  += f_yW
            yW   = (yW * pow(g, f_yW, p)) % p

            if yW == yT:
                return b + xT - xW


        # Didn't find it. Try another `k`
        k -= 1



def hasse_frobenius_trace_interval(p: int) -> (int, int):
    """
    Finds the interval relative to `p` in which the Frobenius trace must reside according to Hasse's theorem.

    Parameters:
        p (int): Prime of the underlying field of the elliptic curve.
    
    Returns:
        (int, int): Start and end ranges of the interval relative to `p`.
    
    Examples:
        >>> from samson.math.general import hasse_frobenius_trace_interval
        >>> hasse_frobenius_trace_interval(53)
        (-16, 17)

    """
    l = 2 * math.ceil(math.sqrt(p))
    return (-l , l + 1)



def primes_product(n: int, blacklist: list=None) -> list:
    """
    Returns a list of small primes whose product is greater than or equal to `n`.

    Parameters:
        n          (int): Product to find.
        blacklist (list): Primes to skip.
    
    Returns:
        list: List of primes.
    
    Examples:
        >>> from samson.math.general import primes_product
        >>> primes_product(100, [2])
        [7, 5, 3]

    """
    total     = 1
    primes    = []
    blacklist = blacklist if blacklist else []

    for prime in sieve.primerange(2, n.bit_length()*2+1):
        if total >= n:

            # We might be able to remove some of the large primes
            primes.reverse()
            needed_primes = []
            for prime in primes:
                if total // prime >= n:
                    total //= prime
                else:
                    needed_primes.append(prime)

            return needed_primes

        if prime not in blacklist:
            primes.append(prime)
            total *= prime



def find_representative(quotient_element: object, valid_range: list) -> int:
    """
    Finds the representative element of `quotient_element` within `valid_range`.

    Parameters:
        quotient_element (QuotientElement): Element to search for.
        valid_range                 (list): Range to search in.
    
    Returns:
        int: Representative element.
    
    Examples:
        >>> from samson.math.all import *
        >>> find_representative((ZZ/ZZ(11))(3), range(11, 22))
        14

    """
    remainder = int(quotient_element)
    modulus   = int(quotient_element.ring.quotient)

    if len(valid_range) > modulus:
        raise ValueError("Solution not unique")

    q, r = divmod(valid_range[0], modulus)
    shifted_range = range(r, r + len(valid_range))

    if remainder in shifted_range:
        return q * modulus + remainder

    elif remainder + modulus in shifted_range:
        return (q+1) * modulus + remainder

    else:
        raise ValueError("No solution")



def frobenius_endomorphism(point: object, q: int) -> object:
    """
    Computes the Frobenius endomorphism of the `point`.

    Parameters:
        point (object): Original point.
        q        (int): Power to raise to.
    
    Returns:
        object: Resultant point.
    """
    return point.__class__(x=point.x**q, y=point.y**q, curve=point.curve)



def frobenius_trace_mod_l(curve: object, l: int) -> object:
    """
    Finds the Frobenius trace modulo `l` for faster computation.

    Parameters:
        curve (object): Elliptic curve.
        l        (int): Prime modulus.

    Returns:
        QuotientElement: Modular residue of the Frobenius trace.
    """
    from samson.math.algebra.curves.weierstrass_curve import WeierstrassCurve
    from samson.math.algebra.fields.fraction_field import FractionField as Frac
    from samson.math.algebra.rings.integer_ring import ZZ

    torsion_quotient_ring = ZZ/ZZ(l)
    psi = curve.division_poly(l)

    # Build symbolic torsion group
    R = curve.curve_poly_ring
    S = R/psi
    T = Frac(S, simplify=False)
    sym_curve = WeierstrassCurve(a=curve.a, b=curve.b, ring=T)

    p_x = T(R((x, 0)))
    p_y = T(R((0, 1)))

    point = sym_curve(p_x, p_y)

    # Generate symbolic points
    p1 = frobenius_endomorphism(point, curve.p)
    p2 = frobenius_endomorphism(p1, curve.p)
    determinant = (curve.p % l) * point

    point_sum = determinant + p2

    # Find trace residue
    if point_sum == sym_curve.POINT_AT_INFINITY:
        return torsion_quotient_ring(0)

    trace_point = p1
    for candidate in range(1, (l + 1) // 2):
        if point_sum.x == trace_point.x:
            if point_sum.y == trace_point.y:
                return torsion_quotient_ring(candidate)
            else:
                return torsion_quotient_ring(-candidate)
        else:
            trace_point += p1

    raise ArithmeticError("No trace candidate satisfied the Frobenius equation")



def frobenius_trace(curve: object) -> int:
    """
    Calculates the Frobenius trace of the `curve`.

    Parameters:
        curve (object): Elliptic curve.
    
    Returns:
        int: Frobenius trace.
    
    Examples:
        >>> from samson.math.general import frobenius_trace
        >>> from samson.math.algebra.all import *

        >>> ring = ZZ/ZZ(53)
        >>> curve = WeierstrassCurve(a=50, b=7, ring=ring, base_tuple=(34, 25))
        >>> frobenius_trace(curve)
        -3

    """
    from samson.math.algebra.rings.integer_ring import ZZ
    from samson.math.polynomial import Polynomial

    search_range      = hasse_frobenius_trace_interval(curve.p)
    torsion_primes    = primes_product(search_range[1] - search_range[0], [curve.ring.characteristic])
    trace_congruences = []

    # Handle 2 separately to prevent multivariate poly arithmetic
    if 2 in torsion_primes:
        defining_poly = Polynomial(x**3 + curve.a*x + curve.b, coeff_ring=curve.ring)
        bases         = frobenius_monomial_base(defining_poly)
        rational_char = bases[1]
        rational_char = frobenius_map(rational_char, defining_poly, bases=bases)

        if gcd(rational_char - curve.ring[x](x), defining_poly).degree() == 0:
            trace_congruences.append((ZZ/ZZ(2))(1))
        else:
            trace_congruences.append((ZZ/ZZ(2))(0))

        torsion_primes.remove(2)


    for l in torsion_primes:
        trace_congruences.append(frobenius_trace_mod_l(curve, l))

    n, mod = crt(trace_congruences)
    return find_representative((ZZ/ZZ(mod))(n), range(*search_range))


def schoofs_algorithm(curve: object) -> int:
    """
    Performs Schoof's algorithm to count the number of points on an elliptic curve.

    Parameters:
        curve (object): Elliptic curve to find cardinality of.
    
    Returns:
        int: Curve cardinality
    
    Examples:
        >>> from samson.math.general import schoofs_algorithm
        >>> from samson.math.algebra.all import *

        >>> ring = ZZ/ZZ(53)
        >>> curve = WeierstrassCurve(a=50, b=7, ring=ring, base_tuple=(34, 25))
        >>> schoofs_algorithm(curve)
        57

    """
    return curve.p + 1 - frobenius_trace(curve)


def bsgs(g: object, h: object, end: int, e: object=1, start: int=0) -> int:
    """
    Performs Baby-step Giant-step with an arbitrary finite cyclic group.

    Parameters:
        g  (object): Generator/base.
        h  (object): The result to find the discrete logarithm of.
        end   (int): End of the search range.
        e  (object): Starting point of the aggregator.
        start (int): Start of the search range.
    
    Returns:
        int: The discrete logarithm of `h` given `g` over `p`.

    Examples:
        >>> from samson.math.general import hasse_frobenius_trace_interval, bsgs, mod_inv
        >>> from samson.math.algebra.all import *

        >>> ring = ZZ/ZZ(53)
        >>> curve = WeierstrassCurve(a=50, b=7, ring=ring, base_tuple=(34, 25))
        >>> start, end = hasse_frobenius_trace_interval(curve.p)
        >>> bsgs(curve.G, curve.POINT_AT_INFINITY, e=curve.POINT_AT_INFINITY, start=start + curve.p, end=end + curve.p)
        57

        >>> ring = ZZ/ZZ(53)
        >>> mul = ring.mul_group()
        >>> base = mul(7)
        >>> exponent = 24
        >>> h = base * exponent
        >>> bsgs(base, h, int(ring.quotient))
        50

    """
    search_range = end - start
    table        = {}
    m            = kth_root(search_range, 2)

    for i in range(m):
        table[e] = i
        e += g

    factor = g * m
    o = g * start
    e = h
    for i in range(m):
        e = h - o
        if e in table:
            return i*m + table[e] + start

        o += factor

    return None


def miller_rabin(n: int, k: int=64, bases: list=None) -> bool:
    """
    Probablistic primality test. Each iteration has a 1/4 false positive rate.
    Always returns a false positive on Carmichael numbers.

    https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test#Miller%E2%80%93Rabin_test

    Parameters:
        n (int): Number to determine if probably prime.
        k (int): Number of iterations to run.
    
    Returns:
        bool: Whether `n` is probably prime.

    Examples:
        >>> from samson.math.general import miller_rabin
        >>> miller_rabin(127)
        True

        >>> miller_rabin(6)
        False

        >>> miller_rabin(29341) and 29341 % 13 == 0 # Carmichael number
        True

    """
    n_1 = n - 1
    d   = n_1
    r   = 0
    while not d % 2 and d:
        r += 1
        d %= 2

    if not bases:
        def generator():
            for _ in range(k):
                yield max(2, random_int(n_1))

        bases = generator()

    for a in bases:
        x = pow(a, d, n)
        if x == 1 or x == n_1:
            continue

        found = False
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n_1:
                found = True
                break

        if not found:
            return False

    return True


FB_LARGE_MOD = 3989930175
def is_square(n: int) -> bool:
    """
    Determines if `n` is a square using "fenderbender" tests first.

    https://mersenneforum.org/showpost.php?p=110896

    Parameters:
        n (int): Number to test.

    Returns:
        bool: Whether or not `n` is a square.
    """
    if n in [0, 1]:
        return True

    m = n % 128
    if ((m*0x8bc40d7d) & (m*0xa1e2f5d1) & 0x14020a):
        return False

    n_mod = n % FB_LARGE_MOD

    m = n_mod % 63
    if ((m*0x3d491df7) & (m*0xc824a9f9) & 0x10f14008):
        return False

    m = n_mod % 25
    if ((m*0x1929fc1b) & (m*0x4c9ea3b2) & 0x51001005):
         return False

    return kth_root(n, 2)**2 == n


def jacobi_symbol(n: int, k: int) -> int:
    """
    Generalization of the Legendre symbol.

    https://en.wikipedia.org/wiki/Jacobi_symbol

    Parameters:
        n (int): Possible quadatric residue.
        k (int): Modulus (must be odd).
    
    Return:
        int: Jacobi symbol.
    """
    assert k > 0 and k % 2 == 1
    n %= k
    t = 1

    while n != 0:
        while n % 2 == 0:
            n //= 2
            r = k % 8

            if r in [3, 5]:
                t = -t

        n, k = k, n
        if n % 4 == 3 and k % 4 == 3:
            t = -t

        n %= k

    if k == 1:
        return t
    else:
        return 0


def generate_lucas_selfridge_parameters(n: int) -> (int, int, int):
    """
    Generates the Selfridge parameters to use in Lucas strong pseudoprime testing.

    Parameters:
        n (int): Possible prime.
    
    Returns:
        (int, int, int): Selfridge parameters.
    """
    D = 5
    while True:
        g = gcd(abs(D), n)
        if g > 1 and g != n:
            return (0, 0, 0)

        if jacobi_symbol(D, n) == -1:
            break

        if D > 0:
            D = -D - 2
        else:
            D = -D + 2

    return (D, 1, (1-D) // 4)


def generate_lucas_sequence(n: int, P: int, Q: int, k: int) -> (int, int, int):
    """
    Adapted from https://docs.sympy.org/latest/_modules/sympy/ntheory/primetest.html#isprime
    """
    D = P**2 - 4*Q

    assert n > 1
    assert k >= 0
    assert D != 0

    if k == 0:
        return (0, 2, Q)

    U  = 1
    V  = P
    Qk = Q
    b  = k.bit_length()

    while b > 1:
        U = U*V % n
        V = (V*V - 2*Qk) % n
        Qk *= Qk
        b  -= 1

        if (k >> (b - 1)) & 1:
            U, V = U*P + V, V*P + U*D

            if U & 1:
                U += n

            if V & 1:
                V += n

            U >>= 1
            V >>= 1
            Qk *= Q

        Qk %= n

    return (U % n, V % n, Qk)


def is_strong_lucas_pseudoprime(n: int) -> bool:
    if n == 2:
        return True

    if n < 2 or n % 2 == 0 or is_square(n):
        return False

    D, P, Q = generate_lucas_selfridge_parameters(n)
    if D == 0:
        return False

    s    = 0
    q, r = divmod(n+1, 2)
    k    = q
    while q and not r:
        k    = q
        s   += 1
        q, r = divmod(q, 2)

    U, V, Qk = generate_lucas_sequence(n, P, Q, k)
    if U == 0 or V == 0:
        return True

    for _ in range(s):
        V = (V**2 - 2*Qk) % n

        if V == 0:
            return True

        Qk = pow(Qk, 2, n)

    return False


PRIMES_UNDER_1000 = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997}

def is_prime(n: int) -> bool:
    """
    Determines if `n` is probably prime using the Baillie-PSW primality test.

    https://en.wikipedia.org/wiki/Baillie%E2%80%93PSW_primality_test

    Parameters:
        n (int): Positive integer.
    
    Returns:
        bool: Whether or not `n` is probably prime.
    """
    if n in PRIMES_UNDER_1000:
        return True

    for prime in PRIMES_UNDER_1000:
        if (n % prime) == 0:
            return False

    return miller_rabin(n, bases=[2]) and is_strong_lucas_pseudoprime(n)

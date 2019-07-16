from samson.math.general import int_to_poly, fast_mul, is_prime
from samson.math.algebra.fields.field import Field, FieldElement
from samson.math.algebra.rings.polynomial_ring import PolynomialRing
from samson.math.polynomial import Polynomial
from sympy.polys.galoistools import gf_irreducible_p
import itertools

class FiniteFieldElement(FieldElement):
    """
    Element of a `FiniteField`.
    """

    def __init__(self, val: Polynomial, field: Field):
        """
        Parameters:
            val    (Polynomial): Value of the element.
            field (FiniteField): Parent field.
        """
        self.field = field
        self.val   = self.field.internal_field.coerce(val)


    def __repr__(self):
        return f"<FiniteFieldElement: val={self.val}, field={self.field}>"


    def shorthand(self) -> str:
        return self.field.shorthand() + f'({self.val.shorthand()})'


    def ordinality(self) -> int:
        return int(self)


    def __add__(self, other: object) -> object:
        other = self.ring.coerce(other)
        return FiniteFieldElement(self.val + other.val, self.field)

    def __mul__(self, other: object) -> object:
        other = self.ring.coerce(other)
        return FiniteFieldElement(self.val * other.val, self.field)

    def __rmul__(self, other: object) -> object:
        return self.__mul__(other)

    def __sub__(self, other: object) -> object:
        other = self.ring.coerce(other)
        return FiniteFieldElement(self.val - other.val, self.field)

    def __mod__(self, other: object) -> object:
        other = self.ring.coerce(other)
        return FiniteFieldElement(self.val % other.val, self.field)

    def __invert__(self) -> object:
        return FiniteFieldElement(~self.val, self.field)

    def __neg__(self) -> object:
        return FiniteFieldElement(-self.val, self.field)

    def __truediv__(self, other: object) -> object:
        other = self.ring.coerce(other)
        return self * ~other

    def __floordiv__(self, other: object) -> object:
        return self.__truediv__(other)



class FiniteField(Field):
    """
    Finite field of GF(p**n) constructed using a `PolynomialRing`.

    Examples:
        >>> from samson.math import *
        >>> from sympy.abc import x
        >>> F = FiniteField(2, 8)
        >>> assert F(5) / F(5) == F(1)
        >>> F[x]/(F[x].one()*2)
        <QuotientRing ring=F_(2**8)[x], quotient=<Polynomial: F_(2**8)(ZZ(0)), coeff_ring=F_(2**8)>>

    """

    def __init__(self, p: int, n: int=1, reducing_poly: Polynomial=None):
        """
        Parameters:
            p                    (int): Prime.
            n                    (int): Exponent.
            reducing_poly (Polynomial): Polynomial to reduce the `PolynomialRing`.
        """
        from samson.math.algebra.all import ZZ
        from sympy import ZZ as sym_ZZ

        assert is_prime(p)
        self.p = p
        self.n = n

        self.internal_ring = ZZ/ZZ(p)

        if not reducing_poly:
            if n == 1:
                reducing_poly = Polynomial([0, 1], self.internal_ring)
            else:
                for c in itertools.product(range(p), repeat=n):
                    poly = (1, *c)
                    if gf_irreducible_p(poly, p, sym_ZZ):
                        reducing_poly = Polynomial(poly[::-1], self.internal_ring)
                        break
                    # poly = Polynomial((1, *c)[::-1], self.internal_ring)
                    # if poly.is_irreducible():
                    #     reducing_poly = poly
                    #     break


        self.reducing_poly  = reducing_poly

        poly_ring           = PolynomialRing(self.internal_ring)
        self.internal_field = poly_ring/poly_ring(reducing_poly)


    def __repr__(self):
        return f"<FiniteField: p={self.p}, n={self.n}, reducing_poly={self.reducing_poly}>"


    def __hash__(self) -> int:
        return hash((self.internal_field, self.reducing_poly, self.__class__))


    def zero(self) -> FiniteFieldElement:
        """
        Returns:
            FiniteFieldElement: '0' element of the algebra.
        """
        return self.coerce(0)


    def one(self) -> FiniteFieldElement:
        """
        Returns:
            FiniteFieldElement: '1' element of the algebra.
        """
        return self.coerce(1)


    def random(self, size: int=None) -> FiniteFieldElement:
        """
        Generate a random element.

        Parameters:
            size (int): The ring-specific 'size' of the element.
    
        Returns:
            FiniteFieldElement: Random element of the algebra.
        """
        from samson.math.general import random_int
        return self[random_int(size or self.order)]


    def shorthand(self) -> str:
        return f'F_({self.p}**{self.n})' if self.n > 1 else f'F_{self.p}'


    @property
    def characteristic(self) -> int:
        return self.p


    @property
    def order(self) -> int:
        return self.p**self.n


    def coerce(self, other: object) -> FiniteFieldElement:
        """
        Attempts to coerce other into an element of the algebra.

        Parameters:
            other (object): Object to coerce.
        
        Returns:
            FiniteFieldElement: Coerced element.
        """
        if type(other) is int:
            other = int_to_poly(other, self.p) % self.reducing_poly

        if not type(other) is FiniteFieldElement:
            other = FiniteFieldElement(self.internal_field(other), self)

        return other


    def element_at(self, x: int) -> object:
        return FiniteFieldElement(self.internal_field.element_at(x), self)


    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and self.p == other.p and self.n == other.n

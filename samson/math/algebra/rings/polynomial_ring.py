from samson.math.algebra.rings.ring import Ring, RingElement
from samson.math.polynomial import Polynomial
from sympy import Expr


class PolynomialRing(Ring):
    """
    Ring of polynomials over a ring.

    Examples:
        >>> from samson.math.all import *
        >>> poly_ring = (ZZ/ZZ(53))[x]
        >>> poly_ring(x**3 + 4*x - 3)
        <Polynomial: x**3 + ZZ(4)*x + ZZ(50), coeff_ring=ZZ/ZZ(53)>

    """

    def __init__(self, ring: Ring):
        """
        Parameters:
            ring (Ring): Underlying ring.
        """
        self.ring = ring


    @property
    def characteristic(self):
        return self.ring.characteristic


    def zero(self) -> Polynomial:
        """
        Returns:
            Polynomial: '0' element of the algebra.
        """
        return Polynomial([self.ring(0)], coeff_ring=self.ring, ring=self)


    def one(self) -> Polynomial:
        """
        Returns:
            Polynomial: '1' element of the algebra.
        """
        return Polynomial([self.ring(1)], coeff_ring=self.ring, ring=self)


    def random(self, size: int=None) -> Polynomial:
        """
        Generate a random element.

        Parameters:
            size (int): The ring-specific 'size' of the element.
    
        Returns:
            Polynomial: Random element of the algebra.
        """
        if not size:
            size = 1

        # TODO: How do we specify this size?
        return Polynomial([self.ring.random(3) for _ in range(size)], coeff_ring=self.ring, ring=self)


    def __repr__(self):
        return f"<PolynomialRing ring={self.ring}>"


    def shorthand(self) -> str:
        return f'{self.ring.shorthand()}[x]'


    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and self.ring == other.ring


    def __hash__(self) -> int:
        return hash((self.ring, self.__class__))


    def coerce(self, other: object) -> Polynomial:
        """
        Attempts to coerce other into an element of the algebra.

        Parameters:
            other (object): Object to coerce.
        
        Returns:
            Polynomial: Coerced element.
        """
        if type(other) is list or issubclass(type(other), Expr):
            return Polynomial(other, coeff_ring=self.ring, ring=self)

        elif type(other) is Polynomial:
            return other

        raise Exception('Coercion failed')

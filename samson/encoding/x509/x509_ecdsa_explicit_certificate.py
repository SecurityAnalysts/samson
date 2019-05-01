from samson.utilities.bytes import Bytes
from pyasn1.codec.der import decoder
from pyasn1.type.univ import Sequence
from pyasn1_modules import rfc2459
from pyasn1.error import PyAsn1Error
from fastecdsa.curve import Curve
from fastecdsa.point import Point

class X509ECDSAExplicitCertificate(object):

    @staticmethod
    def check(buffer: bytes):
        try:
            cert, _ = decoder.decode(buffer, asn1Spec=rfc2459.Certificate())
            alg = cert['tbsCertificate']['subjectPublicKeyInfo']['algorithm']
            return str(alg['algorithm']) == '1.2.840.10045.2.1' and type(decoder.decode(alg['parameters'])[0]) == Sequence
        except PyAsn1Error as _:
            return False


    @staticmethod
    def encode(rsa_key: object):
        pass


    @staticmethod
    def decode(buffer: bytes):
        from samson.public_key.ecdsa import ECDSA

        cert, _left_over = decoder.decode(buffer, asn1Spec=rfc2459.Certificate())
        pub_info = cert['tbsCertificate']['subjectPublicKeyInfo']

        curve_params, _ = decoder.decode(Bytes(pub_info['algorithm']['parameters']))

        p = int(curve_params[1][1])
        b = Bytes(curve_params[2][1]).int()
        q = int(curve_params[4])
        gx, gy = ECDSA.decode_point(Bytes(curve_params[3]))

        curve = Curve('Explicit curve', p=p, a=-3, b=b, q=q, gx=gx, gy=gy)

        x, y = ECDSA.decode_point(Bytes(int(pub_info['subjectPublicKey'])))
        ecdsa = ECDSA(curve.G, None, d=1)
        ecdsa.Q = Point(x, y, curve)

        return ecdsa
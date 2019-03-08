from samson.utilities.bytes import Bytes
from samson.encoding.general import bytes_to_der_sequence
from samson.encoding.pkcs8.pkcs8_eddsa_private_key import PKCS8EdDSAPrivateKey
from samson.encoding.x509.x509_eddsa_subject_public_key import X509EdDSASubjectPublicKey
from samson.utilities.ecc import EDCURVE_OID_LOOKUP
from pyasn1.type.univ import ObjectIdentifier, SequenceOf, Sequence
from pyasn1.codec.der import encoder

class X509EdDSAPublicKey(object):

    @staticmethod
    def check(buffer: bytes):
        items = bytes_to_der_sequence(buffer)
        return not PKCS8EdDSAPrivateKey.check(buffer) and len(items) == 2 and str(items[0][0])[:7] == '1.3.101'


    @staticmethod
    def encode(eddsa_key: object):
        alg_id = SequenceOf()
        alg_id.setComponentByPosition(0, ObjectIdentifier([int(item) for item in eddsa_key.curve.oid.split('.')]))

        seq = Sequence()
        seq.setComponentByPosition(0, alg_id)
        seq.setComponentByPosition(1, X509EdDSASubjectPublicKey.encode(eddsa_key))

        encoded = encoder.encode(seq)
        return encoded


    @staticmethod
    def decode(buffer: bytes):
        from samson.public_key.eddsa import EdDSA
        items = bytes_to_der_sequence(buffer)

        pub_point = Bytes(int(items[1]))

        curve_oid = str(items[0][0])
        curve = EDCURVE_OID_LOOKUP[curve_oid]

        eddsa = EdDSA(curve=curve)
        eddsa.A = eddsa.decode_point(pub_point)

        return eddsa

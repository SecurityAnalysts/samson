from samson.publickey.dsa import DSA
from copy import deepcopy
import hashlib
import unittest

# Test values and Known Answers
p, q, g = (89884656743115801690508003283032491320041051484130708380666508310605797591517657358448008016999203132296409109102891732381220932613670902301632476397501213820805847702280695479500940353078645163835996628341628828734609016397792501661682873394045725954243200605294871617235478335283698125903031997252753894013, 1207753555331593152985388036246139579485647958891, 5685459514059326809802874748014957316613560771138779799702167979852700053970957043705475419576800042124393749290154460175165016805439205742686078247106048259784394071586242286134792733247049365228417141823234012958591708840401400841693876682668942266225335842678094931739699394533691980318928257007905664651)
x, y = (25699150469538346273151504617195356896428318293, 87776125859689842027622448321257490281265790877998817249106298815115428969131775305386159545084670793191253582533101771837559797201510474157521867255147636248371470086721784879086813365664064382328859209285425076675844776906158328001899804552410472894735495394660855543401958332363658604533641691539985334580)
k = 707729718173049907897274687372338676901147366291
H = lambda msg: msg
message = int.from_bytes(b'\xf7\xff\x9e\x8b{\xb2\xe0\x9bp\x93Z]x^\x0c\xc5\xd9\xd0\xab\xf0', byteorder='big')
sig = (503181762231277455297502611450705228583240869840, 1148561876858258037434302178106550418252606972216)


class DSATestCase(unittest.TestCase):
    def setUp(self):
        dsa = DSA()
        dsa.p, dsa.q, dsa.g = p, q, g
        dsa.x, dsa.y = x, y

        self.dsa = dsa

    def test_dsa_sign(self):
        self.assertEqual(self.dsa.sign(H, message, k), sig)


    def test_dsa_verify(self):
        self.assertTrue(self.dsa.verify(H, message, sig))

    
    def test_k_derivation(self):
        messageB = int.from_bytes(hashlib.sha1(b'hiyabois').digest(), byteorder='big')
        sig_genB = self.dsa.sign(H, messageB, k)
        found_k = self.dsa.derive_k_from_sigs(message, sig, messageB, sig_genB)
        self.assertEqual(found_k, k)


    def test_x_derivation(self):
        n_dsa = deepcopy(self.dsa)
        n_dsa.x = 0
        n_dsa.derive_x_from_k(H, message, k, sig)
        self.assertEqual(n_dsa.x, x)
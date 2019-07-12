from samson.public_key.dsa import DSA
from samson.utilities.bytes import Bytes
from samson.encoding.pem import RFC1423_ALGOS
from samson.encoding.general import PKIEncoding
from samson.math.general import is_prime
import hashlib
import unittest


# openssl dsaparam -out dsaparam.pem 2048
# openssl gendsa -out test_dsa.pem dsaparam.pem
# openssl dsa -in test_dsa.pem -text
# openssl dsa -in test_dsa.pem -pubout -text
# openssl dsa -pubin -in test_dsa.pub -pubout -text


TEST_PRIV = b"""-----BEGIN DSA PRIVATE KEY-----
MIIDVgIBAAKCAQEAr9QOzmLmfkEjvB4xt3dBnyGLSKrLpp1WAVkZeElygI+CkbR8
h4fTuaUHuCFX70w/q7egnu5TwG/DZGPcThg6FKe8i6mRDwnD5y6s/Lu3Niojhrrv
CUxs3yJJYvyjrPwKdtMkeVkoiTZeFEeWBXhrgxF6rEWkJBKloZNG32NXqW9gcpfy
ecJ4v0yffuZWjftU0nO+3Yo1VQsGiY0fA8mFfYXNGXCbLENF8jclW7QpuKdcHXkB
deKofZRj+6nV/duLTWL6hOPqqEBc34B4ApeGfFAissN5Juf0Nzku3KIkp23hHZtW
pH0cHz4JpASDg3Y3grhcDy0mjuWt9iyYo2YuIwIhAJD4vs9Y2Oo+I7PRFFouK6Wz
CtO44JKlADo4c4poFGFbAoIBAFgxG8YaNzWyFf1sJuMbBZ1Pq6SOfZ+7A8bH1QRw
0d3DnT8fIkDy4uwmYKtq2lDxyGd+HyJcvzVVttuphfgMo6DevT8DpicKAmGA7y//
0NPCAt1eHx5aYIELxZGfhjdManb6N8hhUmhzzJ1JqqrKj4P60/JZwzYlIfntkIpP
gsXKuAOW3Wf/3s55dnguNwrRHD525xi9qisBXaUBKLViKmEH0lVjEN+RmB2fEjt1
C6xJx4CKQd7hZrBneXz8zLpZc5pCaEStcYpc411IZXQTl3SwMiA7IdlYTN1okXQB
oPal453z1cov8exg3erfs2OkWBH/JLMFssICuGPAVJ7CesACggEBAIU5+UpNOO6r
fvNzveNGnirqEzYTa2w0uEWEun4d/t0jhxDI34vSO6zA5oFwaZ4BFsuxTVzVAKF5
oSaKw2G3qsQ4QLr89VO/QHkbnrRLvkCa1cPZbY4eqPGzMlQsLTrBCb1zwH8Gbpx+
gcSVAwEyOdotoS8VWtURJNI/JaiTQN5ueZtrtKc4rJRg/oHvxgDrDEaqAuAakbr2
03+ZLCimsXVGDpVYoUu+i1su7P9ksLuVJE08ugcmVmZTSJURnao54AzOiVxQE3dH
hg6B3Jd661aatPJNRXyYBFTR5XHH8wclAjxbdMTqru/d8Ig6zAzNZulCbbBydawh
tZSAKpT1c+QCIGfUX0ksNEYbIsoy+Xt1caTltO3zbXuiMOA6bR4E/j8J
-----END DSA PRIVATE KEY-----"""

TEST_PUB = b"""-----BEGIN PUBLIC KEY-----
MIIDRzCCAjkGByqGSM44BAEwggIsAoIBAQCv1A7OYuZ+QSO8HjG3d0GfIYtIqsum
nVYBWRl4SXKAj4KRtHyHh9O5pQe4IVfvTD+rt6Ce7lPAb8NkY9xOGDoUp7yLqZEP
CcPnLqz8u7c2KiOGuu8JTGzfIkli/KOs/Ap20yR5WSiJNl4UR5YFeGuDEXqsRaQk
EqWhk0bfY1epb2Byl/J5wni/TJ9+5laN+1TSc77dijVVCwaJjR8DyYV9hc0ZcJss
Q0XyNyVbtCm4p1wdeQF14qh9lGP7qdX924tNYvqE4+qoQFzfgHgCl4Z8UCKyw3km
5/Q3OS7coiSnbeEdm1akfRwfPgmkBIODdjeCuFwPLSaO5a32LJijZi4jAiEAkPi+
z1jY6j4js9EUWi4rpbMK07jgkqUAOjhzimgUYVsCggEAWDEbxho3NbIV/Wwm4xsF
nU+rpI59n7sDxsfVBHDR3cOdPx8iQPLi7CZgq2raUPHIZ34fIly/NVW226mF+Ayj
oN69PwOmJwoCYYDvL//Q08IC3V4fHlpggQvFkZ+GN0xqdvo3yGFSaHPMnUmqqsqP
g/rT8lnDNiUh+e2Qik+Cxcq4A5bdZ//eznl2eC43CtEcPnbnGL2qKwFdpQEotWIq
YQfSVWMQ35GYHZ8SO3ULrEnHgIpB3uFmsGd5fPzMullzmkJoRK1xilzjXUhldBOX
dLAyIDsh2VhM3WiRdAGg9qXjnfPVyi/x7GDd6t+zY6RYEf8kswWywgK4Y8BUnsJ6
wAOCAQYAAoIBAQCFOflKTTjuq37zc73jRp4q6hM2E2tsNLhFhLp+Hf7dI4cQyN+L
0juswOaBcGmeARbLsU1c1QCheaEmisNht6rEOEC6/PVTv0B5G560S75AmtXD2W2O
HqjxszJULC06wQm9c8B/Bm6cfoHElQMBMjnaLaEvFVrVESTSPyWok0Debnmba7Sn
OKyUYP6B78YA6wxGqgLgGpG69tN/mSwoprF1Rg6VWKFLvotbLuz/ZLC7lSRNPLoH
JlZmU0iVEZ2qOeAMzolcUBN3R4YOgdyXeutWmrTyTUV8mARU0eVxx/MHJQI8W3TE
6q7v3fCIOswMzWbpQm2wcnWsIbWUgCqU9XPk
-----END PUBLIC KEY-----"""


# ssh-keygen -t dsa -f test_dsa_ssh
# ssh-keygen -e -f test_dsa_ssh
TEST_SSH_PRIV = b"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABsQAAAAdzc2gtZH
NzAAAAgQCyDpXjyCzOzkg/goozbmbeMyeLq+fbI5Wih6hQ5Y3KNHC5D0XQXkIAIcK8kgtU
qxP0aczjPsNn5ug8E8xA9VVzlCe5CoazZUhzGNy4Sd711PzzfIZwtAfafRwhkeDqQQPvJA
SDaTSUW/D2rDWcY6MoV/Ib+aQrYPXI6zziEw+5EwAAABUAsTJsICjVdb9E1qNxD5n0oWiB
baUAAACAAd3qkYA/F2X5rGQOqhD3qXESNCw8mHx36hPrGk0Hg4kPAarpseCUvQAD6ZWeGp
TKWuv78goAF8lLhZTa97w85QZ8Vh4sMPunPhKt6y/jireH7lXzk+sYxLnX6GmLHbyityPO
oV6e7mdVwisQMTN4lgLo1kUF/2jnliA6dTWZKGUAAACAJqYEump51X9nOoD/X/2266ViY2
kwzDb51TNK+H0Xx/EDDo1NbIWsnw99fOnXjJWGXzAt4zxEXY5P/bZfM/9OXJ5CV8D3E8Lp
uaQW7ySicRDpdWZIP6+2NkY4HJhj0pn33rur1tsriLr0NyjBGpXFPksM/XEdux1vOBrpcR
6pbMgAAAHoxd+XqsXfl6oAAAAHc3NoLWRzcwAAAIEAsg6V48gszs5IP4KKM25m3jMni6vn
2yOVooeoUOWNyjRwuQ9F0F5CACHCvJILVKsT9GnM4z7DZ+boPBPMQPVVc5QnuQqGs2VIcx
jcuEne9dT883yGcLQH2n0cIZHg6kED7yQEg2k0lFvw9qw1nGOjKFfyG/mkK2D1yOs84hMP
uRMAAAAVALEybCAo1XW/RNajcQ+Z9KFogW2lAAAAgAHd6pGAPxdl+axkDqoQ96lxEjQsPJ
h8d+oT6xpNB4OJDwGq6bHglL0AA+mVnhqUylrr+/IKABfJS4WU2ve8POUGfFYeLDD7pz4S
resv44q3h+5V85PrGMS51+hpix28orcjzqFenu5nVcIrEDEzeJYC6NZFBf9o55YgOnU1mS
hlAAAAgCamBLpqedV/ZzqA/1/9tuulYmNpMMw2+dUzSvh9F8fxAw6NTWyFrJ8PfXzp14yV
hl8wLeM8RF2OT/22XzP/TlyeQlfA9xPC6bmkFu8konEQ6XVmSD+vtjZGOByYY9KZ9967q9
bbK4i69DcowRqVxT5LDP1xHbsdbzga6XEeqWzIAAAAFEcWAvQWXa3f8yu1ehaK9Vnb+EqT
AAAAEWRvbmFsZEBEb25hbGQtTUJQAQI=
-----END OPENSSH PRIVATE KEY-----"""


TEST_SSH_PUB = b"ssh-dss AAAAB3NzaC1kc3MAAACBALIOlePILM7OSD+CijNuZt4zJ4ur59sjlaKHqFDljco0cLkPRdBeQgAhwrySC1SrE/RpzOM+w2fm6DwTzED1VXOUJ7kKhrNlSHMY3LhJ3vXU/PN8hnC0B9p9HCGR4OpBA+8kBINpNJRb8PasNZxjoyhX8hv5pCtg9cjrPOITD7kTAAAAFQCxMmwgKNV1v0TWo3EPmfShaIFtpQAAAIAB3eqRgD8XZfmsZA6qEPepcRI0LDyYfHfqE+saTQeDiQ8Bqumx4JS9AAPplZ4alMpa6/vyCgAXyUuFlNr3vDzlBnxWHiww+6c+Eq3rL+OKt4fuVfOT6xjEudfoaYsdvKK3I86hXp7uZ1XCKxAxM3iWAujWRQX/aOeWIDp1NZkoZQAAAIAmpgS6annVf2c6gP9f/bbrpWJjaTDMNvnVM0r4fRfH8QMOjU1shayfD3186deMlYZfMC3jPERdjk/9tl8z/05cnkJXwPcTwum5pBbvJKJxEOl1Zkg/r7Y2RjgcmGPSmffeu6vW2yuIuvQ3KMEalcU+Swz9cR27HW84GulxHqlsyA== nohost@localhost"

TEST_SSH2_PUB = b"""---- BEGIN SSH2 PUBLIC KEY ----
Comment: "1024-bit DSA, converted by nohost@localhost from OpenSSH"
AAAAB3NzaC1kc3MAAACBAIAAAAAAAAAAieGFUhig59rDgTb/r6cu2nhZ8hceJeZerGmMFw
JXiwfcKhB22iQcdsYtN02Diepa7/0yJqBTDMVl879rUJKROevqwE9Iw8hK+3ltYeWk+aj9
qBKrWUlCMsfStN61CqGO6eEyv6haxDdNf5CRq8PQFe/IcaWERxuxAAAAFQD09H8FeUslYX
S7pumzlqdwflY8WwAAAIBZWMnTiYsiSxJnLAuY4Gxg35I8uLyZnRGUWP71OLj6QEbI21MD
nbYgwJTJ+gd+84m1MipVmUanGQP5kPH34OAl4tf3z0lK/xoEcPW2TDa2JaCX8WUf53UyNV
b+ALNgjIh4koeEgOmQQb5gGmIWbKaJS91BpwVOyJ91a6n8lTAikQAAAIB/LGGoOyuL/zra
hx7LuyMWF/ruvSxiky4FPA2KorGG0xjY32k1GPQTw5818Itybr4CLB2jsw8oo6SHPVdSvZ
SWmPi/r70ltxQCIDstoJqaGE/0xD5S8W4T9IO3kbNr9boPEdQ8paf+CNZfVU4CTYgxjCQe
vlSTJVvZVKoQFKC4Lw==
---- END SSH2 PUBLIC KEY ----"""


TEST_SSH2_PUB_NO_CMT = b"""---- BEGIN SSH2 PUBLIC KEY ----
AAAAB3NzaC1kc3MAAACBAIAAAAAAAAAAieGFUhig59rDgTb/r6cu2nhZ8hceJeZerGmMFw
JXiwfcKhB22iQcdsYtN02Diepa7/0yJqBTDMVl879rUJKROevqwE9Iw8hK+3ltYeWk+aj9
qBKrWUlCMsfStN61CqGO6eEyv6haxDdNf5CRq8PQFe/IcaWERxuxAAAAFQD09H8FeUslYX
S7pumzlqdwflY8WwAAAIBZWMnTiYsiSxJnLAuY4Gxg35I8uLyZnRGUWP71OLj6QEbI21MD
nbYgwJTJ+gd+84m1MipVmUanGQP5kPH34OAl4tf3z0lK/xoEcPW2TDa2JaCX8WUf53UyNV
b+ALNgjIh4koeEgOmQQb5gGmIWbKaJS91BpwVOyJ91a6n8lTAikQAAAIB/LGGoOyuL/zra
hx7LuyMWF/ruvSxiky4FPA2KorGG0xjY32k1GPQTw5818Itybr4CLB2jsw8oo6SHPVdSvZ
SWmPi/r70ltxQCIDstoJqaGE/0xD5S8W4T9IO3kbNr9boPEdQ8paf+CNZfVU4CTYgxjCQe
vlSTJVvZVKoQFKC4Lw==
---- END SSH2 PUBLIC KEY ----"""

# Generated using ssh-keygen and OpenSSL
# ssh-keygen -t dsa -N 'super secret passphrase' -f test_dsa_key -m PEM
# openssl dsa -aes192 -in test_dsa_key -text
# openssl dsa -aes256 -in test_dsa_key -text
# openssl dsa -des -in test_dsa_key -text
# openssl dsa -des3 -in test_dsa_key -text

PEM_PASSPHRASE = b"super secret passphrase"

TEST_PEM_DEC = b"""-----BEGIN DSA PRIVATE KEY-----
MIIBugIBAAKBgQDHngE0HhdDu3LTU/405rxhvVh8dl397TVeuc8WC8DEnzDXx+OY
RQSXDcQuU8vzAeCLaDjsHhS7wFWcfrWH0vlOyZXFLYsM5Qz+3oalxL9rrUspBYIi
3Yc73zGgRoNlHWsmCP3VuxFePZAG6mt/mYnzTxcnIoBnT6vuZAd4/Y5z9QIVAIYt
zW+l0wkMoIUPlOW/EJ0j3ivBAoGABRgyc5mbtlcqRc47R36CcV+6BvX0p9hH8Kwn
E6nxxPlOrTJ+h/xDLzYRnO5V2WfI52KtRahjEMl4yh5CJu+qq9VC2K6FMxMTSakH
bUxPJXj80i10L5WygbSXy0ZhuMR48+x71QFBtadeS/T+S5Jr5yJMU67nWCyxxH87
QWFdvFUCgYBoJToQycvDq0/yRqJYkn/dghmIIL/aHTlgDcZ99ShVuLI93JLsdeB0
d8ndksVuPp8ihvOixVir0xSeJU2yrw1RCIKL06Wt0abYtcCgGC4wAppOifSMk0Xf
LJNps8iFIAVmxHYEbUj9hYx3z+3+svNjfA5N+G4nYgi++WHNB2JuwAIUYHrNRMMT
loOdXmS1PY65gIgki24=
-----END DSA PRIVATE KEY-----"""


TEST_PEM_AES_128_ENC = b"""-----BEGIN DSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2B9284EDD25B215F7747517707E8326D

UndDJGFb/JFwLRubS1bQ4UdwxVy9SkzVwLsFjaqMC1jIbvpQQR56aGCVX7ZU6HHe
+y6gIN7R9llhWb8Jm/sSu0zWEc7L5x5Qj6qEVFH9usJ57IHr3SITgBrKD4d/AtrG
SyOHn8wusq2WKh//aF7WWgrcVv39Ew1Y4Br+KfB9O8TlZhf6fIDRGI/vOluccM/F
26jPzFGXMof/AFynrOQcqHVtCmdes1JtIxvfLYIVbGi+mC0Hvfd8JgQjYMmlxXyK
ZFrZbubjKpNTjnUo77JJ5EzP9fnciIA9/RvHTalL5Ox6bM5hjAUX9ohYc4cL2B10
kA9D6KprzCfecEyhQXOffR8od88DlpSrmMhXwbbWR+68Fsz6AUxOd9MGnckWiGYz
xa2BGE3EzC4R/FygcM4+c5mDlbebMPCRayD3CgdqBWVzB9HJK45uUDz9nQee74yy
Yzrna7I2KrnuirXoGBxiwnNL7b6StCGI4NSbU1evDZ0aKpR7mVQtvekFm+rBHaAd
qaXwrAQccSXjJFzFzcVEhsHEqaYJdOZckGiUcSzC5szGYBsF9BYBn0DF/OKK3t+b
YXoS3wf1KTGoNu4V1e3rPw==
-----END DSA PRIVATE KEY-----"""


TEST_PEM_AES_192_ENC = b"""-----BEGIN DSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-192-CBC,FAE20370CDB461ECA9ACEB9BBABF71E0

Yn3Zk2t5VD4ZciOlapMK+GioEg7Jf8Ckw+wC2F4RWmKOGJqNRtjrVqAtyxPR+hWM
xBax4KqW3LD5wWHUUL6lsQEs9LOzZ0PoIyZqXvSGkVZGMwhY0aRaFwdbb5j0pa+T
KMEmlkeISE+0Ti0OowoAknisiIYn3gk6OdaFJsLphxb0J99Ra119VNlh+penG2NY
4s6m6DlhckCSYm2xwBqJIQNXIYSY9PApGkFQhBrneWfOfynBF++vBNvxw+0anhgj
Dllxe3+KhwDecYvBH9ohL728eoL+NZSYkVaSYaRh9PIz82h8nRMcauiu6URBF6Ct
W+ceAscBz+CU2m6St04L6Mh1XQnlAV9kGQN2l4puKNIq7sWl8ldiA22l0l4DGiAj
cTF0KQoVMtxZv1FM1Psp6UBd2WO1bytuyq5TbketXHvLX28r6VHHl6fnrtmwnBTm
/FIkcwhKuDGOZzgdated+TQY+jxGvVDQJuQyWZ+eiO/478cSca8p4ynfkp/NC6/4
Uh3wR/MVE9XiJrMs8LlPbi0hxGqYuNZwN4uE37qc85pl/iDbDKwroY+S7jYZf6Jq
3LS+g7Obf/MBdw1zuglzag==
-----END DSA PRIVATE KEY-----"""


TEST_PEM_AES_256_ENC = b"""-----BEGIN DSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-256-CBC,DB3428E8CA39E58CD9EF75BE23557C23

lY/WwGbFxE5ZEZx1ZOqEGuOW6N/iTSgMC3zXxMCdyEfIDBLKw5Qbcez/OszZXgof
FcbHoY3KI6CSDLuNdLh64oQC6BqYrdsWgtUMDeUushASYrICeYJSq0dDywBFgpO+
p8UUVvUE0T5nMgaUMUNNkUB1qqbSgtoWa2ZaF7nON04tL+byLt1SK0rBw6zG3DtB
CNYofQmwpwbJQbCaxa90uq90NVG1EDupsK10eeS/TEtcGnIY28qU7z3BVyR9Hbsc
Noccf8qIqZXzT3i0c2wF4B+/OAYn177L+ZxLFKym7WsZP1fnYGSyRT91asR8Up2q
OkDgvMQoMa5GEcEdgx5Pw7WGBHPWyXd0e77SGgJbiGZfMivdVY4t9HVZnaW8KXK1
l5pLFpAh3ysrnNyNorGJlrCP9dE8W/1O2jrME9JyJtRPirZfA5vNQIx29sF4IQAc
8GPxK5C86yCtDKiXIp2fy16UybWOt7O0y6cRhyKs0p6Dg4Gv8RxQVqqOSKi2as28
ZVZpw2dLFVcX5Hp+EfAX9N9STUsfjBFck77SU/vA2eZhJS/vHI4IyoDuRix0x5eA
52/8RRDnrubWfP49kmNxkw==
-----END DSA PRIVATE KEY-----"""


TEST_PEM_DES_ENC = b"""-----BEGIN DSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-CBC,160DA53675A873B4

0FPgOgyus98i/UKSXNIh+H+tGvnKXKLZ+hn11QEIGWe5trYEihLJ1HktaotbtZcp
Dn3F/p9Pxokf4IGww+fiRItg1TCi+99U8Q8LwG+BuTEcAQKuo+SjDNmACHlFXtuG
+kHNJBnnr0dj5P+K1atb7zssvaZ/Yvb/mBRzJ/m+mS4lcCrWA0/wi6xeglxN+Jrk
wA39UaqfmQ7AGIqmP2WFp3dfswh+6ndva6Ajrw4C7xoO6OUZgoHk2WK4wVW2a53d
VmbdUyIjfohUQ/AeHHpnFt4N1x13K+StU0NXvpNiRbx+PmCLP9ITS+N1QGEEu77M
Q5k0zkAB/rRrCESsXQ5kwbYyk9wuv58RVDmencdY4rAQbopzzmegveT4cvqdFjMK
AhC8gMg2IgLg94VXUisAmwpJd2l5rLf5XjCrq3JhCMldt0jEZ+Mr7jPRtxhPDbH+
dWbAWVmAz/PjnloAkI8Iz2hChd6K0rRTysvS0q5uLVFXKbk+mCXvzhjfnj3T+Fwx
8G7X88tKJClkwpY+yFsROaPS3wHOFPewZpBB2Z+xSCgCIX7TVGz0twq+2cqasX9s
dJW8Z3Wgr9MUNVDV+sa6hA==
-----END DSA PRIVATE KEY-----"""


TEST_PEM_DES3_ENC = b"""-----BEGIN DSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,EF0656428C0FB402

kgFYYNtmg55/LutnArhEsMVBL37GvUL0QSlQsA6soAewohjXqOiB8w6mYQzterHT
Ox2ZPyWKVtXDLXR1YhHYr2931n/bp48QNhh0s0mRObjl1z6/nhVmth5kQ8o015tY
uXp6mRQW+aomgYsX05HrGxHMKIs9qfbKAwy9of4kY+fIzYSitPqiH7yHCq79fvO2
H/HB1rbswV1SrsaKLPDypB9IXs/NCWZU+1YMFnM3iLtcTQjIRNYM5hQIDhj9ULDA
DW66jTt2einwpSPwNFUjUeqHPSolyhpPqMjXl6IqSk8mudKUQ7isIEHcAkOoegeG
YKVggt4NOyL1+ZGavsPjTqRuI421nvFLaLZxq/UmvTQmgYQwHQQcrmYVbi5OdUDy
PzxPh3LM3azqDGSqrHpe0umHFVx1K34Jsu1Ficj/OXD6lsDNecVn9RaoU2nlSHPu
nUnPagC4NrDaANf6yo7TdirdLhvejMnsjB2RfJQYekqzU6HDg68mKavOTPzPANhW
hVUiRnlk7iqjDUNJDEvFL/u/50bgxUptd7yW+koK9BsxvDxq8SIm53MHHTJy+686
kRRBxzk5SiQAsSmYzHEsZQ==
-----END DSA PRIVATE KEY-----"""


# ssh-keygen -t dsa -f ssh0
# ssh-keygen -t dsa -f ssh1
# ssh-keygen -t dsa -f ssh2 -N '260c3c0e7b4b4284'
# ssh-keygen -t dsa -f ssh3 -N '5a69e515d27282ce'

TEST_OPENSSH0 = (b"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABsgAAAAdzc2gtZH
NzAAAAgQD/KfuUU+KrHErm32byq/csYh0VPIFCv9wouPTvSDTAx9V/Kc8pMAGjdolzwVVW
h8E9O1E3f1LyedKt5TUIgOK+57d/Jr9lB7n/VBhe6evJSuR/rG0Mlb2mNG+uuF8GoHl1kU
QETh3SAGIgDz2DU0oEF2w/B7RpExXFGwc+31nKFQAAABUAhloSLjRVEkYPkbAxb4rNu4yd
xwcAAACAaNABo+jQT5bPiZ4wqZAVQG9t6GBBcX4tUS54/A/fL0gtU/VRYU5GAjuvwjNwDQ
XWD55SHkLrX//9oHBjz3blEY3ItMAQ/YRUtpP0iVUGSfztI40L9kG7/oAlFRTNVaRXAVlo
mcP34s74o1LhB2X/zTD37Kn2c7SlpyWy7L81QREAAACBAKCNrl+VGHGCo+7Q7ie07ul95g
+sUJxES7P/G4foDAQ3Tt6gI3OcUinDnBlp2OJVW9euaJaQgfUKwY4Q/dR8MzqFnE5BsPOm
M4HOgJpTkNAxyKTV3UKfojwzf85lW1D1r+8ohRp62x0Diisjn0NGccoXz3Vmx337j+r8NL
fDOi6AAAAB6CXknNUl5JzVAAAAB3NzaC1kc3MAAACBAP8p+5RT4qscSubfZvKr9yxiHRU8
gUK/3Ci49O9INMDH1X8pzykwAaN2iXPBVVaHwT07UTd/UvJ50q3lNQiA4r7nt38mv2UHuf
9UGF7p68lK5H+sbQyVvaY0b664XwageXWRRAROHdIAYiAPPYNTSgQXbD8HtGkTFcUbBz7f
WcoVAAAAFQCGWhIuNFUSRg+RsDFvis27jJ3HBwAAAIBo0AGj6NBPls+JnjCpkBVAb23oYE
Fxfi1RLnj8D98vSC1T9VFhTkYCO6/CM3ANBdYPnlIeQutf//2gcGPPduURjci0wBD9hFS2
k/SJVQZJ/O0jjQv2Qbv+gCUVFM1VpFcBWWiZw/fizvijUuEHZf/NMPfsqfZztKWnJbLsvz
VBEQAAAIEAoI2uX5UYcYKj7tDuJ7Tu6X3mD6xQnERLs/8bh+gMBDdO3qAjc5xSKcOcGWnY
4lVb165olpCB9QrBjhD91HwzOoWcTkGw86Yzgc6AmlOQ0DHIpNXdQp+iPDN/zmVbUPWv7y
iFGnrbHQOKKyOfQ0ZxyhfPdWbHffuP6vw0t8M6LoAAAAAUZWE0uRGCDl0bt2yYKJpImo6T
We4AAAARZG9uYWxkQERvbmFsZC1NQlAB
-----END OPENSSH PRIVATE KEY-----""", None)


TEST_OPENSSH1 = (b"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABswAAAAdzc2gtZH
NzAAAAgQD4F1uASoEHqNuQ9TMerG1KWBCHH7JJaQNR/145Eni+FL3voI8NwXxwRjavJ0w+
NBJNhojB8LhxbcQQyf0WHXKDueBpPAU9AGxXUzfUTgRdH+/ftaUbx48T9xh3Zwn65ftSUo
3PvY7yKQni7+GE4XZcZ5Kixd0wH8nnHNK5sG6MowAAABUA1gnsm2SRhVF4pWTJbvhxlzNJ
jHsAAACBAOeu56FlTzxVtBoQyqM3cyV2HbEt7eB38PTGO5HEk9YBCH8jRUWIIqYCvlRgbj
tv1fj053XGDXjf/x33A5m40ttTgpx/rH/cB3k7EdhJU/GL5idIF7576FIiaP6DpaJavt82
EEzSnlLosnFPt8wM9UzTGWmfdZLBzL02fgHwTCRMAAAAgQDxMc52ye9AA5j81W1A17IZnA
pJYik2VTU5zrzcy9UfXMeU0m35u0ELLkuUy//y5ik9Km2zr5B42VwhJFqXRCP02S/MhV4P
D0L15WIkAJ6vXomr/mYFfz1VZ2YsdlQqZGN1NiqDy089mJAgjePlieVApy2e/S9/XN+YMZ
bnxzvrfwAAAegYvTYDGL02AwAAAAdzc2gtZHNzAAAAgQD4F1uASoEHqNuQ9TMerG1KWBCH
H7JJaQNR/145Eni+FL3voI8NwXxwRjavJ0w+NBJNhojB8LhxbcQQyf0WHXKDueBpPAU9AG
xXUzfUTgRdH+/ftaUbx48T9xh3Zwn65ftSUo3PvY7yKQni7+GE4XZcZ5Kixd0wH8nnHNK5
sG6MowAAABUA1gnsm2SRhVF4pWTJbvhxlzNJjHsAAACBAOeu56FlTzxVtBoQyqM3cyV2Hb
Et7eB38PTGO5HEk9YBCH8jRUWIIqYCvlRgbjtv1fj053XGDXjf/x33A5m40ttTgpx/rH/c
B3k7EdhJU/GL5idIF7576FIiaP6DpaJavt82EEzSnlLosnFPt8wM9UzTGWmfdZLBzL02fg
HwTCRMAAAAgQDxMc52ye9AA5j81W1A17IZnApJYik2VTU5zrzcy9UfXMeU0m35u0ELLkuU
y//y5ik9Km2zr5B42VwhJFqXRCP02S/MhV4PD0L15WIkAJ6vXomr/mYFfz1VZ2YsdlQqZG
N1NiqDy089mJAgjePlieVApy2e/S9/XN+YMZbnxzvrfwAAABQD6uMh8acewxv3u9pyCsVx
scan7gAAABFkb25hbGRARG9uYWxkLU1CUA==
-----END OPENSSH PRIVATE KEY-----""", None)


TEST_OPENSSH2 = (b"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABAJyS5PAW
k7R6X7CScJoiXaAAAAEAAAAAEAAAGxAAAAB3NzaC1kc3MAAACBAIKB0KYlV9VmU6V03key
uNVPx3HL75y+08d1beJM0iEJxVIzrDR1K6NlOfRLtlhYcPAJ/YwEekuj0OE7V688UV+M9w
16VrXYjNzXVBd4MXPvQPGmVulGl47Y4z/cut9BgxALbJgxzXvOjZ0RlWyALwg/z5l5MIST
LJg99t1L2pi1AAAAFQCv9KrE0J9a1L7kOTO91woN8otszwAAAIByld2qwLF+fWRds1hJv1
lR5K8YLvVg69Zi8yUVY3HJTQWzShVXY3l6arvD5B/zacd5dQRMhTL29LHqH/mAq90k6vqB
6F9819TJnLdwU0gYsJDczHLuhnINIKj4VVEvlRvixrXV0Nkpv5NcmORQEz12coFd73pAuH
lgyu7WzaLshQAAAIBzkkdcnoFgKNcSREbfbfc2h5gjmdYysgVTeO1ST0WjsYW55C2FO9AF
A5D+z1CfWF0Pp1o0oIq1CaEXwmhqWPtb01HErb77inAIRf5dBzUhVVQHAmvruqnzDNRAPG
X9SeooV+eeO6fXixOcJs6Dqsv8+N0V4E+tc3sV4mp27UEi4gAAAfDmH4FQuV/gTkwMECmf
FI4GuWuu2mpP7zG/cjTk1NdoOOCzftH6d4ptrh8J4kp+ZIgn1Sc0F5DhnmVtdMsdAO9YmK
MeiYRWryE7rxQ8vbj25RjqU3Jnm/2w57H1KI9FqmH9jDhgrPE9grthQvPRyGZA+wdrFNxc
yb/pcqDZwyKlkuy5DRWzG3a0EKW0xhq48W70iHof9qEvxR5+ZTrKsAB+X8RLvFVWjgPbUt
t1GxZByIG+6Of/scG4ncawWxrx/xwztYx8U6/wOqiK7CLaZYlXtHx0KoPrkrTvrZTyzqwO
tbOwo7v9m4/KfKOeveBkepIowIG6uuCgp88WX/RLR37NdiYnxy0sUcFYDBxEWKaYjHxjTd
nczGiPMnyirVIweQn5jbVVW+YZnkFum/E9CdIQk0Tw563y7NN1iPHYz5maVUcjJMPbOFcW
c7LFDNieFaW84+2lZXjGFNMGoprSDcfwdaStXR4JN5h6YmZxCXaGG7JtPvBLgawn16iqMt
VjucPhzGKIjG0mDYvWEu7Qgr08Ji48E9YUYh59XfKDPerBHvAM7LdmTCDdVy72Tiob7HNG
mm05zeqPs9Qrc4uwVrBegjUozlg8MxiPnJfwqOFOJdNHJJ5ZmNqQijZyfR2IHdpipcbfLj
7LLH/7y1ipPRdq
-----END OPENSSH PRIVATE KEY-----""", b'260c3c0e7b4b4284')


TEST_OPENSSH3 = (b"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABDuHy/02U
54Pm85g1cch5HYAAAAEAAAAAEAAAGyAAAAB3NzaC1kc3MAAACBAPjR3XzfIFemcIy+8a5k
5rO6DXj+I9vLz0YlWXXF/5xu0P+i98HmViliS99bIw8BgMDhBBPJWPFdzXjwwl26/Cd0LP
DKa/TbbvnwkS2xAKPrJkTB28dNIihXOyFwfEFewM7oiCSiwMuEg5A3m4nb3ACQ6eiT40mZ
xORcqfFjC06HAAAAFQCGXCavYYbSA2G0iPcGZO7z7JGhbwAAAIEAx897RhPmmli+ofkwO1
Xf7cArahzyxf62dc2KHl+C6OL/+mgkreH9hdfCI5BXu9Ey0hxvn67T+A+/NX8sG2QPtY9u
4Av77EmWe+A7yEPszdUwJpQo+4PZMByaYAzD4DhCiU9iY7YOyQfsFsiNRXE0VtjHWRaRYQ
6/4u1cj1Iq6/8AAACAXvDtdB2M3YuoqCDAQZ/e1bs0tAh3niy16j4rIjXOIPUB7CbX/EQu
HPzPX/Jc0GTfQ8Jfm+cOoK+cZ1+oSRqy6Cl6y3pHFZM2coxMP6gtQzLtMsEFvrcjpd+D8O
MuSzZD/A9oiT/xY5WY6HxBcDL7WwyL9cXLqh+8Zg7jDshn23gAAAHwAX88Noch3Lx0Zsp7
ZSjTaaZlqAnzzhFLPj59Wj9vto2yB2gMwNwK6M2ca/NnCR+8LOsSe+Gb3yayk4GTTN9jND
fcVwYx7gEVJOKHcShZWPyweny3BqXeK78521uBPPmiOO0XZSgSdrLBrANU87q0PqAkRKd1
0V8AVdMtLz5XVLsaPZh0+wHZAEq+9SxT7+oxQcC1s7XQINfGuCukkQeudndd/6wdNcIfit
/I0ZNMA04QvUFuBLvpTBSpI6iSoy0iusgikC/ayToGiQvynalSRPabybj9fWSg1bnUzfHb
J6akWLIrD4KAoUyiLG+Z/Ze920f+q39dpYcqOqI199QwcjaHl4ofUVXUwqJqKdHQq5WoHJ
/AXWJTTwAu7blSt24Hl3Wt/Jq8NgHw6FxmR4VdbcH8X7bhBkV7nTR373r1ZjBHrQbso+Ut
4iGuMR7yUBsmASRSlgM/CRu8aFPwHIjUBP08Yc0o8P8U/249iiaoboDtB/O1/VVU9IK2e1
3gklaiDEsgQEc76RGAlQCBttdY2Lb4o+en6Lr3vKzAXOXbgqLjAgOtfUQXT9NLdlnDBqNt
gq/9OAsoCjVkI1EOYe3QZqqfnVjhQ3G2Yt1K45xls+raNZTvB2lau5yRWySsQTrHYVU/vr
Yx2xpB3JmtceH7WA==
-----END OPENSSH PRIVATE KEY-----""", b'5a69e515d27282ce')


# openssl dsaparam -out dsaparam.pem 2048
# openssl gendsa -out dsaprivkey.pem dsaparam.pem
# openssl req -new -x509 -key dsaprivkey.pem -out dsacert.pem

TEST_X509_CERT = b"""-----BEGIN CERTIFICATE-----
MIIEwDCCBGagAwIBAgIJAKC/wMj8NpOXMAsGCWCGSAFlAwQDAjBCMQswCQYDVQQG
EwJVUzEVMBMGA1UEBwwMRGVmYXVsdCBDaXR5MRwwGgYDVQQKDBNEZWZhdWx0IENv
bXBhbnkgTHRkMB4XDTE5MDMwNTE4MTQ0NloXDTE5MDQwNDE4MTQ0NlowQjELMAkG
A1UEBhMCVVMxFTATBgNVBAcMDERlZmF1bHQgQ2l0eTEcMBoGA1UECgwTRGVmYXVs
dCBDb21wYW55IEx0ZDCCA0gwggI6BgcqhkjOOAQBMIICLQKCAQEA6JHgRNvtyIt3
CsSJevJPcA68CtPpeWrc6/JyRi1cHiXBj29AlnQvfdOUhv5BF3WiVlslRN+lUW3Z
4EhX6QvOPPamARmHzTsz31zlpLUwWUg5KU7k14SEbj1P16CW1KGWHCnQCUZxkOQz
K4Q1BGNstAzFuoudNekFTt3RXWbZaDWivw6SllzsuuNeQgb/RsWPMJTq94FKCFfQ
CnCiRy/FGMoqLkWAI2kd4DH92y7MD9A/EJaT/3APD4ECpE/iLnUGM15xDi8tQTg/
Ulh3cSkTa67ZWss9QLlFhRJGMTEwzyMA/fAn2/0xIHXi3qx5oHlo5ZsKalBKnh+B
aZ+DyBFivQIhAJ/haKf3RXGG2XUIdsgk15eEZYa6/E9l9NKRHO7Yhzm/AoIBAQC7
FZpTJBx7POupT4Q9fFmq9kw1BDhSO2bewmT/yXAZVUNjQspkZlaW0SyUYdpDc5GY
wUSoWwMjeIA+8wEElx5USGKX4qA3OdNxOny32UKhYBTuHnJiVEQNgg/oQW4XQqO9
Ylq0Qau2t16J9/0UyU85so+vWFpq6XZEsvEWEUTQHal8z9v0LOnH5yK9ttThCSFD
XnwaKVyfuvRH8FtyVRoqPUITsjhKX/5tWQI/meY7X04a8YuBbZj/SkDeSRUKJN7d
AEP8R05klpAHgxvZoaliSsR/ajSz5X22s2sPQbdHrDYInAVFO3CjSaBQq/HZ5+Vb
G23dp0WwNvsCZ8z8e8D2A4IBBgACggEBAMAFfi+DOkfKFpEs8P7j46j99FkJ7+pM
K/zH9dRM6zt7Czs2zQaOI8kRcPmDOGlPQq1RanJLyyNnzrXFpSyCgyeXHpUY1lmI
uuPFzeLQvXzDTlXoSNMTaW+cldbG786S6WNjP82S66VCuaytkAU99IIA9u9ocnxl
b2Oymzyh2xa+JhhTXXh4nnym96SsbEFzn8hSFNQq8yvEnOQK5lG9GnzUQkjptzaY
AdNCBHZYk0jI/VoKSFezKH/2rSUKz0YmXq3OqPyTwgd9xDLzh/t2/P9/WCZ3Dovi
E/k4Ry86I6tAjR6HdMSH10rbGHzfOv3pO4TXuaJ+jgx87F71cSw1I8yjUzBRMB0G
A1UdDgQWBBSIJ3YGkFpmT42XrVevtdmhykZIODAfBgNVHSMEGDAWgBSIJ3YGkFpm
T42XrVevtdmhykZIODAPBgNVHRMBAf8EBTADAQH/MAsGCWCGSAFlAwQDAgNHADBE
AiAijo2RgnFWCP1skUVPeViJ0r9G1H9J2au+HvKfaU6+DAIgXMhVJ+YLZ/hZ2Zgy
Z5PasqL55QAoywAUbUAIIM4KVu8=
-----END CERTIFICATE-----"""


TEST_X509 = b"""-----BEGIN PUBLIC KEY-----
MIIDRjCCAjkGByqGSM44BAEwggIsAoIBAQDHR3J1kWfnV+DTOm4qLyZD+J9vgkSI
YpECcun4FocXssRC89BxupEHrXJEp0Hqn07dQMeBX9hSI01XgKjvirQLLFL32gAm
EPw+J8lzWVdZX44HESzpJCParhnQn1UowYd117uopghjjzAg+wddVeje55h1EXE+
RXNr8nhnb+6/J3o8b+KunoARgdPFPaYX0HYlQWpniuunsSarI+iVi6T/oaQC8Wys
vzNC+nSfBsJ+wmVubWa03gVMu2TL+WHiTGrJ6PfBQHpWWSn2K7UMzNx3V6eUX6/3
VDaKxhdxkYpUwXmGXHC3ttXFgU4dtRjvlHgrbLMDBcSCOozU6qsMvDdZAiEAvbiW
E5RFqcgyOP9ovOdZZzPhXbN6Gpj8i7eJhyk5sksCggEAC5j/icethUyrpaFk6Vax
hydInQGB0yoz+CYj0VudQghOkghtub4n3fu+kf6scWCF0IIyMOmdCwCji6J0XVys
wSj0q5wVP8Da3AmWKJLv9UQCDihZyfS6EkSJziCi/vPtBnfGUZBuBxiis82u5r+b
3uaiKEumCsF9yX4kX0NsHq092jQuLrDF25dW5s/j/gncMx3KQfQrcGzZNYYvYQg0
s88keiMEUUZfDWQjUOU/oRSpHsgqK4JBuzc3esNaOmhv8r+UQmumBYneBehBiftK
ji5C/uNTiZTO7tNqw7u4b/pGygOfpjRdiREqzPtxV+WqnqBl23T+T0WoIMyPitBe
tgOCAQUAAoIBAEzvpmDtF2r50yGMBIsaa4lOB+npA3q3RvztIw141uoV0cqCW4Go
XwCGgYid+CIp3BgCBs3FjYOwhFtwmchhu3KCEPUKSMreSyJe2fzBxwK0GAnYu+ip
TTw+KLqmV91L/1ck0Nm3hL6GaPdTW3W3G1gxEVt/zPy/uExeCoGrUtsC8ZVWWkU9
DQVQrO0LDNqxSCxMricYhCqSzRLUORsGTF0QzC32fDtX6mHFaQ/vafY00h/SUrVS
EU5Xh6mQlUOsXomosk8rXNvSZK/8vet4avv4eztLIfAu+BIs8zOfW7GmyU101QV3
YIgggyXMWwPnJANoeF5onLdgeUqToLs4KB8=
-----END PUBLIC KEY-----"""


TEST_PKCS8 = b"""-----BEGIN PRIVATE KEY-----
MIICZAIBADCCAjkGByqGSM44BAEwggIsAoIBAQDHR3J1kWfnV+DTOm4qLyZD+J9v
gkSIYpECcun4FocXssRC89BxupEHrXJEp0Hqn07dQMeBX9hSI01XgKjvirQLLFL3
2gAmEPw+J8lzWVdZX44HESzpJCParhnQn1UowYd117uopghjjzAg+wddVeje55h1
EXE+RXNr8nhnb+6/J3o8b+KunoARgdPFPaYX0HYlQWpniuunsSarI+iVi6T/oaQC
8WysvzNC+nSfBsJ+wmVubWa03gVMu2TL+WHiTGrJ6PfBQHpWWSn2K7UMzNx3V6eU
X6/3VDaKxhdxkYpUwXmGXHC3ttXFgU4dtRjvlHgrbLMDBcSCOozU6qsMvDdZAiEA
vbiWE5RFqcgyOP9ovOdZZzPhXbN6Gpj8i7eJhyk5sksCggEAC5j/icethUyrpaFk
6VaxhydInQGB0yoz+CYj0VudQghOkghtub4n3fu+kf6scWCF0IIyMOmdCwCji6J0
XVyswSj0q5wVP8Da3AmWKJLv9UQCDihZyfS6EkSJziCi/vPtBnfGUZBuBxiis82u
5r+b3uaiKEumCsF9yX4kX0NsHq092jQuLrDF25dW5s/j/gncMx3KQfQrcGzZNYYv
YQg0s88keiMEUUZfDWQjUOU/oRSpHsgqK4JBuzc3esNaOmhv8r+UQmumBYneBehB
iftKji5C/uNTiZTO7tNqw7u4b/pGygOfpjRdiREqzPtxV+WqnqBl23T+T0WoIMyP
itBetgQiAiAgEaSC7Ra5RV4ejvV6K8ccuBuhafTnZ2/qMIIlTxGscg==
-----END PRIVATE KEY-----"""



# Test values and Known Answers
p, q, g = (89884656743115801690508003283032491320041051484130708380666508310605797591517657358448008016999203132296409109102891732381220932613670902301632476397501213820805847702280695479500940353078645163835996628341628828734609016397792501661682873394045725954243200605294871617235478335283698125903031997252753894013, 1207753555331593152985388036246139579485647958891, 5685459514059326809802874748014957316613560771138779799702167979852700053970957043705475419576800042124393749290154460175165016805439205742686078247106048259784394071586242286134792733247049365228417141823234012958591708840401400841693876682668942266225335842678094931739699394533691980318928257007905664651)
x, y = (25699150469538346273151504617195356896428318293, 87776125859689842027622448321257490281265790877998817249106298815115428969131775305386159545084670793191253582533101771837559797201510474157521867255147636248371470086721784879086813365664064382328859209285425076675844776906158328001899804552410472894735495394660855543401958332363658604533641691539985334580)
k = 707729718173049907897274687372338676901147366291
# H = lambda msg: Bytes(msg)
message = int.from_bytes(b'\xf7\xff\x9e\x8b{\xb2\xe0\x9bp\x93Z]x^\x0c\xc5\xd9\xd0\xab\xf0', byteorder='big')
sig = (503181762231277455297502611450705228583240869840, 1148561876858258037434302178106550418252606972216)


class DSATestCase(unittest.TestCase):
    def hash(self, m):
        return Bytes(m)


    def setUp(self):
        dsa = DSA(self)
        dsa.p, dsa.q, dsa.g = p, q, g
        dsa.x, dsa.y = x, y

        self.dsa = dsa


    def test_dsa_sign(self):
        self.assertEqual(self.dsa.sign(message, k), sig)


    def test_dsa_verify(self):
        self.assertTrue(self.dsa.verify(message, sig))


    def test_k_derivation(self):
        messageB = int.from_bytes(hashlib.sha1(b'deadbeef').digest(), byteorder='big')
        sig_genB = self.dsa.sign(messageB, k)
        found_k = self.dsa.derive_k_from_sigs(message, sig, messageB, sig_genB)
        self.assertEqual(found_k, k)


    def test_x_derivation(self):
        self.dsa.x = 0
        self.dsa.x = self.dsa.derive_x_from_k(message, k, sig)
        self.assertEqual(self.dsa.x, x)



    def test_der_encode(self):
        for _ in range(20):
            dsa = DSA(None)

            should_pem_encode = Bytes.random(1).int() & 1

            der_bytes = dsa.export_private_key(should_pem_encode)
            recovered_dsa = DSA.import_key(der_bytes)

            self.assertEqual((dsa.p, dsa.q, dsa.g, dsa.x), (recovered_dsa.p, recovered_dsa.q, recovered_dsa.g, recovered_dsa.x))



    def test_import_export_private(self):
        dsa = DSA.import_key(TEST_PRIV)
        der_bytes = dsa.export_private_key(encoding=PKIEncoding.PKCS1)
        new_dsa = DSA.import_key(der_bytes)

        self.assertEqual((dsa.p, dsa.q, dsa.g, dsa.x), (new_dsa.p, new_dsa.q, new_dsa.g, new_dsa.x))
        self.assertEqual(der_bytes.replace(b'\n', b''), TEST_PRIV.replace(b'\n', b''))


    def test_import_export_public(self):
        dsa_pub  = DSA.import_key(TEST_PUB)
        dsa_priv = DSA.import_key(TEST_PRIV)

        der_bytes = dsa_pub.export_public_key()
        new_pub  = DSA.import_key(der_bytes)

        self.assertEqual((dsa_pub.p, dsa_pub.q, dsa_pub.g, dsa_pub.y), (dsa_priv.p, dsa_priv.q, dsa_priv.g, dsa_priv.y))
        self.assertEqual((new_pub.p, new_pub.q, new_pub.g, new_pub.y), (dsa_priv.p, dsa_priv.q, dsa_priv.g, dsa_priv.y))
        self.assertEqual(der_bytes.replace(b'\n', b''), TEST_PUB.replace(b'\n', b''))


    def _run_import_pem_enc(self, enc_priv):
        with self.assertRaises(ValueError):
            DSA.import_key(enc_priv)

        enc_dsa = DSA.import_key(enc_priv, PEM_PASSPHRASE)
        dec_dsa = DSA.import_key(TEST_PEM_DEC)
        self.assertEqual((enc_dsa.p, enc_dsa.q, enc_dsa.g, enc_dsa.y), (dec_dsa.p, dec_dsa.q, dec_dsa.g, dec_dsa.y))


    def test_import_enc_aes_128(self):
        self._run_import_pem_enc(TEST_PEM_AES_128_ENC)

    def test_import_enc_aes_192(self):
        self._run_import_pem_enc(TEST_PEM_AES_192_ENC)

    def test_import_enc_aes_256(self):
        self._run_import_pem_enc(TEST_PEM_AES_256_ENC)

    def test_import_enc_des(self):
        self._run_import_pem_enc(TEST_PEM_DES_ENC)

    def test_import_enc_des3(self):
        self._run_import_pem_enc(TEST_PEM_DES3_ENC)


    def test_import_enc_gauntlet(self):
        supported_algos = RFC1423_ALGOS.keys()
        for algo in supported_algos:
            for _ in range(10):
                dsa = DSA(None)
                key = Bytes.random(Bytes.random(1).int() + 1)
                enc_pem = dsa.export_private_key(encryption=algo, passphrase=key)
                dec_dsa = DSA.import_key(enc_pem, key)

                self.assertEqual((dsa.p, dsa.q, dsa.g, dsa.y), (dec_dsa.p, dec_dsa.q, dec_dsa.g, dec_dsa.y))



    def test_import_ssh(self):
        dsa_pub = DSA.import_key(TEST_SSH_PUB)
        dsa_ssh2_pub = DSA.import_key(TEST_SSH2_PUB)
        self.assertEqual(dsa_ssh2_pub.p, 89884656743115795391714060562757515397425322659982333453951503557945186260897603074467021329267150667179270601498386514202185870349356296751727808353958732563710461587745543679948630665057517430779539542454135056582551841462788758130134369220761262066732236795930452718468922387238066961216943830683854773169)
        self.assertEqual(dsa_ssh2_pub.q, 1398446195032410252040217410173702390108694920283)
        self.assertEqual(dsa_ssh2_pub.g, 62741477437088172631393589185350035491867729832629398027831312004924312513744633269784278916027520183601208756530710011458232054971579879048852582591127008356159595963890332524237209902067360056459538632225446131921069339325466545201845714001580950381286256953162223728420823439838953735559776779136624763537)
        self.assertEqual(dsa_ssh2_pub.y, 89304173996622136803697185034716185066873574928118988908946173912972803079394854332431645751271541413754929474728944725753979110082470431256515341756380336480154766674026631800266177718504673102950377953224324965826950742525966269191766953261195015149626105144609044917769140962813589211397528346030252275759)

        self.assertEqual(dsa_pub.export_public_key(encoding=PKIEncoding.OpenSSH).replace(b'\n', b''), TEST_SSH_PUB.replace(b'\n', b''))
        self.assertEqual(dsa_ssh2_pub.export_public_key(encoding=PKIEncoding.SSH2).replace(b'\n', b''), TEST_SSH2_PUB_NO_CMT.replace(b'\n', b''))




    def test_import_openssh(self):
        for key, passphrase in [TEST_OPENSSH0, TEST_OPENSSH1, TEST_OPENSSH2, TEST_OPENSSH3]:
            if passphrase:
                with self.assertRaises(ValueError):
                    DSA.import_key(key)

            dsa = DSA.import_key(key, passphrase=passphrase)
            self.assertEqual(dsa.y, pow(dsa.g, dsa.x, dsa.p))
            self.assertLess(dsa.x, dsa.q)
            self.assertTrue(is_prime(dsa.p))
            self.assertTrue(is_prime(dsa.q))


    def test_openssh_gauntlet(self):
        num_runs = 6
        num_enc = num_runs // 3
        for i in range(num_runs):
            dsa = DSA()
            passphrase = None
            if i < num_enc:
                passphrase = Bytes.random(Bytes.random(1).int())

            priv        = dsa.export_private_key(encoding=PKIEncoding.OpenSSH, encryption=b'aes256-ctr', passphrase=passphrase)
            pub_openssh = dsa.export_public_key(encoding=PKIEncoding.OpenSSH)
            pub_ssh2    = dsa.export_public_key(encoding=PKIEncoding.SSH2)

            new_priv = DSA.import_key(priv, passphrase=passphrase)
            new_pub_openssh = DSA.import_key(pub_openssh)
            new_pub_ssh2 = DSA.import_key(pub_ssh2)

            self.assertEqual((new_priv.p, new_priv.q, new_priv.g, new_priv.x, new_priv.y), (dsa.p, dsa.q, dsa.g, dsa.x, dsa.y))
            self.assertEqual((new_pub_openssh.p, new_pub_openssh.q, new_pub_openssh.g, new_pub_openssh.y), (dsa.p, dsa.q, dsa.g, dsa.y))
            self.assertEqual((new_pub_ssh2.p, new_pub_ssh2.q, new_pub_ssh2.g, new_pub_ssh2.y), (dsa.p, dsa.q, dsa.g, dsa.y))



    def test_import_x509_cert(self):
        from subprocess import check_call

        dsa = DSA.import_key(TEST_X509_CERT)
        self.assertEqual((dsa.p, dsa.g, dsa.q, dsa.y), (29359220913751863604833831088508876963959576721066909433519185036122477565374345588645677334816946188725816961177204244286505667536622105129598507183951785847666297741964587922835869455415298445486396512029003492626158257370280004326543237064383812164746423606113267826295308133990946323580302454465345797049077152416869329147414209308332896482919061867497361253158575203307930086395945671596985821884739975618473349063589147702701417308590844611877379910082427573989264746106041860056146871940266394204099594386922044495056768254911353270662373963136495992338504405482333007257545963351600037578526790722778333012669,
23617215781717641617429030982788739308839883025449676002514899895971013739086266219589723087302420802424432207620364342437971077989552668403584830683906724391694927580364566457156558011018261388697901249029874930648117138478782550791538431508968833018975912941761229968196143318555594523977722616137832961924618915535030137041338198568072260683639968253057837316412361105204516582498206127844801532328000057962921798556755270135686136557052844725364560067801871204656590639599770100822180375741326530962498960449714141471757291650594845562147405665000737639213678390322684570440873644788001074612485922815394182840566,
72316005824286355284515606116521507078131054279099309238012872750090099833279,
24240463209582537180230652876781005346105451481524832869285984323585717271952266150668568120092756048095155927490283408872722816120298365210328274832680857067760238236491656811005453081601169078682863189260743532281104198835666955889441439680555890529729382264203182689421640973361971708995350357645100803545925750964854486879395081362199184213078390000740834820889491748353899668574171396907246023123383900652626758107235645341361354392953201524187611449915208661545890873448519779973599548346076584621622740772374654418867730905962971963353521393562860224570461592873543620417563917397982610608266104949697794089932))

        cert = dsa.export_public_key(encoding=PKIEncoding.X509_CERT).decode()
        check_call([f'echo -n \"{cert}\" | openssl x509 -text'], shell=True)


    def test_import_x509(self):
        dsa = DSA.import_key(TEST_X509)

        self.assertEqual((dsa.p, dsa.g, dsa.q, dsa.y), (25156654569543985414899238193689924508406163996733174489974082279485784298259615078312117270875517452081148142482882127409907891315389306112842044598421568324172804398649625417052144684395648595674164312439029436011046483859099109529713573238085329837201232794908263951760737460683338600439958519628368407479843028851912335038765978072027596597451017985192662603371867400132542278066320060614404684783663289898993097885425646719965763286908299540676611841160699585919635210876616249583541461102295966295524254189355469624918949316273478759819356841971549391463773601064548533858835060059336170261107202630741418325849,
1464067577045645655375143295266294465391352713606947323839674420127263935401991055986768415789222071015377844403852155698560675585510192049794973165585031515800615865766677068871466314377865947723271318740878430952896495169876413577639812957830595776929594741532199588179263499170574700740537023478058969031100065858165371126405905453002355737133621632537561646102666739807557196395481785420842406093884097563624829696336146171932407089065073614901561094786562321514289895619979403001136947587622111199094928084942448189142508887136164695485649706278623026996621633039171222422679272596866936807032840596496611040950,
85813264031962452329373401337333701824848487531453606367854109906470224638539,
9712286955706100022811604874507345111332338638978311063297336318443333337479349689374531148134334992750346213506440574687981538071159286479156749524358478616320344780059579593809426016346876129770072081613374384693195409942430842023701769800775705864140737571472174089847631629279838627170998282064620707695252573588223989860999020733985975545341764015539031567806330590570442373859389524374479312480587627656162922527567591167400987223808760759117951603018608731240160159634986003508016675933382814261442735449383526698087070885013832731482992134754748968190468953686616518117966613453900136206593287313995215677471))

        self.assertEqual(dsa.export_public_key(encoding=PKIEncoding.X509).replace(b'\n', b''), TEST_X509.replace(b'\n', b''))



    def test_import_pkcs8(self):
        dsa = DSA.import_key(TEST_PKCS8)
        self.assertEqual((dsa.p, dsa.g, dsa.q, dsa.y), (25156654569543985414899238193689924508406163996733174489974082279485784298259615078312117270875517452081148142482882127409907891315389306112842044598421568324172804398649625417052144684395648595674164312439029436011046483859099109529713573238085329837201232794908263951760737460683338600439958519628368407479843028851912335038765978072027596597451017985192662603371867400132542278066320060614404684783663289898993097885425646719965763286908299540676611841160699585919635210876616249583541461102295966295524254189355469624918949316273478759819356841971549391463773601064548533858835060059336170261107202630741418325849,
1464067577045645655375143295266294465391352713606947323839674420127263935401991055986768415789222071015377844403852155698560675585510192049794973165585031515800615865766677068871466314377865947723271318740878430952896495169876413577639812957830595776929594741532199588179263499170574700740537023478058969031100065858165371126405905453002355737133621632537561646102666739807557196395481785420842406093884097563624829696336146171932407089065073614901561094786562321514289895619979403001136947587622111199094928084942448189142508887136164695485649706278623026996621633039171222422679272596866936807032840596496611040950,
85813264031962452329373401337333701824848487531453606367854109906470224638539,
9712286955706100022811604874507345111332338638978311063297336318443333337479349689374531148134334992750346213506440574687981538071159286479156749524358478616320344780059579593809426016346876129770072081613374384693195409942430842023701769800775705864140737571472174089847631629279838627170998282064620707695252573588223989860999020733985975545341764015539031567806330590570442373859389524374479312480587627656162922527567591167400987223808760759117951603018608731240160159634986003508016675933382814261442735449383526698087070885013832731482992134754748968190468953686616518117966613453900136206593287313995215677471))

        self.assertEqual(dsa.export_private_key(encoding=PKIEncoding.PKCS8).replace(b'\n', b''), TEST_PKCS8.replace(b'\n', b''))

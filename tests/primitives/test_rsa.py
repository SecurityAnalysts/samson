from samson.public_key.rsa import RSA
from samson.utilities.bytes import Bytes
from samson.utilities.pem import RFC1423_ALGOS
import unittest


TEST_PRIV = b"""-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQBUVwJ4kpnFlUTwpIA31fy+KFtcIU0mRp9/UkI3Y9AbMx0PfJ39
XphDWzYuCDh10QHhC/hio0ogzTjNaHQ3cLHuV85/BOQzVymuys3GYrmx4PQ48aaR
U4AB2cjzN03B2r8un7MWvmNrDSOT9RHFvHNzwWZlYjItw5ERY+M4uDvffZpiLIG5
7dGc0Wmcrowt7zJd4xPgcNdzP8fKleCxLvakMJVibh+jsZaBpuaygo62s0h8t7tY
NwCGsQjp6vnyClO49Eyf56t61UXXCzxfRwGQ7OnnFygk4FdH4cQxpmSra9L5FL9k
5NysBXXEk/UqSIc3+FdC+1KqRVXxRKuOYBcTAgMBAAECggEAPID7BdJtvB/ciCIK
1YOOwEAlYk+FkCrj6yvw0tmpBopBk8WbdZNx+ggqMxW0o1igV3kF5IUt/aAb2sfP
b6JKEyksu1Sf/PDPt1RIEMTsYF539Y3uJ51WXH2HOmv3PVWXB3SLvoowujB/0Hnk
GQ2baXRZ5+ttAgWlQWt+K0eHtEkLRVCeJ0AepBOGfCrrjkuayswFF4er5D+8jJZ+
oOsdxUNY6uMntJn2uK/kgWI29mBfkOqG8u4Y5W++F6c3Ye3izDQI1rkN4IFSUDMB
DLlLK5wPbTCayQkktEDiYj4Qb70ylmIWmNzZWM5b4VQ8ceyczT4t9W+fnbZtF9zT
Zc5M2QKBgQCoH3yQUjkWXR7yewd0TPmRbp/Ri7jf8uKzZGbtOtVWnFRolvnnNBma
CJIVQ6JC4H7bBVRMlKH60ybkj0aBWSYsR5MhkKi8CnXE3ErhKSrE3/3YEpPw5s8G
GL90h3ujPaRfUki8bAaA5QL8mwnJni5wDJX9Uxqo8lc6q1Qj4fkJnwKBgQCAbIRU
s76yTpPdz5JONV+gmxEOYGOBijMM308LCCHiuEj/yjp7rxGVct16kmPzYkAMNdtB
9Dpmoa6HTiDFXdJW26sS7EGjY9qQO9cMzGMOZc6Vi4bTdUJfiQBwe0FauDLp9Xl5
r5NUaX3/FeHkNIBVhvcFvfLVN6IT/HKpCZMmDQKBgQCJFyO7i1CBq+1QTIIHk7zt
mgc4F3bpJmU1YumLCC5uMYuivXmJzjISKGr2a/AkGGtYrT/QMmLi5MsSFMKpNsip
0rNm606sBtuBayCj+a2mW//h8UQxbAPkNMnpe5CVy+38zFwDSRMEh7mnwcR5Y0L6
m0izCND0cqgubwZtPBaWgQKBgDBismkHX+3mVSfZMRJuYZ0tT3vPLS59V0aeTDWn
1ryJGlflZat8Bm/8Wx33Udk9R0xSbk2nKunIOO2ZrhcuhjVbhlUW1pQs5wg4w4l6
6EdgbDlD3ISHRX6hK501kyYPCH/FkQMb97JyHJqjL/y/GyseMqvjKT7UOyi0kK7H
gL1xAoGAFizRvHqloxi3Pp+L9S1agxCaSDYcFoE73UCBAfWkHd1Ji/37Qa7bARiW
G8TIq6kR6CylPOz4UiGWbp5Fz0jKZMUROpUZo+g6OLxyJBaZtv9Tj2zF0Ek2w7+f
3eyhIl+K+rhJsKQJeZWrQhJjT+MjSGjMWRowPRpYM8p9gsMmQ+I=
-----END RSA PRIVATE KEY-----
"""


TEST_PUB = b"""-----BEGIN PUBLIC KEY-----
MIIBITANBgkqhkiG9w0BAQEFAAOCAQ4AMIIBCQKCAQBUVwJ4kpnFlUTwpIA31fy+
KFtcIU0mRp9/UkI3Y9AbMx0PfJ39XphDWzYuCDh10QHhC/hio0ogzTjNaHQ3cLHu
V85/BOQzVymuys3GYrmx4PQ48aaRU4AB2cjzN03B2r8un7MWvmNrDSOT9RHFvHNz
wWZlYjItw5ERY+M4uDvffZpiLIG57dGc0Wmcrowt7zJd4xPgcNdzP8fKleCxLvak
MJVibh+jsZaBpuaygo62s0h8t7tYNwCGsQjp6vnyClO49Eyf56t61UXXCzxfRwGQ
7OnnFygk4FdH4cQxpmSra9L5FL9k5NysBXXEk/UqSIc3+FdC+1KqRVXxRKuOYBcT
AgMBAAE=
-----END PUBLIC KEY-----"""


# ssh-keygen -t rsa -f test_rsa_ssh
# ssh-keygen -e -f test_rsa_ssh
TEST_SSH_PRIV = b"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn
NhAAAAAwEAAQAAAQEAyAB4rl+5x3Xhq6Hd0WSl9QS2kMNH5YIIa+dcy05Vi+APPuYhhnmu
LvpZbwspDw5zIiDdDS9WHY+gALJPM7L2Iff1Y4MU7bhyvKCOFJvMV6jYRoEbPD0TSqNUjU
KkZHF0xAJ1E42HbtyJbpOyZVa9YPIu5RLvMAtsHCxoU6kn+Y7Cl36P2lVKya6mIG7K6rbg
VtLsG7uAzL/RXQnQo8QtN5bh9XPrhsRI/s11TFnFgEkd7eOD3jN8e1/b1dajYy9usc8xgP
yl6L95yFQ8JoUZBdvO6UXee1ICQhs8GBhicBpUGWR+sTn09ePs57fhXCkZ6u3l9o5Ie/SD
orhsoKFyoQAAA8iPVCRPj1QkTwAAAAdzc2gtcnNhAAABAQDIAHiuX7nHdeGrod3RZKX1BL
aQw0flgghr51zLTlWL4A8+5iGGea4u+llvCykPDnMiIN0NL1Ydj6AAsk8zsvYh9/VjgxTt
uHK8oI4Um8xXqNhGgRs8PRNKo1SNQqRkcXTEAnUTjYdu3Iluk7JlVr1g8i7lEu8wC2wcLG
hTqSf5jsKXfo/aVUrJrqYgbsrqtuBW0uwbu4DMv9FdCdCjxC03luH1c+uGxEj+zXVMWcWA
SR3t44PeM3x7X9vV1qNjL26xzzGA/KXov3nIVDwmhRkF287pRd57UgJCGzwYGGJwGlQZZH
6xOfT14+znt+FcKRnq7eX2jkh79IOiuGygoXKhAAAAAwEAAQAAAQEAnIxR6hufrVLGG7QN
jnM7u7e+tz1Dr4/Cy8NDTRe5ukzdYhx8LWhdQQRQsKyJrPFgiVwz6rgcrfLYCPOJLyxroF
cYSpY18YUouiDqVZNFtW/CKh2wlcwwp4GFEzUQvFZaUXqi7XUgh1Q0dstBHjVw8stejYvu
kSq/qqXP23xSf/EtmmF14N8EbMlDBJaFLOjqoKJ0F84A0ZTCCQJomWCCv40UdAiTp1b6ZC
EV/BXppXvsl35w5JQhqsjXZBNHDu1UIneQ0qiwRepXGU4trkhawGoBkJQ/1SR8gv4taFnw
gQbQQxfDK/zgcqYnYIcCtQvPpzxwkGj50I6IbAKP7fRXqQAAAIBhCmb+qsBvTSu55H9t2e
26Yr6jIsNK9Dz2nK3+s5Ypo1z+qR9Ol2tqV4Eqylbl2N9m37MHMvPBqqJRRkZ//Cnv6rdH
btrdnN8/WUSyEZTn0fJ/Z/ym5xeOxWf7rXZ0x8shkmFx1MaoybLFo1vDInYkjXzIQEU/fE
t31K1ZZOOqSAAAAIEA8vlEXLZS2vq41VyjWSr2aN6/OhmitDUDP9DXkKRDCNIfMVh91YgE
hJ+fTohoRr8tQrBy2L/xSoTm9MPvSA6ZdR8Rb1fekdVt9E/OGJiI4zBzyxgZVGMNwrb/wH
Lzp9cv+iN9U1pRvxxvMOgH1ALWsWbAuf9qQ9zFwA6X1ybW86sAAACBANK5bhG2hkxB6WkD
n/Vwl8bhGbrresxqRpYXEXmE36aRH/UyQBiH2n9MaKirwAqHoYe5B0SrUD8+Jwxk13Yl5z
vq0G0fTHmWkG0Hg48TltvujewmQxWPlixSocs9dxZEXFY320z58dwVaIH020NlKqktZGCH
0Op+gORSv1w7lCbjAAAAEWRvbmFsZEBEb25hbGQtTUJQAQ==
-----END OPENSSH PRIVATE KEY-----"""


TEST_SSH_PUB = b"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDIAHiuX7nHdeGrod3RZKX1BLaQw0flgghr51zLTlWL4A8+5iGGea4u+llvCykPDnMiIN0NL1Ydj6AAsk8zsvYh9/VjgxTtuHK8oI4Um8xXqNhGgRs8PRNKo1SNQqRkcXTEAnUTjYdu3Iluk7JlVr1g8i7lEu8wC2wcLGhTqSf5jsKXfo/aVUrJrqYgbsrqtuBW0uwbu4DMv9FdCdCjxC03luH1c+uGxEj+zXVMWcWASR3t44PeM3x7X9vV1qNjL26xzzGA/KXov3nIVDwmhRkF287pRd57UgJCGzwYGGJwGlQZZH6xOfT14+znt+FcKRnq7eX2jkh79IOiuGygoXKh nohost@localhost"

TEST_SSH2_PUB = b"""---- BEGIN SSH2 PUBLIC KEY ----
Comment: "2048-bit RSA, converted by nohost@localhost from OpenSSH"
AAAAB3NzaC1yc2EAAAADAQABAAABAQDIAHiuX7nHdeGrod3RZKX1BLaQw0flgghr51zLTl
WL4A8+5iGGea4u+llvCykPDnMiIN0NL1Ydj6AAsk8zsvYh9/VjgxTtuHK8oI4Um8xXqNhG
gRs8PRNKo1SNQqRkcXTEAnUTjYdu3Iluk7JlVr1g8i7lEu8wC2wcLGhTqSf5jsKXfo/aVU
rJrqYgbsrqtuBW0uwbu4DMv9FdCdCjxC03luH1c+uGxEj+zXVMWcWASR3t44PeM3x7X9vV
1qNjL26xzzGA/KXov3nIVDwmhRkF287pRd57UgJCGzwYGGJwGlQZZH6xOfT14+znt+FcKR
nq7eX2jkh79IOiuGygoXKh
---- END SSH2 PUBLIC KEY ----"""


# Generated using ssh-keygen and OpenSSL
# ssh-keygen -t rsa -N 'super secret passphrase' -f test_rsa_key -m PEM
# openssl rsa -aes192 -in test_rsa_key -text
# openssl rsa -aes256 -in test_rsa_key -text
# openssl rsa -des -in test_rsa_key -text
# openssl rsa -des3 -in test_rsa_key -text

PEM_PASSPHRASE = b"super secret passphrase"

TEST_PEM_DEC = b"""-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA9tGc4zTrMLKECbMgkbXi5p+lOcL4QhXcV5LjMMARIqzv03I3
wDJPhqL9FNn4ZCQUjKfDbfaBXISLkjKtNj8jAnqWYnxgfsAgx1AhujN0rjINiUmN
V0cCeTunzfbVzTXKwyYS6rgZokC0LNous0I7RY1HZTJ8iKgZVdHKbDbGt1kJ9Eky
Gy/hmgpUFYFDOQEBRS+gpRIWEVSnhGybjwWW0apx3fbtin1nxWjZUh0KblsayNgF
XSkExg7Ny3dynTKVPXMIz6TqBYz2d1IooJN60WJQfSlGvP95oyyFH8OntSAVgXf1
2zJa0ldUD9D2Ce77mONn4nWrteNryMa4LNtFRQIDAQABAoIBAQCQKZiwYO1qcSqM
G9NPKGTSfbbdCRNGTkx33jTS+axIi6g84b7MhNZMdpDKCBJ8M1LJYQfWB6BBcK2x
A+aGA9SoEwAZoDogbon2wMgiYQGq6VNct9hVfQVl2EFIHP9+MAgxeeCctlFKou5a
MEoMrAfAtSdZZWa1zzGVHcdU852X4sU32x8LO1MwT2mMC5BiXXXU14w0KjNbBAGO
YzhmtpH2Z54epyge8JPeC5DNaOohcYL7BXKr/pI8i3VoioXYQaunQiYRoA66jmcN
STstuS/b44uGBNOqQQfxlWsoWoB2c6IpXDWrd61msbF80s0jRly2/B1sIu4gam56
HiVYeMbBAoGBAPvrHLsKW7Vdq6ardiiZXVA+SoqIGJTUMHpYFFxd5s0D+diBY8f6
hssi47l02dwPTJEMne6Zrmi5iz7h88L8mH3+q6poo5szCYRYacLEkjjhq8VOhObK
sepG3ZlM/G7wKmX0CWdFTOfxBs+KVzV6TqyJDDRxm2r83EP47WNCTE0RAoGBAPrR
WU6b9vrLuWXFqHGO2PivHaGDrPCrI4tCqcdLZYbVJkQvTAR2zlpa7MPxBRhhL5YE
XxL9HnNyY+mEhfbHmfNyPE7y0XK0YmJcHLMYripJu+lC9QSGSN0nqqpTPRS+KhEU
b05I+m+NyLVg6Wrq1kJHf0SPTKo4NHjsgHLTjUT1AoGALVHYs1VjtjcJwEwsT5V3
kg4CvvVI5s1dg0UBNLS35r4GXoq4dqt9QGIgcaax4sLl1VpdtyTymWh3wnJHthZX
IKOGInv8otkFp0d4j09pts3yZuZ/Rj3E0A67ou6UoyiVmA3U+z0eXsOfpAqRMc+1
A5kMFwsxGIgw4BGSMz8kFuECgYEAif2TfMQh5Wkf3vYX7iIBDRCK5Mlk5CPDsmJC
tfqtKLksDGdZEzup29waVtLLUtZlL8vH4tKPZkSQ43Cdo1+9O0qmE2lUAh9r4WF8
CKyTZYCbeYH0+0BF5iZkpsCU4kydKDht5EwSPD1tJxziTohUyLI9OqL8MsopVD4J
jSMGneECgYEAo6Nc2bk07mOASMy3egy6lUhqUI6qm4obd0oQ3IiztvU+/irfEyO4
DS3s4u8oCG8vYXqmuARgTVf3xmpI8Aer82UbSgJSzTA6a8l8iTx2cHhwxuO3kKlw
qe6ackLbeWhkxWbZPinj3+MHRY3c5uN7O+YA1OTD6T9XdDNJPqT5860=
-----END RSA PRIVATE KEY-----"""


TEST_PEM_AES_128_ENC = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,6C31F9B4A2413CC6889C3FDCDE20C22C

c5SAYW6C36T/IR2biLFQBt5rjDnVMZ9GEkkv+cLy7Z+PCMPwWvDYCW+H0dg49LR7
slt8cVjYKUvsWxKYsYV524OGVqaz/mJ7kj6d6ZILODBz5xfDiN2l+W1iBAUrQ8ct
Z7lgmUF2XYHtwFGEubHcxpVCD0Fwl+w+/KemjwQ/BovTYc1fTJzexHJmxTYYhbXw
vW0bN3TfNJ5Bsk8izZlH9lYGDnveccAQy1R+iEOyp07+0kuTpGOBQnAtKNskTUwr
W9umE5BeZf1GY/OkYXY3mKFYBgkMFv99WrPN22gAGpbP4eAxpTsqb9BUtU0idBEB
Fvq2eGZw/L+or9XdmIVGL++rEGZ6gODiSVWhdpJ1tTSMcdzYCkDSycSGOaTT6jqu
uH/c/RupRyULea5KisImhifSbB7IWT/YWo/LVupgXRZV2OXLwaj8XyiyTTvsgNSY
ehHlEdoOArgibTZQSQxZ7nMxD7ndnf8aNsa2YPfQoOLeK/rP02SYpysKCS6ewgsM
b3/DXrJE/gU2vXoNYROMx86WOBPk5/JHrweghJBaByHK1FmmmlIRKBx2vOETebmH
wwKIgm+jdUOOmYMY/hglNykqTX9bup5BtdZvmuxqDhoAVXCl8mrHtkKW/f5N4kDS
4ONbFDmhB6axlrtV5VxQyhjtcnNexbz9YPjDHojynW1s+nUWx3j/fO70sFFge8s6
D7WHO/MOjbw79GIsOfRTcV+uuJNTRVvRTX6+gPRRA0QbHFi7BiPBmtq93AhVa6Z5
fXvzhGUewMX/GnyJGgeU4nfBwyh29ZnAa+goeIOs/q7h2H8PYZFyQ8jQBXqB5xMN
EoS+pGcFVM3H1WGxYc04sgY01gZcgmbuXYMtbl4W8T21qbIolktxXVqxU6vifD4j
NnHi7BTZGSKwVXy8RS+RNSfCFxizz89InUVfZwziv50JKWU5VwlSKb6TDemLJEwt
bgyjQRlagCg9GwFqZe7813vQae9+PXZ6tDCjCn0DwPDFJrC8/CFQ5Wt31wWihaaX
oVj0Ds4o5FVoZ0TZ9Y7vawKeciU2UZkjWtraTclrQXEhDPPDYlFtd2X6P4xvbZo3
Q/AcsxPPBZiYZDnKVznO/uFbXfZ3pi749qirc21SBZH1iSZNXeM4JIasuWg81e9Z
lKOkCVxaq4do+Q2w4BqtLtMJQsRrWQypy29i+LGwaGcnSMYQo/rmDQuF0nsqy/8O
yF4ih2msc41UCMPT2xfYRFQfNswX+6czomD15LSS1ulbwpV2ARZ+CoelOCd1X6EJ
/Gkp5igWZQfIyI4u/5TnbjX4oXaRTNy0kbbBPZsM2VKVxRntEFq8zV/qO7aM2A/o
3L6hQ1vsc38JzX4cL0+/DoWWZ2zdn/Pbm5BVnmpLrDjfbjAixNZk5/P3cTbrg2W+
6sUdrIDKjVUyrq4k5Tpl1Bez/DJcu0riBdPA6foXWaAVb6VeSC5MhCypGrB9UvpX
vpynKRiClXMNVZs6h8ji/xTMK4RTg+e0gpyROcrux4pSC6C/crsQ6fd9B47QdCy7
U8/BS4zBl/Jyub8zoChmNUc5i+mzKHIFy41cnRhiGxAwHsLxP5o2f7r522wynUGa
-----END RSA PRIVATE KEY-----"""


TEST_PEM_AES_192_ENC = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-192-CBC,2256864A7896D06FD40F473D91884CB5

UMq/F2BWxgpIr6Xvp/JrZSEv5BvBnSSvzFLDfUPyVL5PgQZHX1QIXKYbJ/hB3nJp
IbTNAZsCas/nL9eKiZOIg6CkO2Alm/OMB45e/tsi2LFg054oD3xS/h4pXF5XKLpx
Fq2j05ctzo3D58PuHsR1vBNXsMioip3YAhaJW3GMc56g3JmCfgcBCIgVVeMAIKpp
q6M7APrBExccd/ws3+cwcNxOPuHclBYnehwh++dhT9Yvw2BuvKHj4NmLBgeLm+4z
njDZs5PUFUMkWZvY5186eZFu3PXk0kcs4nEYJ6WfX+vM5swiu5lC0YGK7Lij2324
mfQVhWpfbAX1gKupRoisIKtJkB/kf2MtU5TdJEHNxP1GEk/QHheskwzM1y6BC58L
JJ6n3n19xXtOOPM3UydXIK1UH/S2qRnNZc9opqC+ixU1lRqfzbFvn0KlfHuJ4jxk
oPYbM/tZm8uykvVsTKJz1h0I0IRvtrNZSA7ci8IV6b8+9/hLspZ3TzWasWhwCu53
ri3dhhEQS93nV4QM5m+2PdQoW1cshG2IiVJBGBh057HnJJaSca8e0lb8BCHERfGh
+5L/im+JhvdZJ3qj/55SBzr2fR/qQUfjL7uOmxUBV4GZ2b8l19r965PmxtpmstMf
ESfaI0AVQCSR7aaKO+RQRBoVulW+50Os/qdjC8CKLDUdubftf1p9tRt07C7r+6uz
Gz+K2nJri4xpVfFMS9pTfkSxHVviMj89+4a8E7a2DjoFW0+HK3u1eUbWah3kBl0X
EkJwOoXVydeyUoGcGUT1jZPbHl1tJ2urwcJ5GMA0m/5Xu4IA9HI7OMbvm0B2UZMZ
cGRGeiozSmIorv3LQoPGhwx+6Qoi0g5SA4chZrqSUNZgYvPTcVdbQP4eTxOFx8Fr
WTmTZv2CXpxeOCZxEnVWb8BakdEYwyxD+3FqDmLvaEW1dVDAwtlAQIO73Ulcgtt7
UJ4rgSKK7P0Qyi5kWWks92UmEUrqwq0UAz1czGGdUkcwa/F/lzgneEQlcYgHnpzP
czW3RPv+1CyVRmmlWQU+n0gOym5Z5R+Al3Q/rtJKoJtsbeuHWHR0RK4zZElU1VNd
mxJ2iHVn1FaLWAqGNyCNK9/WB4EGDQfzL0xoXc3yWXVzuNGCJ92HaVtHQ+dNiyS8
vd5J4Gevi/BFWT+/s0Vo6Iw/ygOlhB86ELs9Q/aUNechyjso7KIgO4Zh+O9gO+jZ
xKgl5Gt7KovdSsdWmk8pFEhznaZTwHi9uPz6uOs1TqvhbtUDloQOBPX3RcarNQXW
cU2UOSuPwxFdiw6hUmOSJJpdv1xORZa9Q2Aheup627uj8d80mG0HpyPOuVsumxm9
FIUfN/am94YL9P5qGFvscFSMKtW/W0o5mhZKTuAukgbbwCG1MgL61l6cg/SVEMTp
glV39RQVxXLqsd/xJi+g/UaSiYP7GOOzjyCS2+j1uOm0JnBD5XVbSZwf9B1WBdpn
fZlsu1m2CYLstTOH2hqNzVU6dUBnIEUQ5tr2707cVXXqdXkxFblavRKKZywLdxf4
kfHyfsVArbTtDFW8gs8iyWfwqcSz86uHoNTW6tGs57f4Thix8+xgSD+xdVBszPDS
-----END RSA PRIVATE KEY-----"""


TEST_PEM_AES_256_ENC = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-256-CBC,CFD06BF9EA82CCD1E643AD7AF22391D0

MT0nrqgcTAbYpP3iLpzXMVlKSeWxgyutH/nkzHewtHeQhpdBIziO7v7eDTM+3CWI
yXTTB7DXPlbYfnmwz2cF6X9bOWLMnvdsJ0Agmt9ADP2nKqpcVPgtP7gpaZ6rngCE
CDs4uFG44sEMKfhTcyUwXyfmuyq4ju/DN/aC6ABQH5PmI6Bli3+9PxcZxhRgzMR2
Ej8ON23Euc0TsO5SoBTbZWoYqbR9ng59q41iUYRjOiatgb1KzqrxcXujNMFG4G1g
y+OMKn2qmwWnQSyrHK3fljImaEjPOjF1G4RNYSH7qBKcC4tpbmqzM3J/sEd49uqx
6xlPNIA/xx/uAIHmnom74KajGM4cWQucOfxV5U6/Wh/QXJtIY/LcN3gG9YZ7imPJ
PisPDDV7Z5d1lflvHiInBDJy2JdleeeEBnHKRsELXODgXCyBjUSAL/V4qw8oB99a
LPRbhDthmRx/RLtubbYIKPp7gq2vl84dsEnQpWEdc1p6TMjKacjHt5wDG+LIzaVr
zZ3XXgmiQH033OtZVQytRY74teaQZ6yzU9iEKi9C5RjcVp1gO38RRR77NzYYhY3E
Q6TRCmIezip4rFGEkVGv+MFdecnAegYLY7j4vi63PvzNgVqFNXUCQwyMPeY2Rn5Q
c3CKIPMHcIVox8O5q3YsjYfFM3bVDSb4y7W2bFlX+r5C6rnHW8k8hB+lOi0cm0vQ
pWF9UR1+3KBBTj/yjlwH0F70HlrblsqaofrqwPmX1UYJITF/qSf5yn93RelLvHZ2
CCtXJ6Wdrs/k0dW8LWEFCXTWCAcNO68ey6fM2cOlLg/aSMuq+9CNICIO/X7XGDaL
I5xj4MZS3cvWsNXXjBqJP3JWq/0wKUjGAG+nJVa+plwuO597YdkXDAQ7QI+yISad
SZlgNa7lrEd4OlYOqk/tfHHn8l5wW+5UnI+M8KUB0zNSS6j29hI0JtKIylI0Lvsg
qIGTgSpYdu0FxOfQcBZNBxQES1gIwqtcnmSQUJ5dIQwcwnCXVKNg/LCyTa32HXZp
b1OuD3+CqcCC77hk+ish9WJoM3p1OjcNu90zwEVvVfuTcSbgZeXvo2ipWn/1sb60
Gkbddww1Y2kfEbpaeW85G43K5Vgdid6rtSycak2RLcH5rxE1As10J+wK6s0963+Q
an9s9BgC/KBOBmscFjO9q7kps5HyMZCzI2LPyDyj7gBOXF9OaiyiLM6Kgic0Ddly
BfWqzL5j62pM7O9aqw7l2zXg/AG7wcsfXprYZJHkHCJ3S6kmPVSfoN89bUo5fmAq
jVYUvI/0DeGuzQvx+zoneOZSJb9L5RbrDiXXR3tuECXqW/1bb2kaT46eF4a0nOSN
tXBgqjZ99jLY4oyuDQDl4wDSdN3WGqX1xJ19vQLoMP0hhBsOolvX3UjyxPuMpa+u
VAU2QPcMDxfy2S/4211WvodRigDkaIeBOkT28q+62aKaVWfnAB6Y25BD6n8KblF4
hgvTjuf97TNpSstrntOs3u62v9TtnCScQ1PPZZGQ5IY1SMrdmL9PhcRUplVNI2N8
odsdxovBZWIGa2DsWrlQIgK8wyYVscl4Oh9TZtziswLJNCE2eU0uJzouTAU1Jjt/
-----END RSA PRIVATE KEY-----"""


TEST_PEM_DES_ENC = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-CBC,0E0E35BFF36DCE88

IcSVzkFHsN2cPNnTEW8A4Oyhyt+MCcWGggOWUQexDAfYeRd093XBKisDqJHnNNSs
Gdp6IrY+aFhUXid9cbxk0i4nZGMl/G1d21YaFGLsgTfDW+V7bWJBAvK2GY1hxxA/
U619UcVXd6i6cd9EY/GiYz4aWBHL79nMcQsNFdyNcnHKGKrFHl1dFW6GROaHd21r
3xugx2BGuvcEHvJl3fg+HowIQ7b+AEtN5FInrAuRk41s2z0hvXfn8leakusNo5ay
zTAxjzdaEA8QOAqos+yh3ixdLYPeJ0LCUQWalqj8suRt6TaQkybwKVrWBh1sGyWg
D3yoTuNPMT6XxCaggO7uxaexR/DROO50VhCIEL07DCKoqvSOZX/Fg9fkisxlxzHk
0V+mrACMiCcDjstoxPrWg7kNArB+rGiZ3u94hsjUv3tG7qRsJaBIhK49bPPV/OaB
Q+qFesYT0/8/QX/kPAiR3c/sD0lcO1o6g+LCaXgVxiOzbhvn6fKOhmyes2990buN
27GPIBq9U86jf2slY0eyW4l5IC2W/ZfIJH70lDIkR7UcJZJlaTgxz7f2xUH+iQ2i
BJ0XlstzZFkDs1qR7B2MkuvLUasi1QgRjP4Kur+lNnIbooQav4NJlzivKysfKnur
m7bL2Og9p8ueeJ2+dvdskc/lc/RrhlyyR0OdDRcwv7H1Q8kykNAla31zaZ3w71js
MFuF86nljkGpdh3zN0vlJiaWZVHts5Y7ym6e9yJiIA5r0JCaS7ETKG5+oZeEQW4E
wzBCGGhIAcU4SeHIzr6g+OP/d5ml3PvjikK4+gRE1GW1ulIh8MoIPDpIcviuz7ZF
2UaDyfE6/o7rxWlUhFYW8fjbKjLG8sJ4faKiJLTSaEnZ+icRb9B7JFLhNk/57RzV
3zfrchLeF5JlN0GiqegsuA3SYiISOwRK4FLXC5v2IEtWApJPhsRKSnmLUcDldr8q
quaFHMxkfq5KTY66t0p/9pDkUlrZaSK3QZHMZd60c/fnHDCAylQkG+MYVo0JKOYO
3P0Eh9/V/QYAKCMeGL42GNO2wLZtjJHOyHTTkk+SRtti7xw50aJM+P2FyTGPdZIT
8/tdzEAir81pdi5ykkyPRyI5F81ErBdlUoUj+rKGAkPhUiSEkQ2RsA9vIfjyLd1N
1Y9VTgLfqnRDMw1NwF1ssGucIPQtjS+ffBRsJTaca/jI8jDZSawCESrxF4J2prAA
Icgec6FAi5yFzIclczGwTzEw/+jpHxccHnrmc3FgNaNzSCXFRBS108cZsxi94dFx
zIdt4iFOnDFAwbOy9pZie9qRV1OKULaeN6KOZYLIA0imAfVWrXq1M7Ia2dZEPGIW
M+NGs7cX4AFah+CiuniZYt82BgUESRfNVsD4ycqWpT62zFqtW32igJ9etLI99YHO
Yp+pMSKNB78+gXBoOdGH7AcFjz76U1zOP2sa9TaCZTojVPm+nTw/bDMJs9w5H0PR
qwdVQ23iERAdj5oQiA45AQ5+pDfV+hTFieAyvq743C8HIA6GNPmO2++Br34pSvwb
JW+5mP+vPtazOF4ipYJ+B/B7wdHdVwFWhL5s2UCDiAwZaiqxfzE5UkaEvUJj0Bcg
-----END RSA PRIVATE KEY-----"""


TEST_PEM_DES3_ENC = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,0BF4C53B0F1AE4B1

uRk4SdVx2ZN285xmliGpD7wsa7ZAfnMEKjRJ/5ccJywiYS13nrOErZP0UNl4vFLe
NEOt4GBNgZ/3KwvR7Da2jXUTagdTms/zSHUxCJhmBL3zqvySmxMbBO7EbWf0rBMv
poyN+TCbxoBuG6WIXzFe8T54FbLh+MPW6N0G3FI/M8FdozC0CV2pxZ1iXG2LK2ut
msh2hWhFX9ca+0VVed6Wmk1Lr77aky4DgP9xx3tjvgEEvmcLK9QHPOuqUJBszT6j
vjHpJCBnbcGOc6ig3eIWyE3hPciQyq4zG844O1/xOiV+cGxZB/XzJnGBX+RTbzjB
uME/WobgJYi9hADN1rP0mxI73k+nCpIgVWpbOF0hwfNb3b7Yvgc84Spl8+Mb0a61
hVpCsBA1eVWxHqkCdeGNL/jKofThtzyQ/KwZ0mWLzvz0uZ0p670yXewwFQdQ/T7F
mG1z9eu0ngtrdCkdga6gmwfvWHLcL98VG/Jl8ADMil1NNz+MN55Jh8S5X5Q7cdMv
gDHmVNo0oVk4IZTJ6DiWxvhBU+p6HyT3f1MfTT4S+iJLYHd/DWVso7wXLiwChsVW
0hxOqg82/lZ17gFpFSvRTQB53/qXAuDLgTQclFhu2SNwioRvT7/kiMIJIAzg6zSM
cBBC8DP9m0FQEF7qbRQhlRKGrW13bkvKaQlS+HwATSbvaFFORbJOThv8xN3gCEko
RylEBZgo6lpS38NEb4YHGIC3MJeuvmCt6B+FX98RJjjb0xEkbUToLA11dSzbtL+L
iE1K/QTaTcefPvQZWV8X7SQ0gCstEW0dmjBKWF0NadD8tJ3sBollsnbAz+EW5KWK
cSHK+l9P+EXYYoNZ22EiNJRd5V2FQJZ4GoNomDNhxMxhq20fqs3x8wSnAe77rHF5
73sRaGACOEYqGOgj4M/1mw7oPPz2lcQC3ia9uuCpTbso95cGvJLDlJCWTeALU39R
s2LcsMeMUY5sXNU6KhXCJ3yho+D7b2z50idVUlcxWyvgYKJJ1jkbQpsC2xSE6GYR
kdCG9jlyUnLTZFMqgys8CJhtBMMTVBt9PPXpj7u4/L+KWSKeza1SLuCbGzhcvTYE
DqsDQLJoD6NKgqeWkaSRXJHGiHdCbwWYk378RCyT2fc4e/A/ekIBcpGu1VSjKIUx
o67CaY+tWHhwFQC3SIki/y7lO3/Pconf1o4tMktlVzbDaXD6aaMP15cpmRKgL3eR
d9qBFVObDDAXjxuuaiuUPfcSlXiap++oDWhUDguNdOMZv5nZ2DFGXKoR8WFjedSM
b/XM5oZFGMnQEBzD5c73CC3Ux64hTKmo+Qu/Dp9uq8BmH3AiIEjEGs88sr3jGvMi
IE63nI+kiQHZ8dmMH6L3PHPrN+jmWV8UCjLiXgjuy/PkGxy5kd5rY99E1bp+vBmw
xd6mwhPC179R3zPtDKfKc2LMIcPkvGSfdu3a5tFmshFDSCGsuSt+5M8Fp+wKxmPe
2IvvXDsXkbg04VXkLzOpwHO7SWnAZyG5Wbfa/56i4yFmJsXWAZDO12gPceSsHfyV
IAJRveiZ/NlnRs8g01gaIKN6DyHNjt+VbbwUUYOG1y1XCpfKTK8YZSirL7UpfHhP
-----END RSA PRIVATE KEY-----"""



# Test vector from
# https://github.com/dlitz/pycrypto/blob/master/lib/Crypto/SelfTest/PublicKey/test_RSA.py
class RSATestCase(unittest.TestCase):
    def test_kat(self):
        plaintext = Bytes(0xEB7A19ACE9E3006350E329504B45E2CA82310B26DCD87D5C68F1EEA8F55267C31B2E8BB4251F84D7E0B2C04626F5AFF93EDCFB25C9C2B3FF8AE10E839A2DDB4CDCFE4FF47728B4A1B7C1362BAAD29AB48D2869D5024121435811591BE392F982FB3E87D095AEB40448DB972F3AC14F7BC275195281CE32D2F1B76D4D353E2D)
        ciphertext = 0x1253E04DC0A5397BB44A7AB87E9BF2A039A33D1E996FC82A94CCD30074C95DF763722017069E5268DA5D1C0B4F872CF653C11DF82314A67968DFEAE28DEF04BB6D84B1C31D654A1970E5783BD6EB96A024C2CA2F4A90FE9F2EF5C9C140E5BB48DA9536AD8700C84FC9130ADEA74E558D51A74DDF85D8B50DE96838D6063E0955
        modulus    = 0xBBF82F090682CE9C2338AC2B9DA871F7368D07EED41043A440D6B6F07454F51FB8DFBAAF035C02AB61EA48CEEB6FCD4876ED520D60E1EC4619719D8A5B8B807FAFB8E0A3DFC737723EE6B4B7D93A2584EE6A649D060953748834B2454598394EE0AAB12D7B61A51F527A9A41F6C1687FE2537298CA2A8F5946F8E5FD091DBDCB
        prime      = 0xC97FB1F027F453F6341233EAAAD1D9353F6C42D08866B1D05A0F2035028B9D869840B41666B42E92EA0DA3B43204B5CFCE3352524D0416A5A441E700AF461503
        e          = 17

        rsa = RSA(512, p=prime, q=modulus // prime, e=e)

        self.assertEqual(rsa.decrypt(ciphertext), plaintext)
        self.assertEqual(rsa.encrypt(plaintext), ciphertext)


    def test_gauntlet(self):
        for _ in range(10):
            bits = max(16, Bytes.random(2).int() >> 4)
            rsa = RSA(bits, e=65537)

            for _ in range(10):
                plaintext = Bytes.random((bits // 8) - 1)
                ciphertext = rsa.encrypt(plaintext)

                self.assertEqual(rsa.decrypt(ciphertext).zfill(len(plaintext)), plaintext)


    def test_der_encode(self):
        for _ in range(20):
            bits = max(1, Bytes.random(2).int() >> 4)
            rsa = RSA(bits, e=65537)

            should_pem_encode = Bytes.random(1).int() & 1

            der_bytes = rsa.export_private_key(should_pem_encode)
            recovered_rsa = RSA.import_key(der_bytes)

            self.assertEqual((rsa.d, rsa.e, rsa.n, rsa.p, rsa.q), (recovered_rsa.d, recovered_rsa.e, recovered_rsa.n, recovered_rsa.p, recovered_rsa.q))



    def test_import_export_private(self):
        rsa = RSA.import_key(TEST_PRIV)
        der_bytes = rsa.export_private_key()
        new_rsa = RSA.import_key(der_bytes)

        self.assertEqual((rsa.n, rsa.e, rsa.alt_d), (0x545702789299c59544f0a48037d5fcbe285b5c214d26469f7f52423763d01b331d0f7c9dfd5e98435b362e083875d101e10bf862a34a20cd38cd68743770b1ee57ce7f04e4335729aecacdc662b9b1e0f438f1a691538001d9c8f3374dc1dabf2e9fb316be636b0d2393f511c5bc7373c1666562322dc3911163e338b83bdf7d9a622c81b9edd19cd1699cae8c2def325de313e070d7733fc7ca95e0b12ef6a43095626e1fa3b19681a6e6b2828eb6b3487cb7bb58370086b108e9eaf9f20a53b8f44c9fe7ab7ad545d70b3c5f470190ece9e7172824e05747e1c431a664ab6bd2f914bf64e4dcac0575c493f52a488737f85742fb52aa4555f144ab8e601713, 0x10001, 7637900981413881127344732199207423148450857019726723094659043462794313258767201253269496359678839942555541437712415706663660985252940123204794095993626699211163986533562336773310103190916142252882331767886927729021516529141672972169957951166501750445256177733568843099186777096376892875529534391517354389358568809006385725873288954661635538351606457829485241023554979084645466210495420866845750976009860684015622002855709494103022482640146893844516679296838305756556603312962721311081086887412291530082263197989863828789712221961262494351622769754044860656696333724061992404959980518191241190042534000830303328685273))
        self.assertEqual((rsa.d, rsa.e, rsa.p, rsa.q), (new_rsa.d, new_rsa.e, new_rsa.p, new_rsa.q))
        self.assertEqual(der_bytes.replace(b'\n', b''), TEST_PRIV.replace(b'\n', b''))



    def test_import_export_public(self):
        rsa_pub  = RSA.import_key(TEST_PUB)
        rsa_priv = RSA.import_key(TEST_PRIV)

        der_bytes = rsa_pub.export_public_key()
        new_pub  = RSA.import_key(der_bytes)

        self.assertEqual((rsa_pub.n, rsa_pub.e), (rsa_priv.n, rsa_priv.e))
        self.assertEqual((rsa_pub.n, rsa_pub.e), (new_pub.n, new_pub.e))
        self.assertEqual(der_bytes.replace(b'\n', b''), TEST_PUB.replace(b'\n', b''))



    def _run_import_pem_enc(self, enc_priv):
        with self.assertRaises(ValueError):
            RSA.import_key(enc_priv)

        enc_rsa = RSA.import_key(enc_priv, PEM_PASSPHRASE)
        dec_rsa = RSA.import_key(TEST_PEM_DEC)
        self.assertEqual((enc_rsa.d, enc_rsa.e, enc_rsa.p, enc_rsa.q), (dec_rsa.d, dec_rsa.e, dec_rsa.p, dec_rsa.q))


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
                rsa = RSA(512)
                key = Bytes.random(Bytes.random(1).int() + 1)
                enc_pem = rsa.export_private_key(encryption=algo, passphrase=key)
                dec_rsa = RSA.import_key(enc_pem, key)

                self.assertEqual((rsa.d, rsa.e, rsa.p, rsa.q), (dec_rsa.d, dec_rsa.e, dec_rsa.p, dec_rsa.q))


    def test_import_ssh(self):
        rsa_pub      = RSA.import_key(TEST_SSH_PUB)
        rsa_ssh2_pub = RSA.import_key(TEST_SSH2_PUB)
        rsa_priv     = RSA.import_key(TEST_SSH_PRIV)

        self.assertEqual((rsa_pub.n, rsa_pub.e), (rsa_priv.n, rsa_priv.e))
        self.assertEqual((rsa_ssh2_pub.n, rsa_ssh2_pub.e), (rsa_priv.n, rsa_priv.e))

        self.assertEqual(rsa_priv.p, 170621934107914837135188221741345039360973520058114456501388562509658795389537603696495314914263307477879633584504500740005298573150803280618484950209080803799140960436472056595329677438530606065566161783436714140793820145487700054413432516764645134976280363736900482101671242116081306644146548602721659188139)
        self.assertEqual(rsa_priv.q, 147975660846396990587026799132395215581845148822588177668939892854130080870127891229734413269282872842954263443501467315040323804831400031921589112815742747614415764378548901698763469577356909867186752247509564255224167675065755796937983163876790155687818626513794653480829583948160749345458911841406938261219)
        self.assertEqual(rsa_priv.alt_d, 19762369934989515131049274315841316326050549933114536766674916078250573730800216520650633877972440419194814420402043176472759537753254149225125134250003994948721187698467807920387489440310994705791482721107511012797884534895932222871683633147680034924999627916905359454912445366494543706676734716375543152258328317139760580320162173490414588340925370831975060554770385250590880497700813834231770436219310405458193997653119990344803085718020467915664214557758416316811073003911746514622779992001874409075037973245976299609023867178313200550274791579981490063847585903047671618462828834780979891650959756006736369309609)



    def test_factorize_from_shared_p(self):
        for _ in range(5):
            bits = max(1, Bytes.random(2).int() >> 4)
            rsa_a = RSA(bits, e=65537)
            rsa_b = RSA(bits, e=65537, p=rsa_a.p)

            self.assertNotEqual(rsa_a.d, rsa_b.d)

            new_rsa_a, new_rsa_b = RSA.factorize_from_shared_p(rsa_a.n, rsa_b.n, rsa_a.e)

            self.assertEqual((rsa_a.d, rsa_a.e, rsa_a.n, rsa_a.p, rsa_a.q), (new_rsa_a.d, new_rsa_a.e, new_rsa_a.n, new_rsa_a.p, new_rsa_a.q))
            self.assertEqual((rsa_b.d, rsa_b.e, rsa_b.n, rsa_b.p, rsa_b.q), (new_rsa_b.d, new_rsa_b.e, new_rsa_b.n, new_rsa_b.p, new_rsa_b.q))



    def test_factorize_from_d(self):
        for _ in range(5):
            bits = max(1, Bytes.random(2).int() >> 4)
            rsa_a = RSA(bits, e=65537)
            new_rsa_a = RSA.factorize_from_d(rsa_a.d, rsa_a.e, rsa_a.n)

            # Here we sort p and q since we don't know which found prime will be assigned to which variable
            self.assertEqual((rsa_a.d, rsa_a.e, rsa_a.n, sorted([rsa_a.p, rsa_a.q])), (new_rsa_a.d, new_rsa_a.e, new_rsa_a.n, sorted([new_rsa_a.p, new_rsa_a.q])))

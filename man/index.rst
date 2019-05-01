MAN PAGE
========

SYNOPSIS
----------------
``samson [-h] [--eval] {hash,pki} ...``

``samson hash [-h] [--args [ARGS]] type [text]``

``samson pki [-h] [--args [ARGS]] [--pub] [--encoding [ENCODING]] [--encoding-args [ENCODING_ARGS]] action type [filename]``


DESCRIPTION
----------------
samson is a cryptanalysis and attack library. The intent is to provide a way to quickly prototype and execute cryptographic and side-channel attacks. samson was born from frustration with existing libraries artificially limiting user control over cryptographic primitives.
This help is for the command-line interface which provides a subset of samson's functionality for convenience.


TOP-LEVEL
----------------
**-h** - shows the dynamic help menu

**--eval** - evaluates arguments as Python code

**hash** - traverses to the 'hash' subcommand tree

**pki** - traverses to the 'pki' subcommand tree



HASH SUBCOMMANDS
----------------
**-h** - shows the dynamic help menu

**--args [ARGS]** - arguments to pass into the hash function

**type** - hash type (call **-h** for dynamic listing)

**text** - text/evaluation to hash



PKI SUBCOMMANDS
----------------
**-h** - shows the dynamic help menu

**--args** - arguments to pass into the PKI generation function

**--pub** - output public key

**--encoding [ENCODING]** - encoding to use on outputted keys (call **-h** for dynamic listing)

**--encoding-args [ENCODING_ARGS]** - arguments to pass into the encoding function

**action** - action to perform (currently 'parse' or 'generate')

**type** - PKI type (call **-h** for dynamic listing)

**filename** - file to read PKI data from



EXAMPLES
----------------
``samson hash md5 sometext`` - generate a hex-encoded MD5 hash of *sometext*

``samson hash keccak texttohash --args=r=1044,c=512,digest_bit_size=256`` - generate a hex-encoded Keccak hash of *texttohash*

``echo -ne 'hiya\x01\x02' | samson hash sha1`` - generate a hex-encoded MD5 hash of *hiya\\x01\\x02*

``samson --eval hash sha1 "b'hiya\x01\x02'"`` - same as above but using evaluation to process the byte literals

``samson --eval hash sha256 "Bytes(Bytes(0x01234567).zfill(10)[::-1].int() * 2)"`` - complicated evaluation example

``samson pki generate rsa --args=bits=512`` - generate a 512-bit RSA key with default encodings

``samson pki generate ecdsa --args=curve=nistp521 --pub`` - generate an ECDSA key and return the public with default encodings

``samson pki generate eddsa --args=curve=ed25519 --encoding=OpenSSH --encoding-args=user=noone@localhost`` - generate an EdDSA key, encode it as an OpenSSH private key, and set the OpenSSH user information to *noone@localhost*

``openssl genrsa 1024 | samson pki parse rsa`` - generate a PKCS1-encoded RSA key from OpenSSL and parse it with ``samson``

``samson pki parse auto x509_cert.crt`` - parse certificate from file and automatically determine the encoding and algorithm

``samson pki parse auto x509_cert.pem --pub --encoding=X509`` - same as above, but output it as a X509 public key

``samson pki generate rsa --args=bits=2048 --pub --encoding=x509_cert --encoding-args=ca=1,serial_number=#666#,issuer=#'CN=hiya,O=hiya-corp,L=Rack City'# | openssl x509 -text`` - generate CA cert with RDN 'CN=hiya,O=hiya-corp,L=Rack City'. To prevent argument parsing of the RDN string, use the preprocessor macro '#' to signify a literal.
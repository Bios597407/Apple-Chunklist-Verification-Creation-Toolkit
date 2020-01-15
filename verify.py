from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey.RSA import construct
from Crypto.Hash import SHA256
import numpy as np
import sys

def main(chunklist, public_key_loc):

	with open(public_key_loc,"rb") as key:
		key.seek(24) #Seek past header
		pubkey = key.read(256)
		reversed_key = int.from_bytes(pubkey, 'little') #Little endian encoding (so bytes get reversed)
		key.close()

	with open(chunklist,"rb") as chunk:
		chunk.seek(28)
		sig_offset = int.from_bytes(chunk.read(2), 'little')
		chunk.seek(0)
		digest = chunk.read(sig_offset) #Digest = header, filesize & SHA256 hash of DMG) are used for hash digest creation
		chunk.seek(sig_offset)
		signature = chunk.read(256)
		chunk.close()

	# Reverse Signature
	reversed_sig = np.flip(np.frombuffer(bytearray(signature), dtype=np.uint8, count=-1, offset=0),0).tobytes()

	#Exponent & Key
	e = 0x010001
	n = reversed_key

	key = construct((n, e))

	h = SHA256.new(digest)

	verified = PKCS1_v1_5.new(key).verify(h, reversed_sig)
	print('Verification = ', verified)

chunklist = sys.argv[1]
public_key_loc = sys.argv[2]
main(chunklist, public_key_loc)
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import numpy as np
import os
import sys

#Header Variables
#list immediately below pulled from c source files found on internet for reference
#define CHUNKLIST_MAGIC               0x4C4B4E43
#define CHUNKLIST_FILE_VERSION_10     1
#define CHUNKLIST_CHUNK_METHOD_10     1
#define CHUNKLIST_SIGNATURE_METHOD_10 1
#define CHUNKLIST_SIG_LEN             256
#define CHUNKLIST_PUBKEY_LEN          (2048/8)

chunklist_magic = b'\x43\x4E\x4B\x4C\x24\x00\x00\x00\x01\x01\x01\x00'
sig_method = b''
header_tail = b'\x00\x00\x00\x00\x24\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
hash_prefix = b'\x00\x00\xA0\x00'

#Chunk Size (10MB)
chunk = 10485760

# Array to store hashes of dmg
hashed = []

def main(dmgname, output_file, private_key):
	#Calculate Filesize
	if os.path.exists(dmgname):
		filesize = os.path.getsize(dmgname)
		edited_filesize = bytearray(filesize.to_bytes(4,'little'))
		#Filesize is only ever 3 bytes, anything beyond is overwritten with 0x00
		edited_filesize[3] = 0x00

	# Generate SHA256 Hashes of DMG
	with open(dmgname,"rb") as dmg:
		# Read and update hash string value in blocks of 10MB
		for byte_block in iter(lambda: dmg.read(chunk),b""):
			h = SHA256.new(byte_block).digest()
			hashed.append(h)
		dmg.close()

	# Remove output file if exists from previous attempt
	if os.path.exists(output_file):
		os.remove(output_file)

	# Begin Assembling Chunklist File
	with open (output_file, 'ab+') as write_file:
		# Check to see if file is Larger than 10MB, if not then does not use hash_prefix
		if filesize >= chunk:
			#If it used hash_prefix, sig_method = 2F (speculative)
			sig_method = b'\x2F\x00\x00\x00'
			#Assemble header components and write
			header = chunklist_magic + sig_method + header_tail
			write_file.write(header)
			for item in hashed:
				#Begin writing hashes for 10MB Chunks and attach prefix
				if item != hashed[-1]:
					write_file.write(hash_prefix)
					write_file.write(item)
				# For last 10MB Chunk hash, use filesize as prefix
				else:
					write_file.write(edited_filesize)
					write_file.write(hashed[-1])
					#Capture position where signature will be written
					sig_pos = write_file.tell()
					sig_offset = sig_pos.to_bytes(4, 'little')	
		else:
			# If it does not use hash_prefix, sig_method = 01 (speculative)
			sig_method = b'\x01\x00\x00\x00'
			# Assemble header components and write
			header = chunklist_magic + sig_method + header_tail
			write_file.write(header)
			# Write filesize
			write_file.write(edited_filesize)
			# Write hash
			write_file.write(hashed[0])
			# Capture position where signature will be written
			sig_pos = write_file.tell()
			sig_offset = sig_pos.to_bytes(4, 'little')

		write_file.close()

	# Inject Signature Offset into Header
	with open (output_file, 'rb+') as write_file:
		write_file.seek(28)
		write_file.write(sig_offset)
		# Read Entire File (excluding signature) to be used for hash in signature creation
		write_file.seek(0)
		digest = write_file.read(sig_pos)
		# Get Private Key
		key = RSA.import_key(open(private_key).read())
		# Create Signature
		d = SHA256.new(digest)
		signature = PKCS1_v1_5.new(key).sign(d)
		# Reverse bytes in signature
		reversed_sig = np.flip(np.frombuffer(bytearray(signature), dtype=np.uint8, count=-1, offset=0),0).tobytes()
		# Write Reversed signature to chunklist
		write_file.seek(sig_pos)
		write_file.write(reversed_sig)
		write_file.close()

dmgname = sys.argv[1]
output_file = sys.argv[2]
private_key = sys.argv[3]
main(dmgname, output_file, private_key)
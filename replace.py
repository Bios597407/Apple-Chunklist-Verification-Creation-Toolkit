import sys

def main(efi_file, outfile, efi_key_file, custom_key_file):
	#Get Original Key to Patch
	with open(efi_key_file,"rb") as f:
		original_key = f.read()
		f.close()

	#Get Custom Key to Patch
	with open(custom_key_file,"rb") as f:
		patch_key = f.read()
		f.close()

	#Read EFI Rom and store in variable
	with open(efi_file,"rb") as f:
		efi_rom = f.read()
		f.close()

	#Patch Rom File
	patched_efi_rom =  efi_rom.replace(original_key, patch_key)

	#Write Patched EFI Rom to File
	with open(outfile,"wb+") as f:
		f.write(patched_efi_rom)
		f.close()


efi_file = sys.argv[1]
outfile = sys.argv[2]
efi_key_file = sys.argv[3]
custom_key_file = sys.argv[4]
main(efi_file, outfile, efi_key_file, custom_key_file)


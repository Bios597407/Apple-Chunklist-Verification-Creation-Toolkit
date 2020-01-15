# Apple-Chunklist-Verification-Creation-Tool
Python 3 Tool for Verifying Apple Chunklists and Creating Custom Chunklist Files.

__Required Modules:__
```
pip3 install pycryptodome
pip3 install numpy
```

__Usage:__
```
python3 verify.py <chunklist file> <public key in efi format>
python3 create.py <dmg file> <output file> <private key in PEM format>
python3 generate_keys.py
```

__About:__

This project is a proof of concept for working with Apple's chunklist files. The verification tool 'verify.py' can be used in conjunction with the efi keys to verify official chunklist files. The creation tool 'create.py' is purely a proof of concept to show the creation process for the chunklist files. Although the creation tool has the ability to produce chunklist files, it utilizes the custom private key created with the key generation tool 'generate_keys.py'.

When verifying chunklists, 'verify.py' utilizes Apples raw RSA 2048 key format, which is produced by 'generate_keys.py' as 'pubkey.bin'.


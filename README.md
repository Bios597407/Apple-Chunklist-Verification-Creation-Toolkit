# Apple-Chunklist-Verification-Creation-Tool
Python 3 Tool for Verifying and Creating Apple Chunklist Files.

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

This project is a proof of concept for working with Apple's chunklist files. The verification tool 'verify.py' can be used in conjunction with the efi keys to verify official chunklist files. It can also be used with the custom pubkey.bin file created with 'generate_keys.py' to verify custom chunklist files. The creation tool 'create.py' is purely a proof of concept to show the creation process for the chunklist files. Although the creation tool has the ability to produce chunklist files, it utilizes the custom private key created with the key generation tool 'generate_keys.py', meaning they will not pass as official Apple chunklist files. The only way to create an official Apple chunklist file would be to use an offical Apple private key.

When verifying chunklists, 'verify.py' utilizes Apples raw RSA 2048 key format. For official files, this has typically been efi_keys/01.bin. For custom files, it would be the custom_keys/pubkey.bin key produced by 'generate_keys.py'.

__EFI Keys:__

The 5 EFI keys in the 'efi_keys' folder have been extracted from an Apple EFI rom. These keys were discussed by both <a href = "https://trmm.net/Thunderstrike_31c3">Trammell Hudson</a> and <a href = "https://reverse.put.as/2016/06/25/apple-efi-firmware-passwords-and-the-scbo-myth/"> reverser a@t put.as </a>. So far, only the first key seems to be utilized during chunklist verification. This also means that the public keys are hard coded into Apple EFI rom chips. The only way to allow for the verification of custom chunklists would be to replace one of the EFI keys with a custom key.

# Apple-Chunklist-Verification-Creation-Toolkit
Python 3 Toolkit for Verifying and Creating Apple Chunklist Files.

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
python3 replace.py <efi rom file> <output file> <original efi public key file> <custom public key file>
```

__About:__

This project is a proof of concept for working with Apple's chunklist files. The verification tool 'verify.py' can be used in conjunction with the efi keys to verify official chunklist files. It can also be used with the custom pubkey.bin file created with 'generate_keys.py' to verify custom chunklist files. The creation tool 'create.py' is purely a proof of concept to show the creation process for the chunklist files. Although the creation tool has the ability to produce chunklist files, it utilizes the custom private key created with the key generation tool 'generate_keys.py', meaning they will not pass as official Apple chunklist files. The only way to create an official Apple chunklist file would be to use an offical Apple private key.

When verifying chunklists, 'verify.py' utilizes Apple's raw RSA 2048 key format. For official files, this has typically been efi_keys/01.bin. For custom files, it would be the custom_keys/pubkey.bin key produced by 'generate_keys.py'.

__EFI Keys:__

The 5 EFI keys in the 'efi_keys' folder have been extracted from an Apple EFI rom. These keys were discussed by both <a href = "https://trmm.net/Thunderstrike_31c3">Trammell Hudson</a> and <a href = "https://reverse.put.as/2016/06/25/apple-efi-firmware-passwords-and-the-scbo-myth/"> reverser a@t put.as </a>. So far, only the first key seems to be utilized during chunklist verification. This also means that the public keys are hard coded into Apple EFI rom chips. The only way to allow for the verification of custom chunklists is to patch your EFI rom with one of the custom EFI public keys generated with 'generate_keys.py'.

__Replace Original Public Key with Custom Public Key:__

In order to utilize custom chunklist files, the EFI rom will need to be patched with a custom public key. This can be done with 'replace.py'. Just choose one of the 5 public keys and replace it with a custom public key. Keys must be in Apple's raw RSA 2048 format (i.e. one of the efi keys and the custon generated pubkey.bin). Note that is would require the hardware and ability to read / write efi rom chips. Also note that since the first key is generally utilized by official Apple software, patching it will likely result in an inability to verify any future official software verifications / installations and is not recommended. Again this is only a proof of concept.

__Context:__

These tools were developed with 2013 and newer systems in mind. The public key formats for older systems may differ.

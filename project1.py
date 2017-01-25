# -*- coding: utf-8 -*-
import subprocess
import itertools
import struct
import binascii

def first(a):
    return next(iter(a))

username = map(ord, 'cccc000acccccccccccccccccccccccc'.decode('hex'))
salt = map(ord, 'baba000ababababababababababababa'.decode('hex'))

p = subprocess.Popen(['/home/kamil/Projects/Windows & Linux Exploitation/MBE/MBE_release/levels/project1/tw33tchainz'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

# [====== Get generated passphrase and reverse ======]

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

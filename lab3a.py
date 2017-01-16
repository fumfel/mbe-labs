# -*- coding: utf-8 -*-
from pwn import *
import binascii
import struct

context(arch ='i386', os ='linux')

# RA prawdopodobnie w odleglosci 766 bajtow od startu
# 1. Okreslenie adresu powrotu do nadpisania - 2FFFFCF7h * 4 - RA z funkcji store number (który po >> 24 daje 183)
# 2. Okreslenie adresu bufora do wpisania shellcode'u
# 3. Wygenerowanie numerycznego shellcode'u i sekwencji do jego wpisania w pamiec (store + number + index)
# Miejsce w pamieci do wpisania  adres do wpisania = numer + (index * 4)
# Stała dodawana do indeksu: 0xBFFFF3F8

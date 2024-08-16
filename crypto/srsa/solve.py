#!/usr/bin/env sage
from pwn import process
from math import gcd
from Crypto.Util.number import long_to_bytes as ltb

r = process("./chal.py")

def recv():
	r.recvuntil(b'CT = ')
	CT = int(r.recvlineS(keepends=False))
	return CT

def send(x):
	r.sendlineafter(b'Plaintext: ', str(x).encode())

Fp = recv()
F2p = Fp**2

send(Fp)
Fp2 = recv()

send(Fp*Fp)
F2p2 = recv()

X = gcd(Fp2 - Fp, Fp2**2 - F2p2)

# most prime factors of X will be small. The only big one is going to be p due to probability
# so we can factorize it quickly
p = list(factor(X))[-1][0]
print(f"{p = }")

send(F2p**2)
F4p2 = recv()

Y = gcd(Fp2**2 - F2p2, F2p2**2 - F4p2)

assert Y % p == 0

# again most primes of Y will be small. Only big one will be q.
q = list(factor(Y // p))[-1][0]
print(f"{q = }")

p = int(p)
q = int(q)
Fp = int(Fp)

d = pow(p, -1, (p-1)*(q-1))
d = int(d)
F = pow(Fp, d, p * q)
print(ltb(F))

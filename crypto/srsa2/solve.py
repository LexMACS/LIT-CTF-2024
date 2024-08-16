#!/usr/bin/env sage
from Crypto.Util.number import long_to_bytes as ltb
from math import gcd

with open("output.txt", "r") as f:
	f.readline()
	exec(f.read())

CT = Integer(CT)
n = Integer(n)

# MAIN IDEA:
# We know that PT has ~496 bits.
# Furthermore, by Fermat's Little Theorem, we have CT = PT^p = PT mod p so CT = PT + pk for some integer k
# This means CT / n = PT/n + pk/n = PT/n + k/q
# Then, |CT / n - k/q| = PT/n. Because PT has ~496 bits, this means PT/n is around 1/2^(2034)
# This is less than 1/2^(4049) which is less than 1/(2q^2)
# By Legendre's Theorem, this means k/q is a convergent of (CT mod n)/n. This means we can find q.
CF = continued_fraction(CT / n)

for i in range(3000):
	q = CF.denominator(i)
	if gcd(q, n) > 1:
		break

p = n // q

p = int(p)
q = int(q)
d = int(pow(p, -1, (p-1)*(q-1)))
CT = int(CT)

print(ltb(pow(CT, d, p*q)))

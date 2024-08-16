import random

encoded_with_xor = b'\x81Nx\x9b\xea)\xe4\x11\xc5 e\xbb\xcdR\xb7\x8f:\xf8\x8bJ\x15\x0e.n\\-/4\x91\xdcN\x8a'

random.seed(0)
key = random.randbytes(32)

assert len(key) == len(encoded_with_xor)

print(''.join(map(chr, (key[i] ^ encoded_with_xor[i] for i in range(len(key))))))

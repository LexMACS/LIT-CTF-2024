from Crypto.Util.number import long_to_bytes
import owiener

with open("chal.txt", "r") as f:
	exec(f.read())

d = owiener.attack(e, N)
print(long_to_bytes(pow(c, d, N)))

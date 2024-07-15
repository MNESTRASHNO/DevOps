from hashlib import sha256

n = "a1"
stamp = "1716808759"
bytes = n + stamp
a = sha256(bytes.encode()).hexdigest()
print(a)

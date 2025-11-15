
# === Parameters ===

T0 = 7
A = 5
C = 3
b = 8
M = 2 ** b

# random generation
def T(i: int):
    if i == 0:
        return T0
    return (A * T(i - 1) + C) % M

# def build_gamma_cipher(length: int) -> bytes:
#     res = bytes()
#     for i in range(length):
#         res += T(i)
#
#     return res


def apply_gamma_cihper(s: bytes):
    res = b''
    for i in range(len(s)):
        value = s[i] ^ T(i + 1)
        res += bytes([value])

    return res

init = bytes([1, 2, 3])
encrypted = apply_gamma_cihper(init)
print(encrypted)
decrypted = apply_gamma_cihper(encrypted)
print(decrypted)

assert init == decrypted


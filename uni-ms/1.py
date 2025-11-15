
ALPHABET_START = ord('a')
ALPHABET_SIZE = 26

def cycle_chr(c: str, delta: int):
    if (ALPHABET_START <= ord(c) <= ALPHABET_START + ALPHABET_SIZE):
        n = ALPHABET_START + (ord(c) + delta - ALPHABET_START) % ALPHABET_SIZE
        return chr(n)
    else:
        return c


def cipher(s: str, k1: int, k2: int) -> str:
    res = ''
    for i in range(len(s)):
        k = k1 if i % 2 == 0 else k2

        res += cycle_chr(s[i], k)

    return res

encrypted = cipher(input(), 5, 10)
print(encrypted)
print(cipher(encrypted, -5, -10))

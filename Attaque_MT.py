from Mersenne_twister import MersenneTwister


def undo_right_shift_xor(y, shift):
    x = 0
    for i in range(32):
        bit = (y >> (31 - i)) & 1
        if i >= shift:
            bit ^= (x >> (32 - i + shift - 1)) & 1
        x |= bit << (31 - i)
    return x


def undo_left_shift_xor_and(y, shift, mask):
    x = 0
    for i in range(32):
        bit = (y >> i) & 1
        if i >= shift:
            if (mask >> i) & 1:
                bit ^= (x >> (i - shift)) & 1
        x |= bit << i
    return x


def untemper(y5):
    y4 = undo_right_shift_xor(y5, 18)
    y3 = undo_left_shift_xor_and(y4, 15, 0xEFC60000)
    y2 = undo_left_shift_xor_and(y3, 7,  0x9D2C5680)
    y1 = undo_right_shift_xor(y2, 11)
    return y1

randomizer = MersenneTwister(123)
randomizer.next_number()
print(randomizer.MT[randomizer.INDEX])
n = randomizer.next_number()
print(n)
print(untemper(n))
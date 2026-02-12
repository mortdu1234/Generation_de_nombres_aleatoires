from Mersenne_twister import MersenneTwister


def undo_right_shift_xor(y, shift):
    """
    input : y : nombre en sortie de Mersenne Twister -> int
            shift : nombre de bits de décalage -> int

    output : x : antécédent de y avant le décalage -> int

    sémantique : Permmet de résoudre l'équation y = x ^ (x >> shift) pour retrouver x à partir de y.
    """
    x = 0
    for i in range(32):
        bit = (y >> (31 - i)) & 1
        if i >= shift:
            bit ^= (x >> (32 - i + shift - 1)) & 1
        x |= bit << (31 - i)
    return x


def undo_left_shift_xor_and(y, shift, mask):
    """
    input : y : nombre en sortie de Mersenne Twister -> int
            shift : nombre de bits de décalage -> int
            mask : masque utilisé dans l'opération XOR -> int

    output : x : antécédent de y avant le décalage -> int

    sémantique : Permmet de résoudre l'équation y = x ^ ((x >> shift) & mask) pour retrouver x à partir de y.
    """
    x = 0
    for i in range(32):
        bit = (y >> i) & 1
        if i >= shift:
            if (mask >> i) & 1:
                bit ^= (x >> (i - shift)) & 1
        x |= bit << i
    return x


def untemper(y5):
    """
    input : y5 : nombre en sortie de Mersenne Twister après les 4 étapes de tempering -> int

    output : y1 : nombre avant le tempering, soit l'état un des 624 valeur interne de Mersenne Twister -> int

    sémantique : Permet de retrouver le nombre original à partir du nombre temperé en inversant les opérations de tempering.
    """
    y4 = undo_right_shift_xor(y5, 18)
    y3 = undo_left_shift_xor_and(y4, 15, 0xEFC60000)
    y2 = undo_left_shift_xor_and(y3, 7,  0x9D2C5680)
    y1 = undo_right_shift_xor(y2, 11)
    return y1


def restore_interne_state_of_mersenne_tiwister(): 
    """
    input : N/A

    output : N/A

    sémantique : Recompose l'entièreté de l'état interne de Mersenne Twister à partir des sorties. Puis test si l'état recomposé 
                 et le même que l'état d'origine. 
    """
    generator = MersenneTwister(123)
    recompose_state = []
    for _ in range(624):
        recompose_state.append(untemper(generator.next_number()))
    original_state = generator.MT
    assert(original_state == recompose_state)


if __name__ == "__main__":
    print("=== Test pour une valeur ===")
    generator = MersenneTwister(123)
    generator.next_number()
    test1 = generator.MT[generator.INDEX]
    test2 = untemper(generator.next_number())
    print(f"  Etat interne d'une valeur de Mersenne Twister : {test1}")
    print(f"  Retour de la fonction 'untemper([sortie de Mersenne Twister])' : {test2}")
    assert(test1 == test2)
    print("  On retrouve bien l'état initial. Test validé !")

    print("\n=== Test l'état interne de Mersenne Twister (624 valeur) ===")
    print("  Appel de la fonction 'restore_interne_state_of_mersenne_tiwister()' ...")
    restore_interne_state_of_mersenne_tiwister()
    print("  Assertion passé. On retrouve donc bien l'état interne Mersenne Twister uniquement avec les sorties. Test validé !")

    print("\nLes deux tests on réussit. On peut donc conssidérer que notre programme d'attaque fonctionne.")


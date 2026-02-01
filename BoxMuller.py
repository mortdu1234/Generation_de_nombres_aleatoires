from Mersenne_twister import MersenneTwister
from math import log2, sqrt

SEED: int = 123
RANDOMUNIFORM: MersenneTwister = MersenneTwister(SEED) # algorithme de génération de nombre Uniforme
OTHER_NUMBER: float | None = None

def BoxMuller():
    """renvois un nombre aléatoire en suivant l'algorithme de Box Muller
    qui suit une loi Normale Centrée Réduite

    Returns:
        float: nombre aléatoire généré
    """
    global OTHER_NUMBER
    # si un nombre a déjà été généré
    if OTHER_NUMBER:
        nb = OTHER_NUMBER
        OTHER_NUMBER = None
        return nb

    x1 = float("0."+str(RANDOMUNIFORM.next_number()))
    x2 = float("0."+str(RANDOMUNIFORM.next_number()))
    s = x1**2+x2**2
    while s >= 1:
        x1 = float("0."+str(RANDOMUNIFORM.next_number()))
        x2 = float("0."+str(RANDOMUNIFORM.next_number()))
        s = x1**2+x2**2

    
    const = sqrt(-2*log2(s) / s)
    OTHER_NUMBER = x2 * const
    return x1 * const

if __name__ == "__main__":
    print("implémentation de la génération de nombre aléatoire")
    for i in range(10):
        nb = BoxMuller()
        print(nb)
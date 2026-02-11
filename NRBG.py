import os
from Mersenne_twister import MersenneTwister
from BBS import BBS

def check_param(mini,maxi,param):
    """
    Input:
        mini (int): borne inférieure exclusive acceptable pour `param`.
        maxi (int): borne supérieure exclusive acceptable pour `param`.
        param (int): valeur à vérifier.

    Output:
        None

    Sémantique:
        Vérifie que `param` est strictement entre `mini` et `maxi`.
    """
    if not(mini < param < maxi):
        raise RuntimeError(f"La nombre de bits du nombre sortie doit être compri entre {mini+1} et {maxi-1}")

def NRGB(bit_length):
        """
        Input:
                bit_length (int): nombre de bits souhaité pour la valeur de sortie.
                                  Doit être strictement compris entre 1 et 33
        Output:
                int: un entier aléatoire.

        Sémantique:
                Génère un nombre pseudo/aléatoire en combinant trois sources d'entropie.
        """
        check_param(0,33,bit_length)
        entropy = os.urandom(4)
        DRGB1 = MersenneTwister(123)
        DRGB2 = BBS(1)[0]
        s1 = int.from_bytes(entropy, 'big') # 32 bits
        s2 = DRGB1.next_number() # 32 bits
        s3 = DRGB2 # 64 bits

        mask = (1 << bit_length) - 1 
        result = (s1 ^ s2 ^ s3) & mask 

        return result


if __name__ == "__main__":
    res = NRGB(32)
    print(res)


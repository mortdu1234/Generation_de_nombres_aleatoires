from Mersenne_twister import MersenneTwister
from math import sqrt



##################################
#   Fonctions de vérifications  #
##################################

def is_primary(number):
    """
    input : number : entier à tester -> int

    output : True si le nombre est premier, False sinon -> bool

    sémantique : Vérifie si l'entier fourni est un nombre premier.
    """
    if number <= 1:
        return False
    for i in range(2, int(sqrt(number))):
        if number % i == 0:
            return False
    return True

def calcul_pgcd(a, b):
    """
    input : a, b : int, int

    output : pgcd(a,b) : plus grand commun diviseur -> int

    sémantique : Calcule et retourne le pgcd des deux entiers donnés en entrée
                 en utilisant l'algorithme d'Euclide.
    """
    while b != 0:
        a, b = b, a % b
    return a


###############################
#   Fonctions de génération  #
###############################

def generate_prime_3mod4(seed):
    """
    input : seed : valeur d'initialisation pour le générateur -> int

    output : number : nombre premier congru à 3 modulo 4 -> int

    sémantique : Utilise le générateur MersenneTwister pour produire des
                 candidats et retourne le premier nombre qui est premier
                 et qui est congru à 3 modulo 4.
    """
    ramdomizer = MersenneTwister(seed)
    while True:
        number = ramdomizer.next_number()
        number |= 3
        if(is_primary(number)):
            return number

def generate_M_and_Xo(p,q):
    """
    input : p, q : deux nombres premiers (congrus à 3 mod 4) -> int, int

    output : (M, Xo) : module M = p*q et une valeur de départ X0 première avec M -> (int, int)

    sémantique : Calcule M = p*q puis génère (avec MersenneTwister) une valeur
                 Xo telle que pgcd(M, Xo) == 1. Retourne le couple (M, Xo).
    """
    M = p*q
    ramdomizer = MersenneTwister(789)
    while True:
        Xo = ramdomizer.next_number()
        Xo **= 2
        print(calcul_pgcd(M,Xo) == 1)
        if(res == 1):
            return M,Xo


###################################
#   Algorithme de Blum–Blum–Shub  #
###################################

def BBS(length_of_sequence):
    """
    input : length_of_sequence : longueur de la séquence à générer -> int

    output : suite de X1, X2, ... Xn : séquence de nombres pseudo-aléatoires -> list[int]

    sémantique : Implémente l'algorithme Blum–Blum–Shub (BBS). 
    """
    sequence = []
    p = generate_prime_3mod4(123)
    q = generate_prime_3mod4(456)
    M,Xn = generate_M_and_Xo(p,q)
    
    for _ in range(length_of_sequence):
        Xn = (Xn**2)%M
        sequence.append(Xn)
    return sequence


if __name__ == "__main__":
    res = BBS(10)
    print(f"Séquence générée : {res}")
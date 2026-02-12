from math import  gcd
from LCG import linear_congruential_generator
from functools import reduce

def modinverse(a, m):
    """
        Entrée :
            a : entier
            m : entier (modulo)

        Sortie :
            retourne l’inverse modulaire de a modulo m

        Remarque :
            si a et m ne sont pas premiers entre eux,
            alors l’inverse n’existe pas.
    """
    if gcd(a, m) != 1:
        raise ValueError("Inverse modulaire inexistant : gcd(a, m) ≠ 1")
    return pow(a, -1, m)


def trouver_terme_precedent(x1, a, c, m):
    """
        Entrée :
            x1 : terme courant de la suite
            a, c, m : paramètres du LCG connus

        Sortie :
            retourne le terme précédent x0
    """
    inv_a = modinverse(a, m)
    x0 = (x1 - c) * inv_a % m
    return x0


def attaque(xn, a, c, m, long_seq):
    """
        Entrée :
            xn : dernier terme connu de la suite
            long_seq : nombre de fois qu’on remonte dans la suite

        Sortie :
            retourne le (n-long_seq)ème terme de la suite générée

        Principe :
            on applique plusieurs fois la fonction trouver_terme_precedent
            pour remonter la suite terme par terme.
    """
    xi = xn
    for _ in range(long_seq,0,-1):
        xi = trouver_terme_precedent(xi,a,c,m)
    return xi



def trouver_modulo(seq):
    """
        Entrée : seq = sequence générée avec LCG
            Condition : len(seq) >= 4
        Sortie : retourne le modulo m ou un multiple de m selon le nombre de sorties observées
                Plus il y a de sorties dans la séquence, plus il y a de chance d'obtenir m
    """
    values = []
    for i in range(len(seq)-3):
        t0, t1, t2 = seq[i+1] - seq[i] , seq[i+2] - seq[i+1], seq[i+3] - seq[i+2]
        v = t1**2 - (t2*t0)
        values.append(v)
        
    """
        La fonction map(abs, values) applique la valeur absolue à
           chaque élément de la liste values.
           On obtient donc une nouvelle séquence contenant |v1|, |v2|, ...

        Ensuite, la fonction reduce est utilisée pour "réduire"
           cette liste en une seule valeur.
           Elle applique une fonction binaire (ici gcd) de gauche à droite.

           Concrètement, cela revient à calculer :
           gcd(gcd(gcd(v1, v2), v3), v4), ...

        On obtient ainsi le PGCD de toutes les valeurs,
           ce qui permet de retrouver un multiple du modulo m.
    """
    return reduce(gcd, map(abs, values))


def trouver_a(x0,x1,x2, m):
    """
        Entrée :
            x0, x1, x2 : trois termes consécutifs de la suite
            m : modulo du LCG (supposé connu)

        Sortie :
            retourne la valeur du multiplicateur a modulo m
    """

    a = (x2-x1)*modinverse(x1-x0,m)
    return a % m

def trouver_c(x0, x1, a, m):
    """
        Entrée :
            x0, x1 : deux termes consécutifs de la suite
            a : multiplicateur du LCG (déjà retrouvé)
            m : modulo

        Sortie :
            retourne la constante c modulo m
    """
    return ( x1 - (a*x0) ) % m


def attaque_cas2(seq, n):
    """
        Entrée :
            seq : séquence générée par le LCG (au moins 4 valeurs)
            n   : nombre de termes que l’on veut remonter

        Sortie :
            permet de retrouver les paramètres m, a, c
            puis de remonter jusqu’à la graine initiale
            retourne le n-ème terme de la suite générée , en partant de la fin et en remontant

        Principe de l’attaque (cas 2) :
            Ici on suppose que l’on ne connaît aucun paramètre
            du LCG (ni m, ni a, ni c).
    """
    m = trouver_modulo(seq)
    print("m trouvé : ",m,end="; ")
    a = trouver_a(seq[0], seq[1], seq[2], m)
    print("a trouvé : ",a,end="; ")
    c = trouver_c(seq[0], seq[1], a, m)
    print("a trouvé : ",c)
    print("La graine trouvé :",end=" ")
    return attaque(seq[-1], a, c, m, long_seq=n)

if __name__ == "__main__":
    print("---------Cas 1: on connaît les paramètres a, c et m ------------")
    m, a, c,  = 1024, 585, 899 #paramètres connus
    x0 = 339 #graine à retrouver
    long_seq = 8 
    seq = linear_congruential_generator(m,a,c,x0,long_seq)
    print("Séquence générée par LCG à partir de la graine",x0, " :")
    print(seq)
    x1 = seq[-1]
    graine_retrouvee = attaque(x1, a, c, m, long_seq)
    seq_reconstruite = linear_congruential_generator(m,a,c,graine_retrouvee,long_seq)
    print("Séquence générée par LCG à partir de la graine retrouvée ",graine_retrouvee, " :")
    print(seq_reconstruite)
    
    print("\n---------Cas 2: on ne connaît pas les paramètres a, c et m------------")
    print(attaque_cas2(seq, long_seq))
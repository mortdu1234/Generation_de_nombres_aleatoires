
def linear_congruential_generator(m,a,c,Xo,length_of_sequence):
    """
    input : m : 0 < m est le modulo -> int
            a : 0 < a < m est le multiplicateur -> int
            c : 0 <= c < m est l’incrément -> int
            X0 : 0 <= X0 < m est la valeur de départ -> int
            length_of_sequence : nombre de nombre à généré -> int

    output : X1,X2, ... , Xn+1: nombres aléatoires générés -> int[]

    sémentique : Produit une séquence de nombres pseudo-aléatoires calculés à l'aide 
                 d'une équation linéaire discontinue par morceaux.
    """
    sequence = []
    Xn = Xo
    for _ in range(length_of_sequence):
        Xn = (a*Xn + c) % m 
        sequence.append(Xn)
    return sequence

# Test
def test():
    """
    input : N/A
    output : N/A
    sémentique : Vérifie le fonctionnement du générateur à l'aide d'une assertion
    """
    try:
        res = linear_congruential_generator(9,2,1,3,7)
        print(f"Séquence générée : {res}\nSéquence attendue : [7, 6, 4, 0, 1, 3, 7]")
        assert(res == [7, 6, 4, 0, 1, 3, 7])
        print("Test passé avec succès !!")
    except AssertionError:
        print("Erreur : la séqence optenue n'est pas celle qui était attendue")


def check_input(text,mini,maxi):
    elem = int(input(text))
    while not(mini < elem < maxi):
        print(f"Erreur : vous devez entrer une valeur entre {mini+1} et {maxi-1}")
        elem = int(input(text))
    return elem


if __name__ == "__main__":
    print("==== Phase de teste avant démarage ====")
    test()
    print("\n==== Entré pour l'utilisateur ====")
    m = check_input("Entrez m : ",0,10000)
    a = check_input("Entrez a : ",0,m)
    c = check_input("Entrez c : ",-1,m)
    Xo = check_input("Entrez X0 : ",-1,m)
    length = int(input("Entrez la longueur de la séquence que vous voulez générer : "))
    res = linear_congruential_generator(m,a,c,Xo,length)
    print(f"Séquence générée : {res}")
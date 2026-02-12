from time import time_ns
from hashlib import sha256
def random(seedlen):
    """
    Simule un générateur de nombres aléatoires système basé sur l'entropie locale.
    
    Entrée :
        seedlen (int) : Nombre d'octets aléatoires à générer.
        
    Sortie :
        (bytes) : Un tableau d'octets imprévisibles de longueur 'seedlen'.
        
    Logique : 
        On utilise des sources de bruit liées au matériel : temps en nanosecondes 
        et adresse mémoire d'un objet pour créer une graine initiale, puis on 
        l'étend via SHA-256 pour atteindre la taille demandée.
    """
    t = time_ns() #prends l'horodotage actuel en nanosecondes
    obj_random = id(object()) #id unique d'un objet temporaire
    
    
    """
        val : concatenation en bytes des données aléatoires sources
    """
    val =  t.to_bytes(8, 'big') + obj_random.to_bytes(8, 'big')
    
    
    base_hash = sha256(val).digest() #hashage de val pour générer 32 octets
    
    cpt = 0
    result = b'' #contient le retour du random
    while len(result) < seedlen:
        data = base_hash + cpt.to_bytes(4,'big')
        result += sha256(data).digest()
        cpt += 1
        
    return result[:seedlen]

if __name__ == "__main__":
    print(random(50).hex())    
    
    
    
    
    
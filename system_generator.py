from time import time_ns
from hashlib import sha256
def random(seedlen): #seedlen : type entier - nombre d'octets de l'aléatoire à générer
    """
        Sources d'aléatoire : le temps et un objet aléatoire
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
    
    
    
    
    
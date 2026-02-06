from hashlib import sha256
from system_generator import random

def hashgen(seedlen, etat):
    """
    seedlen : type int
        nombre d'octets de la valeur à retourner
    etat : type bytes
        donnee initiale en tableau d'octets
    """
    data = etat
    w = b'' #initialisation du bytes à retourner
    while len(w) < seedlen:
        w += sha256(data).digest() #on ajoute à w le hashage de data courant
        data_int = int.from_bytes(data, byteorder='big') + 1 #conversion en int, puis incrémentation 
        data = data_int.to_bytes(len(data), byteorder='big') #reconversion en bytes
    
    return w[:seedlen]

def seed(seedlen):
    """Génère un nouveau seed aléatoire de longueur seedlen octets"""
    return random(seedlen)
        
        
def generer_hash_DRBG(etat, const, reseed_cpt, reseed_interval, seedlen):    
    if reseed_cpt > reseed_interval:
        etat = seed(seedlen)
        reseed_cpt = 1
        
    # Génération des bits pseudo-aléatoires
    bits_retournes = hashgen(seedlen, etat)
    
    const_int =  int.from_bytes(const, byteorder='big')
    
    """
        b'\x03' + etat : Concatène l’octet constant 0x03 devant etat
        Dans Hash_DRBG, le même état est utilisé pour produire plusieurs valeurs (w, H, etc.)
        Ajouter 0x03 devant etat garantit que ce hash est différent du hash pour w, même si etat est identique
    """
    H = sha256(b'\x03' + etat).digest()
    H_int = int.from_bytes(H, byteorder='big')
    
    etat_int = int.from_bytes(etat, byteorder='big')
    etat_int = (etat_int + H_int + const_int + reseed_cpt) % (2**(8*seedlen))
    
    etat = etat_int.to_bytes(seedlen, byteorder='big')
    
    # Incrémenter le compteur de reseed
    reseed_cpt += 1
    
    
    return bits_retournes, etat, reseed_cpt
    
    
if __name__ == "__main__":
    # --- Paramètres ---
    seedlen = 16  # 128 bits = 16 octets
    reseed_interval = 5
    
    # --- Initialisation ---
    V = seed(seedlen)          # état interne initial
    C = seed(seedlen)          # constante interne
    reseed_cpt = 1
    
    print("État initial V :", V.hex())
    print("Constante C    :", C.hex())
    print("Reseed compteur :", reseed_cpt)
    print("-------------------------------------------------")
    
    # --- Génération de plusieurs sorties ---
    for i in range(1, 6):
        output, V, reseed_cpt = generer_hash_DRBG(V, C, reseed_cpt, reseed_interval, seedlen)
        print(f"Génération {i}:")
        print("  Sortie (hex) :", output.hex())
        print("  Nouvel V     :", V.hex())
        print("  Reseed compteur :", reseed_cpt)
        print("-------------------------------------------------")
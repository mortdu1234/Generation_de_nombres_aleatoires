from hashlib import sha256
from system_generator import random

def hashgen(seedlen, etat):
    """
    Produit un tableau d'octets en hachant l'état de manière itérative.
    Entrées :
        seedlen (int) : Nombre d'octets total à générer.
        etat (bytes)  : La valeur interne actuelle qui sert de base au hachage.
        
    Sortie :
        (bytes) : Un tableau d'octets de longueur 'seedlen' destiné à l'utilisateur.
        
    Logique : On hache l'état, puis on l'incrémente de 1 à chaque tour pour que 
    chaque nouveau bloc de 32 octets soit radicalement différent du précédent.
    """
    data = etat
    w = b'' #initialisation du bytes à retourner
    while len(w) < seedlen:
        w += sha256(data).digest() #on ajoute à w le hashage de data courant
        data_int = int.from_bytes(data, byteorder='big') + 1 #conversion en int, puis incrémentation 
        data = data_int.to_bytes(len(data), byteorder='big') #reconversion en bytes
    
    return w[:seedlen]

def seed(seedlen):
    """
    Récupère une source de hasard frais auprès du système.
    
    Entrée :
        seedlen (int) : Longueur de la graine souhaitée en octets.
        
    Sortie :
        (bytes) : Une suite d'octets aléatoires (entropie système).
        
    """
    return random(seedlen)
        
        
def generer_hash_DRBG(etat, const, reseed_cpt, reseed_interval, seedlen):   
    """
    Génère les bits aléatoires
    
    Entrées :
        etat (bytes)            : L'état V actuel.
        const (bytes)           : La constante C (graine de sécurité).
        reseed_cpt (int)        : Compteur du nombre de générations effectuées.
        reseed_interval (int)   : Limite avant de devoir rafraîchir le hasard.
        seedlen (int)           : Taille de l'état en octets.
        
    Sorties :
        bits_retournes (bytes) : Les données aléatoires produite.
        etat (bytes)           : Le nouvel état V mis à jour pour la prochaine itération.
        reseed_cpt (int)       : Le compteur
    """ 
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
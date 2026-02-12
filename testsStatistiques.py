import math
from BoxMuller import BoxMuller
from LCG import linear_congruential_generator
from Mersenne_twister import MersenneTwister
from BBS import BBS
from scipy.stats import chi2



def normaliser(data : list):
    """normalise les données entre 0 et 1

    Args:
        data (list): donnée récupéré

    Returns:
        list[float]: donnée en d'entrée normalisé
    """
    if not data:
        return []
    
    # Si déjà entre 0 et 1
    min_val = min(data)
    max_val = max(data)
    
    if min_val >= 0 and max_val <= 1:
        return data
    
    # Sinon, normaliser
    if max_val == min_val:
        return [0.5] * len(data)
    
    return [(x - min_val) / (max_val - min_val) for x in data]


def conversion_octet(data: list[float]) -> dict[int, int]:
    """Renvoie le nombre d'occurrences de chaque octet
    Args:
        data (list[float]): données normalisées dans [0, 1]
    Returns:
        dict[int, int]: nombre d'occurrences de chaque octet (0-255)
    Raises:
        ValueError: si les données ne sont pas normalisées ou du mauvais type
    """
    nb_occurence_octet: dict[int, int] = {i: 0 for i in range(256)}
    
    for i, value in enumerate(data):
        if not isinstance(value, float):
            raise ValueError(f"Donnée à l'index {i} n'est pas un float: {type(value)}")
        
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"Donnée à l'index {i} hors de [0,1]: {value}")
        
        # Conversion en octet [0, 255]
        octet = int(value * 255)
        nb_occurence_octet[octet] += 1
    
    return nb_occurence_octet


def effectuer_test(data_brut: list, precision: int=3, affichage: bool=False) -> list[str]:
    """effectue les différents tests a partir de donnée brut

    Args:
        data_brut (list): ensemble de données brut générée
        precision (int, optional): nombre de chiffre de précision dans l'affichage des résultats. Defaults to 3.
        affichage (bool, optional): effectue un affichage terminal des résultats. Defaults to False.

    Returns:
        list[str]: liste des interprétations des différents tests
    """
    data = normaliser(data_brut)
    n = len(data)

    result_shannon = Shannon(data, n)
    result_chi2 = Chi2(data, n)
    result_correlations = []
    lags = [1, 2, 8, 16]
    for lag in lags:
        result_correlations.append(autocorrelation(data, n, lag))
    result_ks = kolmogorov_smirnov(data, n)

    # AFFICHAGE 
    if affichage:
        print("\n"*5)
        print("="*60)
        print("Test de Shannon")
        print("="*60)
        print(f"Entropie : {round(result_shannon.get('entropie', 0), precision)}")
        print(f"Ratio : {round(result_shannon.get('ratio', 0), precision)}")
        print(f"{result_shannon.get('interpretation')}")
        print("="*60)
        print()
        print("="*60)
        print("Test de Chi2")
        print("="*60)
        print(f"Chi2 calculée : {round(result_chi2.get('chi2c', 0), precision)}")
        print(f"Chi2 théorique : {round(result_chi2.get('chi2t', 0), precision)}")
        print(f"{result_chi2.get('interpretation')}")
        print("="*60)
        print()
        for index, result_autocorrelation in enumerate(result_correlations):
            print("="*60)
            print(f"Test d'autocorrellation lag = {lags[index]}")
            print("="*60)
            print(f"valeur d'autocorrélation : {round(result_autocorrelation.get('rho', 0), precision)}")
            print(f"{result_autocorrelation.get('interpretation')}")
            print("="*60)
            print()
        print("="*60)
        print("Test de Kolmogorov Smirnov")
        print("="*60)
        print(f"valeur critique : {round(result_ks.get('d_crit', 0), precision)}")
        print(f"distance max : {round(result_ks.get('d_max', 0), precision)}")
        print(f"{result_ks.get('interpretation')}")
        print("="*60)
        print()        

    return [result_shannon.get("interpretation", ""), result_chi2.get("interpretation", "")] + \
        [result_autocorrelation.get("interpretation", "") for result_autocorrelation in result_correlations] + \
        [result_ks.get("interpretation", "")]


def generer_tableau_tests(tests, resultats, fichier='resultat.txt'):
    """
    Génère un tableau formaté des tests statistiques et leurs résultats dans un fichier
    
    Parameters:
    tests (list): Liste des noms de tests
    resultats (list of list): Liste de listes de résultats, chaque sous-liste correspond à une ligne
    fichier (str): Nom du fichier de sortie (par défaut 'resultat.txt')
    """
    # Vérification que chaque sous-liste a la même longueur que tests
    for i, row in enumerate(resultats):
        if len(row) != len(tests):
            raise ValueError(f"La ligne {i} n'a pas le même nombre d'éléments que la liste des tests")
    
    # Calculer la largeur maximale pour chaque colonne
    largeurs = []
    for i, test in enumerate(tests):
        max_largeur = len(test)  # Commencer avec la largeur du nom du test
        for row in resultats:
            max_largeur = max(max_largeur, len(row[i]))
        largeurs.append(max_largeur)
    
    # Ouvrir le fichier en écriture
    with open(fichier, 'w', encoding='utf-8') as f:
        # En-tête du tableau avec les noms des tests
        header = "| " + " | ".join(test.ljust(largeurs[i]) for i, test in enumerate(tests)) + " |"
        separator = "|" + "|".join(["-" * (largeur + 2) for largeur in largeurs]) + "|"
        
        f.write(header + "\n")
        f.write(separator + "\n")
        
        # Lignes avec les résultats
        for row in resultats:
            values = "| " + " | ".join(val.ljust(largeurs[i]) for i, val in enumerate(row)) + " |"
            f.write(values + "\n")
    
    print(f"Tableau généré dans le fichier '{fichier}'")

##################################################
# Entropie de Shannon
##################################################
def Shannon(data: list[float], nb_data: int):
    """Effectue un test d'entropie de Shanon par octet

    Args:
        data (list[float]): liste des données normalisé a tester
        nb_data (int): nombre de donnée a tester
    """
    # etape de conversion en octet
    nb_occurence_octet = conversion_octet(data)

    # calcul des probabilité d'apparitions
    entropie = 0.0
    for key in nb_occurence_octet:
        # formule 1
        proba: float = nb_occurence_octet[key] / nb_data
        if proba > 0:
            # formule 2
            entropie -= proba * math.log2(proba)

    # ajout d'un ratio par rapport a l'entropie max possible
    # le ratio est le taux de dispertion des données
    entropie_max = 8.0
    ratio = entropie / entropie_max if entropie_max > 0 else 0

    return {
        "entropie": entropie,
        "ratio": ratio,
        "interpretation": _interpreter_entropie(ratio)
    }

def _interpreter_entropie(ratio):
    """Interprète le ratio d'entropie"""
    if ratio > 0.99:
        return "Excellent - Distribution très uniforme"
    elif ratio > 0.95:
        return "Bon - Distribution acceptable"
    elif ratio > 0.90:
        return "Moyen - Quelques biais détectés"
    else:
        return "Faible - Distribution non uniforme"


# =================================================================
# Test du Chi-2 (χ²)
# =================================================================

def chi2_critique(ddl, alpha=0.05):
    """
    Renvoie la valeur critique du chi² pour un degré de liberté donné.
    
    Paramètres:
    -----------
    ddl : int
        Degré de liberté (degrees of freedom)
    alpha : float, optional
        Seuil de significativité (par défaut 0.05 pour 5%)
    """
    return chi2.ppf(1 - alpha, ddl)



def Chi2(data: list[float], nb_data: int):    
    """effectue un test du Chi2 sur l'uniformité des octets

    Args:
        data (list[float]): liste des données normalisé a tester
        nb_data (int): nombre de donnée a tester
    """
    
    # etape de conversion en octet
    nb_occurence_octet = conversion_octet(data)

    frequence_theorique: float = nb_data / 256

    # calcul du Chi2 pratique
    chi2_calcule = 0.0
    for key in nb_occurence_octet:
        chi2_calcule += ( (nb_occurence_octet[key] - frequence_theorique)**2 / frequence_theorique )

    # calcul du Chi2 théorique avec 255 degrés de liberté
    ddl = 255
    chi2_theorique = chi2_critique(ddl)

    return {
        "chi2c": chi2_calcule,
        "chi2t": chi2_theorique,
        "interpretation": "Suit bien une lois Uniforme" if chi2_calcule<chi2_theorique else "Ne suit pas une loi Uniforme"
    }
    
# =================================================================
# Autocorrélation
# =================================================================
def autocorrelation(data: list[float], nb_data: int, lag: int):
    """vérifie si il y a une corrélation entre les données avec un décallage
    de lag

    Args:
        data (list[float]): liste des données normalisé a tester
        nb_data (int): nombre de donnée a tester
        lag (int): valeur du lag de décalage
    """
    moy = sum(data)/nb_data

    numerateur = 0
    denominateur = 0
    for i in range(nb_data-lag):
        data_sub_moy = data[i]-moy
        numerateur += (data_sub_moy) * (data[i+lag]-moy)
        denominateur += data_sub_moy**2
    for i in range(nb_data-lag, nb_data):
        denominateur += (data[i]-moy)**2
    
    rho = numerateur / denominateur
    
    interval_confiance = 1.96/math.sqrt(nb_data)
    
    return {
        "rho": rho,
        "interpretation": "non corrélation" if abs(rho)<interval_confiance else "corrélation"
    }


# =================================================================
# Test de Kolmogorov-Smirnov
# =================================================================
def kolmogorov_smirnov(data: list[float], nb_data: int):
    """permet de tester si les données sont uniformes ou non

    Args:
        data (list[float]): liste des données normalisé a tester
        nb_data (int): nombre de donnée a tester
    """
    # tri des données
    data = sorted(data)
    max_distance = 0

    for i in range(nb_data):
        x_i = data[i]
        f_empirique = (i + 1) / nb_data
        f_theorique = x_i

        distance = abs(f_empirique - f_theorique)
        if distance > max_distance:
            max_distance = distance
        
    # formule approximative
    d_critique_005 = 1.36 / math.sqrt(nb_data)
    
    return {
        "d_crit" : d_critique_005,
        "d_max": max_distance,
        "interpretation": "Les données sont bien de distribution uniforme" if max_distance < d_critique_005 else "les données ne sont pas de distribution uniforme"
    }



if __name__ == "__main__":
    # INITIALISATEURS
    mt = MersenneTwister(123)
    
    tests = [
        'Algorithme',
        'Shannon', 
        'Chi²', 
        'Corrélation-lag1', 
        'Corrélation-lag2', 
        'Corrélation-lag8', 
        'Corrélation-lag16', 
        'Kolmogorov-Smirnov'
    ]
    interpretations = []

    # DATA
    nb_data = 10000 # nombre de données de tests
    
    data = [mt.next_number() for _ in range(nb_data)]
    interpretations.append(["Mersenne Twister"] + effectuer_test(data))

    data = [BoxMuller() for _ in range(nb_data)]
    interpretations.append(["Box Muller"] + effectuer_test(data))

    data = linear_congruential_generator(9,2,1,3,nb_data)
    interpretations.append(["LCG"] + effectuer_test(data))

    data = BBS(nb_data)
    interpretations.append(["BBS"] + effectuer_test(data))



    generer_tableau_tests(tests, interpretations)

    


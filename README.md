Dans ce projet nous devons réaliser différents algorithmes de génération de nombre aléatoire :
- Linear congruential generator (LCG)
- Mersenne Twister (MT19937)
- ransformée de Box–Muller
- NIST SP (SP stands for ”special publication”) 800-90A DR-BG (Deterministic Random Bit Generators)
- Blum–Blum–Shub (BBS)
- Générateur système
- Construction XOR NRBG (Non-Random Bit Generator)


Ensuite nous devons réaliser des tests statistiques sur ces générateurs :
- Estimation d’entropie (Shannon) par octet
- Test du χ2 (chi-carré) pour l’uniformité des octets
- Autocorrélation (lags 1, 8, ... )
- Test de Kolmogorov–Smirnov (KS)

Ensuite nous devons réaliser au moins 2 attaques parmis : 
- Récupération de la graine LCG
- Reconstruction d’état MT19937
- Réutilisation de nonce en AES-CTR
- IV prévisible en AES-CBC
Pour chaque attaques, nous devons expliquer le fonctionnement de l'attaques dans le rapport
avec les points suivants : 
    - modèle de menace
    - hypothèse
    - algorithme
    - condition de succes
    - métriques et résultat


temps total : 7 séances

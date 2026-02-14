# Implémentation des Générateurs de Nombres Aléatoires et Analyse de la Qualité

Le hasard et la capacité à produire des nombres aléatoires sont au cœur des protocoles de sécurité informatique. Les nombres aléatoires servent à générer des clés secrètes, des nonces, des vecteurs d’initialisation ou des jetons CSRF. Une génération non sécurisée permettrait à un attaquant d’inférer ou de prédire des clés ou des jetons ultérieurs, compromettant ainsi la sécurité du système. Même si des constructions théoriques robustes existent, elles sont parfois mal mises en œuvre et lorsque la qualité de l’aléa est insuffisante, l’ensemble du système devient vulnérable.

Ainsi on souhaite réaliser une implémentation de différents algorithmes de génération de nombres aléatoires ainsi que deux attaques pédagogiques contre certains de ces algorithmes vulnérables.


## Table des matières

- [Aperçu](#aperçu)
- [Générateurs implémentés](#générateurs-implémentés)
- [Outils d'analyse](#outils-danalyse)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Tests statistiques](#tests-statistiques)
- [Attaques cryptographiques](#attaques-cryptographiques)
- [Structure du projet](#structure-du-projet)

## Aperçu

Ce projet est à titre pédagogique et les attaques réalisées sont interdites sur des systèmes réels

## Générateurs implémentés

### 1. Linear Congruential Generator (LCG)
**Fichier:** `LCG.py`

Générateur congruentiel linéaire utilisant la formule : `Xn+1 = (a × Xn + c) mod m`

```python
from LCG import linear_congruential_generator

sequence = linear_congruential_generator(m=9, a=2, c=1, Xo=3, length_of_sequence=7)
```

**Paramètres:**
- `m`: modulo (0 < m)
- `a`: multiplicateur (0 < a < m)
- `c`: incrément (0 ≤ c < m)
- `Xo`: valeur initiale (0 ≤ Xo < m)

### 2. Mersenne Twister (MT19937)
**Fichier:** `Mersenne_twister.py`

Implémentation du générateur Mersenne Twister avec période de 2^(19937-1).

```python
from Mersenne_twister import MersenneTwister

mt = MersenneTwister(seed=123)
random_number = mt.next_number()
```

### 3. Blum Blum Shub (BBS)
**Fichier:** `BBS.py`

Générateur cryptographiquement sécurisé basé sur le problème de la racine carrée modulaire.

```python
from BBS import BBS

sequence = BBS(length_of_sequence=10)
```

**Principe:** Xn+1 = Xn² mod M, où M = p × q (p, q nombres premiers ≡ 3 mod 4)

### 4. Hash-Based DRBG
**Fichier:** `hash_DRBG.py`

Générateur déterministe basé sur SHA-256, conforme aux standards NIST.

```python
from hash_DRBG import generer_hash_DRBG, seed

seedlen = 16
V = seed(seedlen)
C = seed(seedlen)
reseed_cpt = 1

output, V, reseed_cpt = generer_hash_DRBG(V, C, reseed_cpt, 
                                          reseed_interval=5, 
                                          seedlen=seedlen)
```

### 5. Box-Muller Transform
**Fichier:** `BoxMuller.py`

Transforme une distribution uniforme en distribution normale (gaussienne).

```python
from BoxMuller import BoxMuller

gaussian_number = BoxMuller()  # Loi N(0,1)
```

### 6. Non-Random Generator for Benchmarking (NRGB)
**Fichier:** `NRBG.py`

Combine plusieurs sources d'entropie (système, Mersenne Twister, BBS).

```python
from NRBG import NRGB

random_value = NRGB(bit_length=32)
```

## Outils d'analyse

### Tests statistiques
**Fichier:** `testsStatistiques.py`

Suite complète de tests pour évaluer la qualité des générateurs :

#### 1. Entropie de Shannon
Mesure la distribution des octets générés (valeur idéale : 8 bits).

#### 2. Test du Chi² (χ²)
Vérifie l'uniformité de la distribution des valeurs.

#### 3. Test d'autocorrélation
Détecte les corrélations entre valeurs successives avec différents décalages (lag 1, 2, 8, 16).

#### 4. Test de Kolmogorov-Smirnov
Compare la distribution empirique à une distribution uniforme théorique.

**Utilisation:**

```python
from testsStatistiques import effectuer_test, generer_tableau_tests
from Mersenne_twister import MersenneTwister

mt = MersenneTwister(123)
data = [mt.next_number() for _ in range(10000)]

# Effectuer les tests avec affichage
resultats = effectuer_test(data, precision=3, affichage=True)

# Générer un rapport
tests = ['Shannon', 'Chi²', 'Corrélation-lag1', 'Corrélation-lag2', 
         'Corrélation-lag8', 'Corrélation-lag16', 'Kolmogorov-Smirnov']
generer_tableau_tests(tests, [resultats], fichier='rapport.txt')
```

## Attaques cryptographiques

### Attaque sur LCG
**Fichier:** `LCG_attack.py`

Deux types d'attaques implémentées :

#### Cas 1 : Paramètres connus (a, c, m)
Remonte la séquence pour retrouver la graine initiale.

```python
from LCG_attack import attaque

graine_retrouvee = attaque(xn=dernier_nombre, a=585, c=899, m=1024, long_seq=8)
```

#### Cas 2 : Paramètres inconnus
Retrouve tous les paramètres (m, a, c) à partir d'au moins 4 sorties consécutives.

```python
from LCG_attack import attaque_cas2

sequence_observee = [...]  # Au moins 4 valeurs
graine = attaque_cas2(sequence_observee, n=8)
```

**Principe mathématique:**
- Calcul de m via PGCD de différences
- Extraction de a par inversion modulaire
- Déduction de c par substitution

### Attaque sur Mersenne Twister
**Fichier:** `Attaque_MT.py`

Inverse la fonction de tempering pour retrouver l'état interne.

```python
from Attaque_MT import untemper

etat_interne = untemper(sortie_observee)
```

**Implications:** Avec 624 sorties consécutives, l'état complet peut être récupéré et toutes les sorties futures prédites.

## Installation

### Prérequis
- Python 3.8+
- pip

### Dépendances

```bash
pip install scipy
```

### Clonage du projet

```bash
git clone https://github.com/mortdu1234/Generation_de_nombres_aleatoires.git
cd generateurs-aleatoires
```

## Utilisation

### Génération de nombres aléatoires

```python
# Mersenne Twister
from Mersenne_twister import MersenneTwister
mt = MersenneTwister(123)
print([mt.next_number() for _ in range(5)])

# LCG
from LCG import linear_congruential_generator
print(linear_congruential_generator(1024, 585, 899, 339, 10))

# BBS
from BBS import BBS
print(BBS(5))

# Distribution normale
from BoxMuller import BoxMuller
print([BoxMuller() for _ in range(5)])
```

### Analyse statistique complète

```bash
python testsStatistiques.py
```

Génère un fichier `resultat.txt` avec les résultats pour tous les générateurs testés.

### Démonstration d'attaques

```bash
# Attaque LCG
python LCG_attack.py

# Attaque Mersenne Twister
python Attaque_MT.py
```

## Structure du projet

```
.
├── LCG.py                    # Générateur congruentiel linéaire
├── LCG_attack.py             # Attaque sur LCG
├── Mersenne_twister.py       # Mersenne Twister MT19937
├── Attaque_MT.py             # Attaque sur MT
├── BBS.py                    # Blum Blum Shub
├── BoxMuller.py              # Transformation Box-Muller
├── hash_DRBG.py              # DRBG basé sur SHA-256
├── NRBG.py                   # Générateur combiné
├── system_generator.py       # Générateur système
├── testsStatistiques.py      # Suite de tests statistiques
└── README.md                 # Ce fichier
```

## Résultats des tests

Les tests statistiques montrent que :

- **Mersenne Twister** : Excellentes propriétés statistiques, mais vulnérable aux attaques par prédiction
- **BBS** : Très bonnes propriétés, cryptographiquement sécurisé mais lent
- **LCG** : Simple et rapide, mais faibles propriétés statistiques et facilement attaquable
- **Hash-DRBG** : Propriétés cryptographiques excellentes, recommandé pour usage sécurisé
- **Box-Muller** : Distribution gaussienne correcte pour simulations statistiques

## Avertissements

- Ces implémentations sont **à but éducatif uniquement**
- **NE PAS utiliser LCG ou MT pour la cryptographie** (facilement attaquables)
- Pour des applications de sécurité, utiliser `secrets` (Python) ou Hash-DRBG
- Les tests statistiques ne garantissent pas la sécurité cryptographique

## Références

Linear congruential generator
- https://en.wikipedia.org/wiki/Linear_congruential_generator (visité le 11/02/2026)
- https://rosettacode.org/wiki/Linear_congruential_generator (visité le 11/02/2026)

Mersenne Twister (MT19937)
- https://en.wikipedia.org/wiki/Mersenne_Twister (visité le 11/02/2026)
- https://www.youtube.com/watch?v=TF4PLUcJO5w : (visité le 11/02/2026)
- https://asecuritysite.com/primes/twister (visité le 11/02/2026)

Transformée de Box-Muller
- https://fr.wikipedia.org/wiki/M%C3%A9thode_de_Box-Muller (visité le 11/02/2026)
- https://fr-academic.com/dic.nsf/frwiki/1212323 (visité le 11/02/2026)

NIST SP 800-90A DR-BG
- https://en.wikipedia.org/wiki/NIST_SP_800-90A (visité le 11/02/2026)
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-90Ar1.pdf (visité le 11/02/2026)

Blum-Blum-Shub
- https://fr.wikipedia.org/wiki/Blum_Blum_Shub (visité le 11/02/2026)
- https://asecuritysite.com/encryption/blum (visité le 11/02/2026)

Générateur Système
- https://docs.python.org/3.12/library/os.html (visité le 11/02/2026)

Construction XOR NRBG
- https://csrc.nist.gov/csrc/media/events/random-bit-generation-workshop-2016/documents/presentations/sessioni-2-elaine-barker-presentation.pdf (visité le 11/02/2026)

Test de Shannon
- https://fr.wikipedia.org/wiki/Indice_de_Shannon (visité le 11/02/2026)

Test du Chi2
- https://numiqo.fr/tutorial/chi-square-test (visité le 11/02/2026)
- https://fr.wikipedia.org/wiki/Test_du_%CF%87%C2%B2 (visité le 11/02/2026)

Test d’autocorrélation
- https://fr.wikipedia.org/wiki/Test_de_Durbin-Watson (visité le 11/02/2026)

Test de Kolmogorov-Smirnov
- https://www.jybaudot.fr/Inferentielle/kolmogorov.html (visité le 11/02/2026)


## Contribution

- ROBERT Denis
- MAHE Noah
- ANDRINIRINA Gatien


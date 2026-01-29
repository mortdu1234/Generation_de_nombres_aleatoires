##############################################################
# coef de MT19937
##############################################################
w: int = 32   # nombre de bit des entier générés
n: int = 624  # nombre d'entier générer
m: int = 397  # décalage pour le twist

a = 0x9908B0DF  # coefficient matriciel

u = 11        
d = 0xFFFFFFFF

s = 7
b = 0x9D2C5680

t = 15
c = 0xEFC60000

l = 18

f = 1812433253  


MT = [0] * n
INDEX = 624

def init(seed: int):
    global MT, INDEX
    INDEX = n  
    MT[0] = seed & 0xFFFFFFFF
    
    for i in range(1, n):
        MT[i] = (f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i) & 0xFFFFFFFF


def twist():
    global MT, INDEX
    newMT = [0] * n
    for i in range(n):
        mti = MT[i]
        mti1 = MT[(i+1) % n]
        mtim = MT[(i+m) % n]
        
        Y = (mti & 0x80000000) | (mti1 & 0x7FFFFFFF)
        
        Ydecal = Y >> 1
        if Y & 1: 
            Ydecal = Ydecal ^ a
        
        newMT[i] = mtim ^ Ydecal
    
    MT = newMT
    INDEX = 0

def temper():
    global INDEX
    
    if INDEX >= n:
        twist()
    
    y = MT[INDEX]
    
    y = y ^ ((y >> u) & d)
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)
    
    INDEX += 1
    return y & 0xFFFFFFFF




reponse_seed_123 = [2991312382, 3062119789, 1228959102, 1840268610,
                    974319580, 2967327842, 2367878886, 3088727057,
                    3090095699, 2109339754, 1817228411, 3350193721,
                    4212350166, 1764906721, 2941321312, 2489768049,
                    2065586814, 601083951, 1684131913, 1722357280]

init(123)
print(f"i  : valeurCaculée   | valeurThéorique => egalité")
for i in range(10):
    test = temper()
    print(f"{i:2} : {test:15} | {reponse_seed_123[i]:15} => {test==reponse_seed_123[i]}")
class MersenneTwister:
    def __init__(self, seed: int): 
        """Initialiation de MersenneTwister avec la norme MT19937 pour 32 bits

        Args:
            seed (int): seed d'initialisation
        """
        self.w: int = 32   # nombre de bit des entier générés
        self.n: int = 624  # nombre d'entier générer
        self.m: int = 397  # décalage pour le twist

        self.a = 0x9908B0DF  # coefficient matriciel

        self.u = 11        
        self.d = 0xFFFFFFFF

        self.s = 7
        self.b = 0x9D2C5680

        self.t = 15
        self.c = 0xEFC60000

        self.l = 18

        self.f = 1812433253  


        self.MT = [0] * self.n
        self.INDEX = self.n  
        self.MT[0] = seed & 0xFFFFFFFF
        
        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i) & 0xFFFFFFFF

    def twist(self):
        """effectue un twist pour regénérer une nouvelle matrice
        """
        newMT = [0] * self.n
        for i in range(self.n):
            mti = self.MT[i]
            mti1 = self.MT[(i+1) % self.n]
            mtim = self.MT[(i+self.m) % self.n]
            
            Y = (mti & 0x80000000) | (mti1 & 0x7FFFFFFF)
            
            Ydecal = Y >> 1
            if Y & 1: 
                Ydecal = Ydecal ^ self.a
            
            newMT[i] = mtim ^ Ydecal
        
        self.MT = newMT
        self.INDEX = 0

    def temper(self):      
        """effectue la génération d'un nombre aléatoire a partir de la matrice

        Returns:
            int: nombre aléatoire généré
        """
        if self.INDEX >= self.n:
            self.twist()
        
        y = self.MT[self.INDEX]
        
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        
        self.INDEX += 1
        return y & 0xFFFFFFFF

    def next_number(self) -> int:
        """(alias) renvois un nombre aléatoire généré par MersenneTwister

        Returns:
            int: nombre aléatoire généré
        """
        return self.temper()

    

if __name__ == "__main__":
    mersenne = MersenneTwister(123)
    reponse_seed_123 = [2991312382, 3062119789, 1228959102, 1840268610,
                        974319580, 2967327842, 2367878886, 3088727057,
                        3090095699, 2109339754, 1817228411, 3350193721,
                        4212350166, 1764906721, 2941321312, 2489768049,
                        2065586814, 601083951, 1684131913, 1722357280]
    print("tests pour seed")
    print(f" i :   valeurCaculée | valeurThéorique => egalité")
    for i in range(10):
        test = mersenne.next_number()
        print(f"{i:2} : {test:15} | {reponse_seed_123[i]:15} => {test==reponse_seed_123[i]}")
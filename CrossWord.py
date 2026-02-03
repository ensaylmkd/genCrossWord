from DicoPrefixeTree import *

PATH= "genCrossWord/Fr_Simple.txt"
CASENOIR="."

class Grille:
    """Classe représentant une grille de mots croisés de taille NxN"""
    
    def __init__(self, taille,path):
        self.taille = taille
        self.grille = [['' for _ in range(taille)] for _ in range(taille)]
        self.dpt :DicoPrefixeTree = DicoPrefixeTree(path)
    
    def generate(self):
        self.generateFirstLine()
        for i in range(self.taille-1):
            self.generateNextLine(i+1)
        # while i < self.taille:
        #     i += self.generateNextLine()
    
    def generateFirstLine(self): # refaire tres tres brouillon 
        w = self.dpt.random_word(self.taille)
        while len(w)< self.taille: # refaire tres tres brouillon 
            w+=CASENOIR
        
        for i, l in enumerate(w):
            self.grille[0][i]=l
    
    def generateNextLine(self,i):
        print("début data analyse")
        data=[self.dpt.stat_prefixe(self.readPrefixeColumn(y),self.taille) for y in range(self.taille)]
        print("la data: ",data)
        data = [sorted(elt.items(), key=lambda x: x[1], reverse=True) for elt in data]
        word= self.buildWord(data)
        
        for y, l in enumerate(word):
            self.grille[i][y] = l
        
        self.afficher()

        return 1
    
    def readPrefixeColumn(self,n):
        assert n>=0 or n <= self.taille-1, "numero colonne nom valide"
        pref=""
        for i in range(self.taille):
            l=self.grille[i][n]
            pref += l
            if l == ".":
                pref=""
        return pref
    
    def buildWord(self,data):
        '''data : liste tels que [[(lettre, frequence),...],...]'''
        word = self._recBuildWord(data,"")
        return word

    def _recBuildWord(self,data,w):
        if len(w) == len(data) or self.dpt.is_word(w):
            return w
        
        columdData= [letter for letter,y in data[len(w)-1]]
        statPrefixe = self.dpt.stat_prefixe(w,self.taille)
        lineData = [x for x,y in list(sorted(statPrefixe.items(), key=lambda x: x[1], reverse=True))]

        for l in lineData:
            if l in columdData:
                if self._recBuildWord(data,w+l) != -1:
                    print("lettre choisi:",l)
                    return self._recBuildWord(data,w+l)
        return -1
        
    def afficher(self):
        """Affiche la grille"""
        for ligne in self.grille:
            print(' '.join(ligne))

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
        i=1
        while i < self.taille:
            res = self.generateNextLine(i)
            i += res
            if res == -1:
                print("backtrack ligne ",i+1)
                self.backtrack(i)
                return -1
    
    def generateFirstLine(self): # refaire tres tres brouillon 
        w = self.dpt.random_word(self.taille)
        while len(w)< self.taille: # refaire tres tres brouillon 
            w+=CASENOIR
        
        for i, l in enumerate(w):
            self.grille[0][i]=l
    
    def generateNextLine(self,i):

        print("début data analyse")
        data=[self.dpt.stat_prefixe(self.readPrefixeColumn(y),self.taille) for y in range(self.taille)]
        data = [list(sorted(elt.items(), key=lambda x: x[1], reverse=True)) for elt in data]
        print("la data: ",data)
        
        infoLine = self.readLine(i)
        index = 0
        words=[]
        for l in infoLine:
            words.append(self.buildWord(data[i:i+l],l))
            index += l + 1
        
        if  -1 in words:
            print("impossible de generer la ligne ",i+1)
            return -1
        
        for y, l in enumerate(".".join(words)):
            self.grille[i][y] = l
        return 1
    
    def readLine(self,n):
        assert n>=0 or n <= self.taille-1, "numero colonne nom valide"
        res=[]
        cpt = 0
        for i in range(self.taille):
            print(i,": ", self.grille[n][i])
            if self.grille[n][i] != CASENOIR:
                cpt +=1
            else:
                res.append(cpt)
                cpt = 0
        res.append(cpt)
        return res
    
    def readPrefixeColumn(self,n):
        assert n>=0 or n <= self.taille-1, "numero colonne nom valide"
        pref=""
        for i in range(self.taille):
            l=self.grille[i][n]
            pref += l
            if l == ".":
                pref=""
        return pref
    
    def buildWord(self,data,taille):
        '''data : liste tels que [[(lettre, frequence),...],...]'''
        word = self._recBuildWord(data,"",taille)
        # if word == -1:
        #     word = CASENOIR * self.taille
        return word

    def _recBuildWord(self,data,w,taille):
        if len(w) == len(data) or (self.dpt.is_word(w) and len(w)==taille):
            return w
        
        columdData= [letter for letter,y in data[len(w)-1]]

        statPrefixe = self.dpt.stat_prefixe(w,taille)
        lineData = [x for x,y in list(sorted(statPrefixe.items(), key=lambda x: x[1], reverse=True))]

        for l in lineData:
            if len(w) == 0 :
                print("info: ",columdData,lineData)
            if l in columdData:
                if self._recBuildWord(data,w+l,taille) != -1:
                    return self._recBuildWord(data,w+l,taille)
        return -1
    
    def backtrack(self,i):
        print("avant backtrack ",i)
        self.afficher()
        for y in range(self.taille):
            self.grille[i][y]=''
        CPGC = self.get_CPGC()

        data=[self.dpt.stat_prefixe(self.readPrefixeColumn(y),self.taille) for y in range(self.taille)]
        data = [list(sorted(elt.items(), key=lambda x: x[1], reverse=True)) for elt in data]

        data[CPGC]=list(self.dpt.stat_prefixe(self.readPrefixeColumn(CPGC),i+1).items())
        print("le CPGC est la colonne ",CPGC)
        print("sa data est:\n ",data[CPGC])
        word = self.buildWord(data,self.taille)
        print("apres backtrack ",word)

        if word == -1:
            print("impossible de generer la ligne ",i)
            self.backtrack(i-1)
            return -1

        for y, l in enumerate(word):
            self.grille[i][y] = l
        self.grille[i+1][CPGC] = "."


    def get_CPGC(self):
        '''Colone avec la Plus Grosse Contraintes'''
        data=[self.dpt.nb_words(self.readPrefixeColumn(y),self.taille) for y in range(self.taille)]
        CPGC = min(data)
        indexColonne = data.index(CPGC)
        return indexColonne

        
    def afficher(self):
        """Affiche la grille"""
        for ligne in self.grille:
            print(' '.join(ligne))

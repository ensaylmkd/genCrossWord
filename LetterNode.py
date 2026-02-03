# redaction cheminement de penser : 
# j'ai hésité entre 
# 1) une variable de fin de mot , 
# 2) un charactere collé en str(ex:"A\0")
# 3) un autre noeud "\0", 
# j'ai opté pour la 3eme option car je trouve plus propre mais surement moins opti 
# idée : creer un seul noeud fin de mot pour que chaque fin de mot pointe sur lui 

class LetterNode:
    def __init__(self, letter='\0', profondeur = 0):
        self.letter : str = letter
        self.childLetters : dict[str:LetterNode] = {}
        self.len2nbWords : dict[int:int] = {}
        self.profondeur : int = profondeur
    
    def get_child(self):
        return self.childLetters

    def searchChild(self,letter):
        return self.childLetters.get(letter,None)
    
    def addChildLetter(self,letter:str, deep :int):
        if not (self.searchChild(letter)):
            self.childLetters[letter] = LetterNode(letter, deep)

    def _countNbWords(self):
        l2nb = {}
        if self.letter == "\0":
            l2nb = { self.profondeur: 1 }
        else:
            for letter in self.childLetters.keys():
                cNode : LetterNode = self.childLetters.get(letter)
                for key in cNode.get_l2nbWords().keys():
                    l2nb[key] = l2nb.get(key,0) + cNode.len2nbWords.get(key,0)
        return l2nb

    def get_l2nbWords(self):
        if self.len2nbWords == {}:
            self.len2nbWords = self._countNbWords()
        return self.len2nbWords

    def get_nbWordOfLen(self,n):
        dic = self.get_l2nbWords()
        cpt = 0
        for i in range(n+1):
            cpt += dic.get(i,0)
        return cpt
    
    def stat(self,n):
        '''
        renvoie {lettre enfant : nombre de mot pour longueur max n@}

        :param n: longueur max
        '''
        res={}
        for c in self.childLetters.keys():
            if self.childLetters[c].get_nbWordOfLen(n) and c != "\0" : 
                res[c]= self.childLetters[c].get_nbWordOfLen(n)
        return res
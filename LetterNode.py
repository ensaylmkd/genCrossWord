# redaction cheminement de penser : 
# j'ai hésité entre 
# 1) une variable de fin de mot , 
# 2) un charactere collé en str(ex:"A\0")
# 3) un autre noeud "\0", 
# j'ai opté pour la 3eme option car je trouve plus propre mais surement moins opti 
# idée : creer un seul noeud fin de mot pour que chaque fin de mot pointe sur lui 

class LetterNode:
    def __init__(self, letter='\0'):
        self.letter : str = letter
        self.childLetters : dict[str:LetterNode] = {}
        self.len2nbWords : dict[int:int] = {}

    def searchChild(self,letter):
        return self.childLetters.get(letter,None)
    
    def addChildLetter(self,letter:str):
        if not (self.searchChild(letter)):
            self.childLetters[letter] = LetterNode(letter)

    def _countNbWords(self):
        l2nb = {}
        if self.letter == "\0":
            l2nb = { -1:1 }
        else:
            for letter in self.childLetters.keys():
                cNode : LetterNode = self.childLetters.get(letter)
                for key in cNode.get_l2nbWords().keys():
                    l2nb[key+1] = l2nb.get(key+1,0) + cNode.len2nbWords.get(key,0)
        return dict(sorted(l2nb.items(), key=lambda x: x[1], reverse=True))

    def get_l2nbWords(self):
        if self.len2nbWords == {}:
            self.len2nbWords = self._countNbWords()
        return self.len2nbWords


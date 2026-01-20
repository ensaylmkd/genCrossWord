from LetterNode import LetterNode 

class ArbrePrefixe:
    def __init__(self,pathFile):
        self.racine:LetterNode = LetterNode("")
        self._initFile(pathFile)
        
    def _initFile(self,file):
        with open(file, 'r') as f:
                for line in f:
                    p = self.racine
                    line = line.strip()
                    for letter in line:
                        p.addChildLetter(letter)
                        p = p.searchChild(letter)
                    p.addChildLetter("\0")
        f.close()
    
        
    

        
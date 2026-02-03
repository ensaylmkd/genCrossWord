from LetterNode import LetterNode
import random 

class DicoPrefixeTree:
    
    def __init__(self, pathFile: str = None):
        self.racine: LetterNode = LetterNode("")
        
        if pathFile:
            self._initFile(pathFile)
    
    def _initFile(self, file: str) -> None:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.insert(word.upper())
            f.close()
        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")
    
    def insert(self, word: str) -> None:
        node = self.racine
        w=word.upper()
        for i  in range(len(w)):
            node.addChildLetter(w[i],i+1)
            node = node.searchChild(w[i])
        node.addChildLetter('\0',len(w))
    
    def is_word(self, word: str) -> bool:
        node = self.racine
        for letter in word.upper():
            node = node.searchChild(letter)
            if node is None:
                return False
        return node.searchChild('\0') is not None
    
    def is_prefixe(self, prefixe: str):
        node = self.racine
        for letter in prefixe.upper():
            node = node.searchChild(letter)
            if node is None:
                return False
        return True
    
    def l2nb_prefixe(self, prefixe: str):
        if not self.is_prefixe(prefixe.upper()):
            return None
        node = self.racine
        for letter in prefixe.upper():
            node = node.searchChild(letter)
        data = node.get_l2nbWords()
        return data
    
    def stat_prefixe(self, prefixe: str,n: int): # regarder stat, fonction a rename 
        if not self.is_prefixe(prefixe.upper()):
            return {}
        node = self.racine
        for letter in prefixe.upper():
            node = node.searchChild(letter)
        
        data = node.stat(n)
        return data
    
    def random_word(self,n):
        node = self.racine
        word=""
        for _ in range(n):
            if not list(self.stat_prefixe(word,n).keys()):
                return word
            letter = random.choice(list(self.stat_prefixe(word,n).keys()))
            word+=letter
            node = node.searchChild(letter)
        return word

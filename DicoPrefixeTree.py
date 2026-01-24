from LetterNode import LetterNode

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
        for letter in word.upper():
            node.addChildLetter(letter)
            node = node.searchChild(letter)
        node.addChildLetter('\0')
    
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
    
    def l2nb_stat_with_prefixe(self, prefixe: str):
        if not self.is_prefixe(prefixe.upper()):
            return None
        node = self.racine
        for letter in prefixe.upper():
            node = node.searchChild(letter)
        data = node.get_l2nbWords()
        return data
    

"""
testMain.py
Test file for DicoPrefixeTree class
Tests insertion, word search, prefix search, and file loading functionality
"""

from DicoPrefixeTree import DicoPrefixeTree


def test_basic_insertion_and_search():
    """Test basic word insertion and word search"""
    print("=" * 60)
    print("TEST 1: Basic Insertion and Word Search")
    print("=" * 60)
    
    tree = DicoPrefixeTree()
    
    # Insert some test words
    words = ["apple", "app", "application", "apply", "banana", "band", "cat", "car"]
    for word in words:
        tree.insert(word)
        print(f"✓ Inserted: '{word}'")
    
    print("\nSearching for words:")
    # Test word search
    test_words = ["apple", "app", "appl", "banana", "ban", "cat", "car", "dog", "x"]
    for word in test_words:
        result = tree.is_word(word)
        symbol = "✓" if result else "✗"
        print(f"{symbol} is_word('{word}'): {result}")
    
    print()


def test_prefix_search():
    """Test prefix search functionality"""
    print("=" * 60)
    print("TEST 2: Prefix Search")
    print("=" * 60)
    
    tree = DicoPrefixeTree()
    
    words = ["hello", "help", "helper", "world", "word", "work", "abc", "ab"]
    for word in words:
        tree.insert(word)
    
    print(f"Inserted words: {words}\n")
    print("Testing prefix search:")
    
    prefixes = ["hel", "wor", "ab", "abc", "help", "xyz", "h", ""]
    for prefix in prefixes:
        result = tree.is_prefixe(prefix)
        symbol = "✓" if result else "✗"
        print(f"{symbol} is_prefixe('{prefix}'): {result}")
    
    print()


def test_file_loading():
    """Test loading words from file"""
    print("=" * 60)
    print("TEST 3: File Loading")
    print("=" * 60)
    
    filepath = "genCrossWord/Fr_Simple.txt"
    
    try:
        tree = DicoPrefixeTree(filepath)
        print(f"✓ Successfully loaded dictionary from '{filepath}'")
        
        # Test some common French words
        test_words = ["le", "de", "et", "un", "chat", "maison", "soleil"]
        print("\nSearching in loaded dictionary:")
        for word in test_words:
            result = tree.is_word(word)
            symbol = "✓" if result else "✗"
            print(f"{symbol} is_word('{word}'): {result}")
        
    except Exception as e:
        print(f"✗ Error loading file: {e}")
    
    print()


def test_edge_cases():
    """Test edge cases"""
    print("=" * 60)
    print("TEST 4: Edge Cases")
    print("=" * 60)
    
    tree = DicoPrefixeTree()
    
    # Test with single character words
    tree.insert("a")
    tree.insert("b")
    tree.insert("ab")
    
    print("Testing single character and short words:")
    test_cases = [("a", True), ("b", True), ("ab", True), ("abc", False), ("", False)]
    for word, expected in test_cases:
        result = tree.is_word(word)
        symbol = "✓" if result == expected else "✗"
        print(f"{symbol} is_word('{word}'): {result} (expected: {expected})")
    
    print("\nTesting prefix search on short words:")
    prefix_cases = [("a", True), ("b", True), ("ab", True), ("abc", False)]
    for prefix, expected in prefix_cases:
        result = tree.is_prefixe(prefix)
        symbol = "✓" if result == expected else "✗"
        print(f"{symbol} is_prefixe('{prefix}'): {result} (expected: {expected})")
    
    print()


def test_duplicate_insertion():
    """Test inserting duplicate words"""
    print("=" * 60)
    print("TEST 5: Duplicate Insertion")
    print("=" * 60)
    
    tree = DicoPrefixeTree()
    
    word = "test"
    tree.insert(word)
    tree.insert(word)  # Insert same word again
    tree.insert(word)  # And again
    
    print(f"Inserted '{word}' three times")
    result = tree.is_word(word)
    print(f"✓ is_word('{word}'): {result}")
    print("(Should still be True - duplicates handled correctly)")
    
    print()


def test_case_sensitivity():
    """Test case sensitivity"""
    print("=" * 60)
    print("TEST 6: Case Sensitivity")
    print("=" * 60)
    
    tree = DicoPrefixeTree()
    
    tree.insert("Hello")
    tree.insert("world")
    
    print("Inserted: 'Hello', 'world'\n")
    print("Testing case sensitivity:")
    
    test_cases = ["Hello", "hello", "HELLO", "world", "World"]
    for word in test_cases:
        result = tree.is_word(word)
        print(f"✓ is_word('{word}'): {result}")
    
    print()


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "DicoPrefixeTree Test Suite" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    test_basic_insertion_and_search()
    test_prefix_search()
    #test_file_loading()
    test_edge_cases()
    test_duplicate_insertion()
    test_case_sensitivity()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
    print("\n")
    tree = DicoPrefixeTree()
    
    words = ["hello", "help", "helper", "world", "word", "work", "abc", "ab"]
    for word in words:
        tree.insert(word)
    print(tree.l2nb_stat_with_prefixe("h"))


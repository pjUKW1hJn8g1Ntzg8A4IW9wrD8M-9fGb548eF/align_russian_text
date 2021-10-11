
from align_russian_text import TextHandler, WordHandler
from align_russian_text import GRAMMATICAL_RULES, ALPHABET, VOWELS, CONSONANTS
from align_russian_text import vowels_and_consonats, special_symbols


class TestGrammaticRules:
    def test_vowels_and_consonats(self):
        assert vowels_and_consonats(['а', 'б'], ['ё', 'й', 'к']) is True
        assert vowels_and_consonats(['э', 'ъ'], ['ц', 'е']) is False
        assert vowels_and_consonats(['э', 'й', 'л'], ['и', 'е']) is False

    def test_special_symbols(self):
        assert special_symbols(['к', 'о'], ['р', 'ы', 'т', 'о']) is True
        assert special_symbols(['к', 'о', 'р'], ['ы', 'т', 'о']) is False
        assert special_symbols(['к', 'о', 'р', 'ы'], ['т', 'о']) is True

        assert special_symbols(['т', 'ы', 'л'], ['ь', 'н', 'ы', 'й']) is False
        assert special_symbols(['т', 'ы', 'л', 'ь'], ['н', 'ы', 'й']) is True

        assert special_symbols(['б', 'о'], ['й', 'л', 'е', 'р']) is False
        assert special_symbols(['б', 'о', 'й'], ['л', 'е', 'р']) is True

        assert special_symbols(['о', 'б'], ['ъ', 'ё', 'м']) is False
        assert special_symbols(['о', 'б', 'ъ'], ['ё', 'м']) is True


class TestWordHandler:
    pass

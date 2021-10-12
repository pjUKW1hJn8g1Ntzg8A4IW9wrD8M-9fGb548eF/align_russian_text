
from collections import deque
from align_russian_text import TextHandler, WordHandler
from align_russian_text import GRAMMATICAL_RULES, ALPHABET, VOWELS, CONSONANTS
from align_russian_text import vowels_and_consonats, special_symbols, common_symbols


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

    def test_common_symbols(self):
        assert common_symbols(['п', 'р', 'о', 'п', 'е', 'л'], ['л', 'е', 'р']) is True
        assert common_symbols(['п', 'р', 'о', 'п', 'е'], ['л', 'л', 'е', 'р']) is False
        assert common_symbols(['п', 'р', 'о', 'п'], ['е', 'л', 'л', 'е', 'р']) is False
        assert common_symbols(['п', 'р', 'о'], ['п', 'е', 'л', 'л', 'е', 'р']) is True

        assert common_symbols(['п', 'р', 'о', 'с'], ['м', 'о', 'т', 'р']) is True


class TestWordHandler:
    def test_calc_word_begin(self):
        w = WordHandler([',', ' ', 'п', 'р', 'о', 'п', 'е', 'л', 'л', 'е', 'р'], deque(), pivot=3)

        assert w.word_begin == -1
        w._calc_word_begin()

        assert w.word_begin == 2

    def test_move_whole_word(self):
        buffer = [',', ' ', 'п', 'р', 'о', 'п', 'е', 'л', 'л', 'е', 'р']
        tmp_buf = deque()
        w = WordHandler(buffer, tmp_buf, pivot=3)
        w._calc_word_begin()

        assert len(w.tmp_buf) == 0

        w._move_whole_word()
        assert buffer == [',', ' ']
        assert list(tmp_buf) == ['п', 'р', 'о', 'п', 'е', 'л', 'л', 'е', 'р']

    def test_transit_word(self):
        buffer = [',', ' ', 'п', 'р', 'о', 'п', 'е', 'л', 'л', 'е', 'р']
        tmp_buf = deque()
        tmp_buf.append(".")

        w = WordHandler(buffer, tmp_buf, pivot=8)
        w._calc_word_begin()
        w._transit_word()

        assert buffer == [',', ' ', 'п', 'р', 'о', 'п', 'е', 'л', '-']
        assert list(tmp_buf) == ['л', 'е', 'р', '.']

    def test_handle(self):
        buffer = [',', ' ', 'п', 'р', 'о', 'п', 'е', 'л', 'л', 'е', 'р']
        tmp_buf = deque([';'])

        w = WordHandler(buffer, tmp_buf, pivot=9)
        w.handle()

        assert buffer == [',', ' ', 'п', 'р', 'о', 'п', 'е', 'л', '-']
        assert list(tmp_buf) == ['л', 'е', 'р', ';']

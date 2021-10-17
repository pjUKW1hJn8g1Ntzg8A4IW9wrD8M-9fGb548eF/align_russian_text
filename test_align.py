
from collections import deque
from align_russian_text import TextHandler, WordHandler, DEFAULT_PIVOT
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


class TestTextHandler:
    def test_create(self):
        txt_len = 100
        term_size = 45
        h = TextHandler(txt_len=txt_len, term_size=term_size)

        assert h.term_size == term_size
        assert h.txt_len == txt_len
        assert h.buffer == []
        assert isinstance(h.tmp_buf, deque)
        assert h.pivot == DEFAULT_PIVOT
        assert h.need_to_write is False

    def test_property(self):
        h = TextHandler(txt_len=100, term_size=10)
        h.buffer.extend(['э', 'ю', 'я', 'к', 'у', 'ц'])
        assert h.enough_space is True

        h.buffer.extend(['э', 'ю', 'у'])
        assert h.enough_space is True

        h.buffer.append('м')
        assert h.enough_space is False

    def test_clean_up(self):
        h = TextHandler(txt_len=100, term_size=10)
        h.buffer.extend(['э', 'ю', 'я', 'к', 'у', 'ц'])
        h.tmp_buf.append('у')
        h.pivot = 4
        h.need_to_write = True

        buf = h.buffer

        h._clean_up()

        assert buf is h.buffer
        assert len(h.tmp_buf) == 0
        assert h.buffer == ['у']
        assert h.pivot == DEFAULT_PIVOT
        assert h.need_to_write is False

    def test_got_eof(self):
        pass

    class TestDecideWhatToDo:
        def test_char_is_letter(self):
            h = TextHandler(txt_len=100, term_size=10)
            h.buffer.extend([',', ' ', 'п', 'р', 'о', 'п', 'е', 'л', 'л'])

            h._decide_what_to_do('е')
            assert h.need_to_write is False
            assert h.pivot == 9
            assert h.buffer[-1] == 'е'
            assert len(h.tmp_buf) == 0

            h._decide_what_to_do('р')
            assert h.need_to_write is False
            assert h.pivot == 9
            assert h.buffer[-1] == 'р'
            assert len(h.tmp_buf) == 0

            h._decide_what_to_do(' ')
            assert h.need_to_write is True
            assert h.pivot == 9
            assert h.buffer[-1] == '-'
            assert list(h.tmp_buf) == ['л', 'е', 'р', ' ']

        def test_char_is_not_letter(self):
            h = TextHandler(txt_len=100, term_size=10)
            h.buffer.extend(['п', 'р', 'о', 'п', 'е', 'л', 'л', 'е', 'р'])

            h._decide_what_to_do(',')
            assert h.need_to_write is True
            assert h.pivot == DEFAULT_PIVOT
            assert h.buffer[-1] == ','
            assert len(h.tmp_buf) == 0

            # test when last char is a space symbol
            h = TextHandler(txt_len=100, term_size=10)
            h.buffer.extend(['п', 'р', 'о', 'п', 'е', 'л', 'л', 'е', 'р'])
            h._decide_what_to_do('\n')
            assert h.need_to_write is True
            assert h.pivot == DEFAULT_PIVOT
            assert h.buffer[-1] == 'р'
            assert len(h.tmp_buf) == 0

    def test_handle(self):
        pass

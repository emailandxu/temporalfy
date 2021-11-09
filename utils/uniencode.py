from functools import lru_cache
class UnicodeVocabMapping():
    def __init__(self, chars):
        vocab_cnt = {}
        for char in chars:
            cnt = vocab_cnt.get(char, 0)
            cnt += 1
            vocab_cnt[char] = cnt

        vocab = list(vocab_cnt.keys())
        vocab.sort(key = lambda char: vocab_cnt[char], reverse=True)

        self.vocab = vocab

    @property
    @lru_cache(maxsize=1)
    def unicode_chars(self):
        control_chars_offset = 100

        unicode_start = control_chars_offset
        unicode_end = len(self.vocab) + control_chars_offset

        return [chr(i) for i in range(unicode_start, unicode_end)]

    def to_unicode(self, text):
        return "".join([self.unicode_chars[self.vocab.index(char)] for char in text])

    def from_unicode(self, text):
        try:
            return " ".join([self.vocab[ self.unicode_chars.index(char) ] for char in text])
        except IndexError as e:
            raise ValueError
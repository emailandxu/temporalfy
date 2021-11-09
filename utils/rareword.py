from typing import Set
from Levenshtein import distance

def neibor(index, text, neibor_radius):
    """given radius, get neibor sub-string"""
    left, right  = index - neibor_radius, index + neibor_radius
    left = max(0, left)
    right = min(len(text), right)
    return text[left:right ]

def cer(hypo, label):
    """compute charater error rate"""
    return distance(hypo, label) / len(label)

class FilterBothRareWord:
    """Tool class to compute the proper rare words, call it as a function.

    It will find out the rare words appears in hypo, label strings both up 'word_count_threhold' times.

    And the rare words will be filtered twice. One is filtered by character word error rate by 'neighbor_cer_threhold' within the range defined by 'neibor_raius'.

    Another is filtered by the words distance which means adjoint rare words closer than 'word_distance_threhold' will be not taken account.
"""
    def __init__(self, hypo, label, word_count_threhold=1, word_distance_threhold=5, neighbor_cer_threhold=0.5, neibor_radius=15) -> None:
        self.hypo = hypo
        self.label = label
        self.word_count_threhold = word_count_threhold
        self.word_distance_threhold = word_distance_threhold
        self.neighbor_cer_threhold = neighbor_cer_threhold
        self.neibor_radius = neibor_radius

    def get_rare_word(self) -> Set[str]:
        label_word_counter = {}

        for char in self.label:
            cnt = label_word_counter.get(char, 0)
            cnt += 1
            label_word_counter[char] = cnt

        label_rares = set(map(lambda x:x[0], filter(lambda x:x[1] == 1,  label_word_counter.items())) )

        hypo_word_counter = {}

        for char in self.hypo:
            cnt = hypo_word_counter.get(char, 0)
            cnt += 1
            hypo_word_counter[char] = cnt

        hypo_rares = set(map(lambda x:x[0], filter(lambda x:x[1] <= self.word_count_threhold,  hypo_word_counter.items())) )
        return label_rares.intersection(hypo_rares)

    def filter_by_word_distance(self, word_index_pairs_in_label):
        assert len(word_index_pairs_in_label) > 1
        filtered_l = []
        for (w0, w0i), (w1, w1i) in zip(word_index_pairs_in_label[:-1], word_index_pairs_in_label[1:]):
            distance = w1i - w0i
            if distance > self.word_distance_threhold:
                filtered_l.append((w0, w0i))
        filtered_l.append((w1, w1i))
        return filtered_l

    def filter_by_neighbor_cer_between_hypo_label(self, word_index_pairs_in_label):
        assert len(word_index_pairs_in_label) > 1

        filtered_l = []

        for w, li in word_index_pairs_in_label:
            hi = self.hypo.index(w)
            h_neibor, l_neibor = neibor(hi, self.hypo, self.neibor_radius), neibor(li, self.label, self.neibor_radius)
            if cer(h_neibor, l_neibor) > self.neighbor_cer_threhold:
                continue
            else:
                filtered_l.append((w, li))
        return filtered_l

    def __call__(self):
        """return word index pair in hypo, and in label"""
        rare_words = self.get_rare_word()
        word_index_pairs_in_label = [ (w, self.label.index(w) ) for w in rare_words]
        word_index_pairs_in_label = sorted(word_index_pairs_in_label, key=lambda x:x[1]) # before filter must sort

        word_index_pairs_in_label = self.filter_by_word_distance(word_index_pairs_in_label)
        word_index_pairs_in_label = self.filter_by_neighbor_cer_between_hypo_label(word_index_pairs_in_label)

        word_index_pairs_in_hypo = [ (w, self.hypo.index(w)) for w, _ in word_index_pairs_in_label ]

        return word_index_pairs_in_hypo, word_index_pairs_in_label

if __name__ == "__main__":
    hypo = open("./data/4-refOut.txt", "r").read().replace(" ", "")
    label = open("./data/4-hypOut.txt", "r").read().replace(" ", "")
    word_index_pairs_in_hypo, word_index_pairs_in_label = FilterBothRareWord(hypo, label)()
    print(word_index_pairs_in_hypo, word_index_pairs_in_label, sep="\n")
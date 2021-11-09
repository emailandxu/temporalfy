from typing import Generator
from utils.align import  Diff
from utils.rareword import FilterBothRareWord
import argparse

def get_substr_by_indexs(indexs, text):
    """given indexs, it will output a sequence of substrs from left to right"""
    leftbound = 0
    rightbound = len(text)
    windows_indexs = [leftbound, *indexs, rightbound]

    for left_ptr, right_ptr in zip(windows_indexs[:-1], windows_indexs[1:]):
        yield text[left_ptr:right_ptr]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('--hyp',  help='hypothesis file path')
    parser.add_argument('--ref',  help='reference file path')

    args = parser.parse_args()

    hypo = open(args.hyp, "r").read().replace(" ", "")
    label = open(args.ref, "r").read().replace(" ", "")

    hypo_word_index_pairs, label_word_index_pairs = FilterBothRareWord(hypo, label)()

    h_indexs = [ i for _, i in hypo_word_index_pairs]
    l_indexs = [i for _, i in label_word_index_pairs]

    whole_aligns = []
    for h_substr, l_substr in zip( get_substr_by_indexs(h_indexs, hypo), get_substr_by_indexs(l_indexs, label) ):
        # print(h_substr, l_substr, sep=" @@@@ ")
        aligns = Diff(h_substr, l_substr).aligns
        whole_aligns.append(aligns)

    from itertools import  chain
    squzzed_aligns = list(chain(*whole_aligns))
    print(Diff.make_aligns_json(squzzed_aligns))

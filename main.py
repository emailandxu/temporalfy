from itertools import  chain
from utils.align import  Diff
from utils.rareword import FilterBothRareWord
import argparse
from utils.uniencode import UnicodeVocabMapping
import re

def get_substr_by_indexs(indexs, text):
    """given indexs, it will output a sequence of substrs from left to right"""
    leftbound = 0
    rightbound = len(text)
    windows_indexs = [leftbound, *indexs, rightbound]

    for left_ptr, right_ptr in zip(windows_indexs[:-1], windows_indexs[1:]):
        yield text[left_ptr:right_ptr]


def args_parser():
    parser = argparse.ArgumentParser(description='Align Text')
    parser.add_argument('--hyp',  default="data/4-2-hypOut.txt", help='hypothesis file path')
    parser.add_argument('--ref',  default="data/4-2-refOut.txt", help='reference file path')
    parser.add_argument('--out',  default="data/4-2-output.txt", help='output file path')
    return parser

if __name__ == "__main__":
    args = args_parser().parse_args()

    hypo_text = ""
    ref_text = ""

    with open(args.hyp, "r") as hf:
        hypo_text = hf.read()

    with open(args.ref, "r") as rf:
        ref_text = rf.read()

    # trim duplicated spaces
    hypo_text = re.sub(" +", " ", hypo_text)
    ref_text = re.sub(" +", " ", ref_text)

    hypo_tokens = hypo_text.split(" ")
    label_tokens = ref_text.split(" ")

    uvmap = UnicodeVocabMapping(chain(hypo_tokens, label_tokens))

    # encode to unicode to avoid word level issues
    hypo = uvmap.to_unicode(hypo_tokens)
    label = uvmap.to_unicode(label_tokens)

    hypo_word_index_pairs, label_word_index_pairs = FilterBothRareWord(hypo, label)()

    h_indexs = [ i for _, i in hypo_word_index_pairs]
    l_indexs = [i for _, i in label_word_index_pairs]

    whole_aligns = []
    for h_substr, l_substr in zip( get_substr_by_indexs(h_indexs, hypo), get_substr_by_indexs(l_indexs, label) ):
        # print(h_substr, l_substr, sep=" @@@@ ")
        aligns = Diff(h_substr, l_substr).aligns
        whole_aligns.append(aligns)

    squzzed_aligns = chain(*whole_aligns)

    # postprocess from unicode to origin tokens
    squzzed_aligns = map( lambda x: (uvmap.from_unicode(x[0]), uvmap.from_unicode(x[1]) ), squzzed_aligns)

    print(Diff.make_aligns_json(squzzed_aligns), file=open(args.out, "w"))

#!/bin/bash

# name corpus
corp="full_corpus.txt"

# clean, compile corpora into one large corpus: creates full_corpus.txt
python conv.py $corp $1
echo 'finished processing'

# build 5-gram language model from corpus, "LM" FST
ngramsymbols < $corp > fst/lm.syms
echo 'finished extracting symbols'

farcompilestrings -symbols=fst/lm.syms -keep_symbols=1 $corp > fst/lm.far
ngramcount -order=5 fst/lm.far > fst/lm.cnts
echo 'finished counting ngrams'

ngrammake fst/lm.cnts > fst/lm.mod
echo 'finished model'
# ngramprint lm.mod > lm.txt

# compile "V" FST
python make_vocab.py $corp
fstcompile --isymbols=fst/v.isyms --osymbols=fst/lm.syms --keep_isymbols --keep_osymbols fst/v.fst > fst/v_out.fst
echo 'compiled VFST'

#!/bin/bash
n=$(cat short_inputs.txt | wc -l)
k=100

## for each input
for i in `seq 1 $n`;
do
    # create corpus and lm.* files (i passed because input must be rm'ed from corpus)
    bash make_lm.sh $i

    # create mn.fst from this input
    python make_input.py $i

    # compile mn.fst
    fstcompile --isymbols=fst/v.isyms --osymbols=fst/v.isyms --keep_isymbols --keep_osymbols --acceptor fst/mn.fst > fst/mn_out.fst
    echo 'mn.fst done'

    # MN o V = MNV
    fstcompose fst/mn_out.fst fst/v_out.fst > fst/mnv.fst

    # make MN an FSA
    fstproject --project_output fst/mnv.fst fst/mnv.fsa

    # MNV o LM = CONSTR
    fstcompose fst/mnv.fsa fst/lm.mod > fst/constr.mod
    echo 'constr.mod done'

    # rmepsilon and determinize
    fstdeterminize fst/constr.mod | fstrmepsilon > fst/constr_rd.mod
    echo 'constr_rd.mod rmepsilon/determinize done'

    # find and write shortestpaths to file
    a="mn/i"
    b="k"
    c=".tfst"
    d=".sp"

    fstshortestpath --nshortest=$k --unique=true fst/constr_rd.mod $a$i$b$k$d
    fstrmepsilon $a$i$b$k$d | fstdeterminize | fstprint - $a$i$b$k$c
    echo 'shortest path done'

    python sp_to_string.py $i $k
    echo 'shortest path written to string'
    
    echo $i
done

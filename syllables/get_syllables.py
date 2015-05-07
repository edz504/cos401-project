from syllabify import syllabify
import count_syl as cs
from textstat.textstat import textstat

a = syllabify('hello')
# this doesn't really work, it's for ARPANET, not English words

b = cs.count_syllables('accident')
# this script seems to work pretty well, but gives lower and upper bound

c = textstat.syllable_count('fragmentation')
# ^ works well

def get_mnemonic_syllables(mn):
    return sum([textstat.syllable_count(a) for a in mn.split()])
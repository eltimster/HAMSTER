# HAMSTER
HArmonised Multiword and Syntactic TreE Resource

As referenced in the paper:

Chan, King, Julian Brooke and Timothy Baldwin (to appear) Semi-Automated Resolution of Inconsistency for a Harmonized Multiword Expression and Dependency Parse Annotation, In Proceedings of the 13th Workshop on Multiword Expressions (MWE 2017), Valencia, Spain.

This code produces a HAMSTERized version of the Reviews subset of the English Web Treebank corpus, including MWE annotations from the [STREUSLE corpus](http://www.cs.cmu.edu/~ark/LexSem/). This process produces a single CoNLL-formated output file with numerous fixes for both the MWE and dependency parse annotations, see the paper for a detailed discussion. The tool requires STREUSLE. There is only one major option (other than input and output paths), namely the choice of how to deal with cases which have been marked as "Hard": They can be left as hard), converted to nonMWEs, converted to weak MWEs, or left how they were originally annotated. We used ^ to indicate the hard annotation, which is intended primarily as a way to avoid evaluating based on cases which humans cannot agree on. For other aspects of the annotation, please see the respective documentation for STREUSLE and the EWT. The tool should be executed as follows:

python hamster.py --hard_as_hard|hard_as_nonMWE|hard_as_weak|hard_as_original *location-of-streusle.tags* *output-file.tags*  

# HAMSTER
HArmonised Multiword and Syntactic TreE Resource

As referenced in the paper:

Chan, King, Julian Brooke and Timothy Baldwin (to appear) Semi-Automated Resolution of Inconsistency for a Harmonized Multiword Expression and Dependency Parse Annotation, In Proceedings of the 13th Workshop on Multiword Expressions (MWE 2017), Valencia, Spain.

This code produces a HAMSTERized version of the Reviews subset of the English Web Treebank (EWT) corpus, including MWE annotations from the [STREUSLE corpus](http://www.cs.cmu.edu/~ark/LexSem/) as well as the Stanford typed dependency annotations converted from the original constituency parse of the EWT. The output of the tool is a single CoNLL-formated output file with numerous fixes for both the MWE and dependency parse annotations, see the paper for a detailed discussion. The tool requires [STREUSLE 3.0](http://www.cs.cmu.edu/~ark/LexSem/streusle3.0.zip), which includes a CoNLL-formated version of the corpus, streusle.tags; if you don't have STREUSLE, please download it before applying this tool. The two arguments to the tool are the path to that streusle.tags file (e.g. "./streusle-3.0/streusle.tags") and a filename for the output file (e.g. "hamster-streusle.tags"). There is only one other option, namely the choice of how to deal with cases which have been marked as "Hard", indicating unresolvable disagreement among annotators: They can be left as hard (the default), converted to nonMWEs, converted to weak MWEs, or left as they were originally annotated in STREUSLE. We have used "^" to indicate the hard annotation. For other aspects of the annotation, please see the respective documentation for STREUSLE and the EWT. The tool should be executed as follows:

python hamster.py --hard_as_hard|hard_as_nonMWE|hard_as_weak|hard_as_original *STREUSLE-input-path* *output-path*  

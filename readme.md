Overview

In this assignment you will implement a program that calculates the BLEU evaluation metric, as defined in Papineni, Roukos, Ward and Zhu (2002): Bleu: a Method for Automatic Evaluation of Machine Translation, ACL 2002. You will run the program on sets of candidate and reference translations, and calculate the BLEU score for each candidate. The assignment will be graded on how closely your calculated BLEU score matches the true BLEU score.

Program

You will write a Python program which will take a two paths as parameters: the first parameter will be the path to the candidate translation (a single file), and the second parameter will be a path to the reference translations (either a single file, or a directory if there are multiple reference translations). The program will write an output file called bleu_out.txt which contains a single floating point number, representing the BLEU score of the candidate translation relative to the set of reference translations. If you use Python 2.7, name your program calculatebleu.py; if you use Python 3.4, name your program calculatebleu3.py. For example, your program will be expected to handle:

> python calculatebleu.py /path/to/candidate /path/to/reference

You can test your program by running it on the following candidate and translation files, and comparing the result to the true BLEU score.

Language	Candidate	Reference	BLEU score
German	candidate-1.txt	reference-1.txt	0.151184476557
Greek	candidate-2.txt	reference-2.txt	0.0976570839819
Portuguese	candidate-3.txt	reference-3.txt	0.227803041867
English	candidate-4.txt	
reference-4a.txt
reference-4b.txt
0.227894952018
The German, Greek and Portuguese reference translations above are excerpted from the common test set of the EUROPARL corpus; the candidate translations were obtained by taking the corresponding English sentences and running them through Google Translate. The English reference translations are from two alternative translations of the Passover Hagaddah; the candidate translation was obtained by running the original Hebrew text through Google translate. The actual test will be done with similar files.

Grading

There will be 10 test cases, so each test case is worth 10% of the grade for the assignment.
For each test case, the grade will be the (lower) ratio between the BLEU score you compute and the true BLEU score:
min (your-bleu, true-bleu)
max (your-bleu, true-bleu)
Notes

The candidate and reference files will be in UTF-8 encoding.
You may assume a line-by-line correspondence of sentences between the candidate and reference translations.
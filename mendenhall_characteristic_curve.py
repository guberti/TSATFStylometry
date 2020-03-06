import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import path
import re
import operator
import math
import nltk

SECTION_DIVIDERS = ["April 7, 1928", "June 2, 1910", "April 6, 1928", "April 8, 1928", "APPENDIX", "They endured"]
SECTION_VOICES = ["Benjy", "Quentin", "Jason", "Dilsey", "Hemmingway"]
TSATF_PATH = "TheSoundAndTheFury.txt"
TSAR_PATH = "TheSunAlsoRises.txt"
OUTDIR = "res"
SCALE = 10000

SECTIONS = []
with open(TSATF_PATH, 'r') as file:
    TSATF = file.read()
    for i, narrator in enumerate(SECTION_VOICES[:4]):
        i = SECTION_VOICES.index(narrator)
        start = TSATF.find(SECTION_DIVIDERS[i]) + len(SECTION_DIVIDERS[i])
        end = TSATF.find(SECTION_DIVIDERS[i], start)
        SECTIONS.append(TSATF[start:end])

with open(TSAR_PATH, 'r') as file:
    TSAR = file.read()
    SECTIONS.append(TSAR)

# Transform the authors' corpora into lists of word tokens
by_author_tokens = {}
by_author_length_distributions = {}
for i, section in enumerate(SECTIONS):
    tokens = nltk.word_tokenize(section)
    author = SECTION_VOICES[i]

    # Filter out punctuation
    by_author_tokens[author] = ([token for token in tokens
                                            if any(c.isalpha() for c in token)])

    # Get a distribution of token lengths
    token_lengths = [len(token) for token in by_author_tokens[author]]
    by_author_length_distributions[author] = nltk.FreqDist(token_lengths)
    print(by_author_length_distributions[author])

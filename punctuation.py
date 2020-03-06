import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from os import path
import re
import operator
import math

SECTION_DIVIDERS = ["April 7, 1928", "June 2, 1910", "April 6, 1928", "April 8, 1928", "APPENDIX", "They endured"]
SECTION_VOICES = ["Benjy", "Quentin", "Jason", "Dilsey", "Hemmingway"]
#PUNCTUATION = ["-", "!", ";", ":", "("]
#PUNCTUATION_MARKS = ["Hyphen", "Exclamation", "Semicolon", "Colon", "Parenthesis"]
#PUNCTUATION = ["\"", ".", ",", "?", "!"]
#PUNCTUATION_MARKS = ["Quote", "Period", "Comma", "Question", "Exclamation"]
PUNCTUATION = ["the", "be", "to", "of", "and"]
PUNCTUATION_MARKS = ["The", "Be", "To", "Of", "And"]
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


# Per 1,000 characters
def punctuation_density(section, char):
    return section.count(char) * SCALE / len(section)

#def pun_std_dev(section, char):


fig, ax = plt.subplots()
axes = []

ind = np.arange(len(SECTION_VOICES))    # the x locations for the groups
width = 0.15

for k, section in enumerate(SECTIONS):
    yerrs = []
    for m in PUNCTUATION:
        p = punctuation_density(section, m) / SCALE
        print(p)
        print(p)
        yerrs.append(math.sqrt(p * (1-p) / len(section)) * SCALE)
    axis = ax.bar(ind + width * k,
            [punctuation_density(section, m) for m in PUNCTUATION],
            width, bottom=0, yerr=yerrs)
    axes.append(axis)

for i, mark in enumerate(PUNCTUATION):
    for j, section1 in enumerate(SECTIONS):
        for k, section2 in enumerate(SECTIONS):
            combined = section1 + section2
            p = combined.count(mark) / len(combined)
            std_err = math.sqrt(p * (1-p) * ((1/len(section1)) + (1/len(section2))))
            mean = (section1.count(mark)/len(section1) - section2.count(mark)/len(section2))
            sigmas = mean / std_err
            print("For \"{}\", {} and {} differ by {} ({} sigmas)".format(
                mark,
                SECTION_VOICES[j], SECTION_VOICES[k],
                mean, sigmas
                ))
#ax.set_title('Common Punctuation Across TSATF Sections')
ax.set_xticks(ind + width * 2)
ax.set_xticklabels(tuple(PUNCTUATION_MARKS))
ax.set_ylabel("Occurrences per 10,000 characters")
print(axes)
ax.legend((p[0] for p in axes), tuple(SECTION_VOICES))

filename = "_".join(PUNCTUATION_MARKS).lower() + "_{}.png".format(SCALE)
fig.savefig(path.join(OUTDIR, filename))
plt.show()

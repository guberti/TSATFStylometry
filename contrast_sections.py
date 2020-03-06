import argparse
import matplotlib.pyplot as plt
from os import path
import re
import operator
import math

SECTION_DIVIDERS = ["April 7, 1928", "June 2, 1910", "April 6, 1928", "April 8, 1928", "APPENDIX", "They endured"]
SECTION_VOICES = ["Benjy", "Quentin", "Jason", "Dilsey", "Appendix"]
FILE = "TheSoundAndTheFury.txt"

WORDS = ['smell', 'fire', 'hush', 'tp', 'stop', 'dead', 'coming', 'cold', 'shadow', 'time']
VOICE1 = "Dilsey"
VOICE2 = "Benjy"
VOICE3 = "Quentin"

with open(FILE, 'r') as file:
    BOOK = file.read()


def get_character_subsection(character):
    i = SECTION_VOICES.index(character)
    start = BOOK.find(SECTION_DIVIDERS[i]) + len(SECTION_DIVIDERS[i])
    end = BOOK.find(SECTION_DIVIDERS[i], start)
    return BOOK[start:end]

section1 = get_character_subsection(VOICE1)
section2 = get_character_subsection(VOICE2)
section3 = get_character_subsection(VOICE3)

def gen_word_histogram(text):
    words = re.sub(r'[^A-Za-z0-9 ]+', '', text).lower().split(" ")
    hist = {}
    for word in words:
        if word not in hist:
            hist[word] = 0
        hist[word] += 1

    # Now find the most common word, and plot all other words as fractions of that
    frequent_word = max(hist.items(), key=operator.itemgetter(1))[0]
    occurrences = hist[frequent_word]

    return {key:val/occurrences for key, val in hist.items()}

base = gen_word_histogram(section1)
xaxis = gen_word_histogram(section2)
yaxis = gen_word_histogram(section3)

xdata = []
ydata = []
for word in WORDS:
    xdata.append(math.log10(xaxis[word]/base[word]))
    ydata.append(math.log10(yaxis[word]/base[word]))

fig, ax = plt.subplots()
ax.scatter(xdata, ydata)

for i, word in enumerate(WORDS):
    ax.annotate(word, (xdata[i], ydata[i]))

ax.grid()
ax.set(xlabel=VOICE2 + "'s Section (log10)", ylabel=VOICE3 + "'s Section (log10)")
fig.savefig(path.join("res", "{}_{}_{}_contrast.png".format(VOICE1, VOICE2, VOICE3)))
plt.show()

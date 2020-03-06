import argparse
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
from os import path

SECTION_DIVIDERS = ["June 2, 1910", "April 6, 1928", "April 8, 1928", "APPENDIX"]
TOP_10000_PATH = "google-10000-english-usa.txt"

with open(TOP_10000_PATH) as f:
    l = f.read().split("\n")
    TOP_100 = set(l[:100])
    TOP_1000 = set(l[:1000])

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('filepath', type=str, help='location of the ebook pdf')
    parser.add_argument('subdivisions', type=int, help='number of subdivisions to divide the book', default=50)
    parser.add_argument('--outdir', type=str, help='output dir for graphs', default='res')

    args = parser.parse_args()

    with open(args.filepath, 'r') as file:
        text = file.read()

    # Mark section divider locations
    dividers = []
    for d in SECTION_DIVIDERS:
        dividers.append(args.subdivisions * text.find(d) / len(text))

    sentence_length = []
    word_frequency_100 = []
    word_frequency_1000 = []

    section_length = len(text) // args.subdivisions
    for i in range(args.subdivisions):
        section = text[section_length * i : section_length * (i+1)]

        words = section.split(" ")
        word_frequency_100.append(100 * len([s for s in words if s.lower() in TOP_100]) / len(words))
        word_frequency_1000.append(100 * len([s for s in words if s.lower() in TOP_1000]) / len(words))

        section = section.replace('!', '.').replace('?', '.')
        sentences = section.split(". ")

        sentence_length.append(sum([len(s) for s in sentences]))
        print("Crunched section " + str(i))


    fig, ax1 = plt.subplots()
    color1 = 'tab:red'
    ax1.set_xlabel('Subsection')
    ax1.set_ylabel('Top 100 Words (%)', color=color1)
    ax1.plot(range(args.subdivisions), word_frequency_100, color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = 'tab:blue'
    ax2.set_ylabel('Top 1,000 Words (%)', color=color2)  # we already handled the x-label with ax1
    ax2.plot(range(args.subdivisions), word_frequency_1000, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    for xc in dividers:
        plt.axvline(x=xc, color='k', linestyle='--')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    filename = "sentences_{}.png".format(args.subdivisions)

    fig.savefig(path.join(args.outdir, filename))
    plt.show()

if __name__ == '__main__':
    main()

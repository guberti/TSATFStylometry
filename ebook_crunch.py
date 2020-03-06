import argparse
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
from os import path

SECTION_DIVIDERS = ["June 2, 1910", "April 6, 1928", "April 8, 1928", "APPENDIX"]
TOP_10000_PATH = "google-10000-english-usa.txt"

with open(TOP_10000_PATH) as f:
    TOP_10000 = f.read().split("\n")


def count_word(section, word):
    return section.lower().count(word.lower())

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('filepath', type=str, help='location of the ebook pdf')
    parser.add_argument('subdivisions', type=int, help='number of subdivisions to divide the book', default=50)
    parser.add_argument('action', type=str, help='analysis engine to use', choices=['word'])
    parser.add_argument('--outdir', type=str, help='output dir for graphs', default='res')
    parser.add_argument('--words', type=str, help='word to use for frequency analysis', nargs='+')
    parser.add_argument('--seperate', action='store_true')
    parser.add_argument('--smooth', action='store_true')

    args = parser.parse_args()

    with open(args.filepath, 'r') as file:
        text = file.read()

    # Mark section divider locations
    dividers = []
    for d in SECTION_DIVIDERS:
        dividers.append(args.subdivisions * text.find(d) / len(text))

    values = []
    if args.seperate:
        for i in range(len(args.words)):
            values.append([])

    section_length = len(text) // args.subdivisions
    for i in range(args.subdivisions):
        section = text[section_length * i : section_length * (i+1)]
        if args.action == 'word':
            if (args.seperate):
                for i, word in enumerate(args.words):
                    values[i].append(count_word(section, word))
            else:
                s = 0
                for word in args.words:
                    s += count_word(section, word)
                values.append(s)

    print(values)

    fig, ax = plt.subplots()

    if args.seperate:
        for i, data in enumerate(values):
            xnew = np.linspace(0, args.subdivisions - 1, 100)
            spl = make_interp_spline(range(args.subdivisions), data, k=5)  # type: BSpline
            power_smooth = [max(y, 0) for y in spl(xnew)]

            ax.plot(xnew, power_smooth, label=args.words[i])
            #ax.plot(range(args.subdivisions), data)
    else:
        #xnew = np.linspace(0, args.subdivisions - 1, 100)
        #spl = make_interp_spline(range(args.subdivisions), values, k=3)  # type: BSpline
        #power_smooth = spl(xnew)

        #ax.plot(xnew, power_smooth)
        ax.plot(range(args.subdivisions), values)

    # Divide up each character's section
    for xc in dividers:
        plt.axvline(x=xc, color='k', linestyle='--')

    if args.action == 'word':
        ax.set(xlabel='Subsection', ylabel='Occurrences')
        if args.seperate:
            ax.legend(loc='upper right')
        filename = "{}_{}_{}_seperate.png".format(args.action, args.subdivisions, args.words[0])
    fig.savefig(path.join(args.outdir, filename))
    plt.show()

if __name__ == '__main__':
    main()

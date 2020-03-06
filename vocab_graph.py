import argparse
import matplotlib.pyplot as plt
import numpy as np
from os import path
from functools import lru_cache
import re
import copy
import statistics

SECTION_DIVIDERS = ["June 2, 1910", "April 6, 1928", "April 8, 1928", "APPENDIX"]
TOP_100000_PATH = "wiki-100000-english.txt"
BUCKETS_THRESHOLDS = [10, 100, 1000, 10000, 100000]
BUCKETS_THRESHOLDS_S = ["10", "100", "1,000", "10,000", "100,000"]
BUCKETS = []

with open(TOP_100000_PATH, encoding="utf8") as f:
    l = f.read().split("\n")
    no_comments = [x for x in l if x[0] != "#"]
    BUCKETS = [set(no_comments[:x]) for x in BUCKETS_THRESHOLDS]
print("Loaded words into buckets")

@lru_cache(maxsize=100000)
def bucket(word):
    bucket_num = 0
    for bucket in BUCKETS:
        if word in bucket:
            break
        else:
            bucket_num += 1
    return bucket_num

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('filepath', type=str, help='location of the ebook pdf')
    parser.add_argument('subdivisions', type=int, help='number of subdivisions to divide the book', default=50)
    parser.add_argument('--outdir', type=str, help='output dir for graphs', default='res')

    args = parser.parse_args()

    with open(args.filepath, encoding="utf8") as file:
        text = file.read()

    # Mark section divider locations
    dividers = []
    for d in SECTION_DIVIDERS:
        dividers.append(args.subdivisions * text.find(d) / len(text))

    bucket_usages = [[] for x in range(len(BUCKETS_THRESHOLDS) + 1)]
    section_length = len(text) // args.subdivisions
    for i in range(args.subdivisions):
        section = text[section_length * i : section_length * (i+1)]
        section = section.replace("\n", " ")
        section = re.sub(r'[^A-Za-z0-9 ]+', '', section).lower()

        bucket_usage = [0] * (len(BUCKETS_THRESHOLDS) + 1)
        words = section.split(" ")

        for word in words:
            b = bucket(word)
            bucket_usage[b] += 1

        for i in range(len(bucket_usage)):
            bucket_usages[i].append(bucket_usage[i] / len(words))

    bucket_sums = copy.deepcopy(bucket_usages)
    for i in range(1, len(bucket_sums)):
        for k in range(0, len(bucket_sums[i])):
            bucket_sums[i][k] = bucket_sums[i-1][k] + bucket_sums[i][k]

    for i in range(0, len(bucket_sums)):
        print("{} : {}".format(
            statistics.mean(bucket_sums[i]),
            statistics.stdev(bucket_sums[i]))
        )

    plt.stackplot(range(args.subdivisions), *tuple(bucket_usages),
        labels=["Top {}".format(i) for i in BUCKETS_THRESHOLDS_S] + ["Other"])

    for xc in dividers:
        plt.axvline(x=xc, color='k', linestyle='--')

    plt.legend(loc='upper left')
    plt.xlabel('Subsection')
    plt.ylabel('Fraction of words')
    filename = "{}_{}_vocab_graph.png".format(args.filepath[:-4], args.subdivisions)
    plt.savefig(path.join(args.outdir, filename))
    plt.show()


if __name__ == '__main__':
    main()

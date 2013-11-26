#!/usr/bin/env python

import nltk
from nltk import LidstoneProbDist, NgramModel
import re
import random
import os

TOPDIR = os.path.dirname(os.path.realpath(__file__))

class Generator:
    def __init__(self):
        dataset = open(os.path.join(TOPDIR, 'dataset.txt')).read()
        words = [word for word in dataset.split() if re.match(r'[a-zA-Z0-9 \.,?:\'"!_\(\)]+', word)]
        self.words = words
        self.model = nltk.Text(words)

    def raw_words(self, length=100):
        """Generates a list of words using an NLTK NgramModel."""
        if not hasattr(self, '_ngram_model'):
            estimator = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
            self._ngram_model = NgramModel(2, self.model, estimator)
        return self._ngram_model.generate(length, [random.choice(self.words)])[1:]

    def smart_trim(self, genwords):
        """Trims to tweet-size while attempting to respect sentence boundaries."""
        new_words = genwords[:]

        # Cleverly trim to tweet size
        stoppers = r'[.?!]'
        while True:
            short_enough = (sum([len(word)+1 for word in new_words]) < 140)
            if short_enough and re.search(stoppers, new_words[-1]):
                break
            if len(new_words) <= 1:
                new_words = genwords[:]
                break
            new_words.pop()

        # Proper sentence markings
        for i, word in enumerate(new_words):
            if i == 0  or re.search(stoppers, new_words[i-1][-1]):
                new_words[i] = word.capitalize()

        return new_words

    def tweetworthy(self):
        """Generate some tweetable text."""
        genwords = self.raw_words()

        genwords = self.smart_trim(genwords)

        while len(genwords) > 1 and sum([len(word)+1 for word in genwords]) > 140:
            genwords.pop()

        # genwords[-1] += random.choice(['.', '!', '?'])

        product = " ".join(genwords)
        if len(product) > 140: product = product[0:140]

        # Remove mismatched enclosures
        for pair in [['(', ')'], ['{', '}'], ['[', ']']]:
            if product.count(pair[0]) != product.count(pair[1]):
                product = product.replace(pair[0], '').replace(pair[1], '')

        for enc in ['"', '*']:
            if product.count(enc) % 2 != 0:
                product = product.replace(enc, '')

        return product


if __name__ == '__main__':
    gen = Generator()
    tweet = gen.tweetworthy()
    print tweet

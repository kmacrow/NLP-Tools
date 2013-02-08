#!/usr/bin/env python

'''
  Copyright (C) 2013 Kalan MacRow <kalanwm@cs.ubc.ca>

  Part-of-Speech bi-gram model comparison engine.
  CPSC 503, Winter 2012.
  Department of Computer Science
  The University of British Columbia, Vancouver 
'''

import sys
import re

# print the usage instructions
def usage():
  print "Usage: ./cep.py BIGRAM-MODEL TAG-SENTENCES"

# return all of the bigrams in a sentence
def get_bigrams(sentence):
  bigrams = []
  words = sentence.split()
  for i in range(len(words) - 1):
      bigrams.append(words[i] + ' ' + words[i + 1])
  return bigrams

# main entry point for the script
def main():
  fp = None # file pointer
  N = 0.0   # total number of bigrams
  P = {}    # model probabilities
  Q = {}    # empirical probabilities
  H = 0.0   # perplexity


  if len(sys.argv) != 3:
    usage()
    sys.exit(1)

  try:
    # open model in line-buffered mode
    fp = open(sys.argv[1], 'r', 1)
  except:
    print "Invalid model definition file."
    sys.exit(1)

  # compile regex = faster
  prog = re.compile(r"(\-?\d*\.?\d+) \-?\d*\.?\d+ __EOC__ (.*)")

  # load model into memory
  for line in fp:
    result = prog.match(line)
    # store log2P(ti|ti-1) for bigram on this line
    P[result.group(2).strip()] = float(result.group(1))

  # finished with model
  fp.close()

  try:
    # open sentences in line-buffered mode 
    fp = open(sys.argv[2], 'r', 1)
  except:
    print "Invalid tag sentences file."
    sys.exit(1)

  # load empirical probabilities
  for line in fp:
    bigrams = get_bigrams(line)
    for bigram in bigrams:
      if bigram in Q:
        Q[bigram] += 1
      else:
        Q[bigram] = 1.0
    N += len(bigrams)

  fp.close()

  # calculate the cross entropy
  for bigram in Q:
    # counts --> probabilities
    Q[bigram] /= N
    # model doesn't know about this bigram?
    if not bigram in P:
      P[bigram] = -99999.0

    H += Q[bigram] * P[bigram]

  # output some useful numbers
  print 'B (unique bigrams)     = ' + str(len(Q.keys()))
  print 'N (total bigrams)      = ' + str(N)
  print 'H (cross-entropy)      = ' + str(H)
  print '2^H (cross-perplexity) = ' + str(pow(2, H))


if __name__ == '__main__':
  main()


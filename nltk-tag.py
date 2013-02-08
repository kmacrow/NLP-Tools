#!/usr/bin/env python

'''
  Copyright (C) 2013 Kalan MacRow <kalanwm@cs.ubc.ca>

  Quick + Dirty confusion matrix generator with NLTK
  CPSC 503, Winter 2012.
  Department of Computer Science
  The University of British Columbia, Vancouver 
'''
import sys
import re
import nltk


def main():
  fp = None
  A = []         # existing, tagged sentences
  B = []         # NLTK tagged sentences
  tags = {}      # known tags
  tag_index = {} # quick lookup for tag --> index into list of tags
  sentences = [] # raw, untagged sentences to feed NLTK
  matrix = None  # out confusion matrix
  errors = 0     # total errors
  correct = 0    # total correct

  if len(sys.argv) != 3:
    print "Usage: ./nltk-tag.py TAGGED-SENTENCES UNTAGGED-SENTENCES"
    sys.exit(1)

  # need to get the two "taggings" into equivalent data structures
  try:
    fp = open(sys.argv[1], 'r', 1)
  except:
    print "Could not read tagged-sentences file."
    sys.exit(1)

  # load up existing tagged sentences
  prog = re.compile(r"([\-\`\,\$\.\'\"\w]+)_([^\s]+)")
  for line in fp:
    sentence = []
    results = prog.findall(line)
    for result in results:
      # append (word, POS) to list
      sentence.append((result[0], result[1]))
      # keep track of the tags we see
      if not result[1] in tags:
        tags[result[1]] = True
    # append the tagged, parsed sentence to A
    A.append(sentence)

  # convert tag hash into an array
  tags = tags.keys()
  # create a reverse-index on tag name
  for i in range(len(tags)):
    tag_index[tags[i]] = i

  fp.close()

  try:
    fp = open(sys.argv[2], 'r', 1)
  except:
    print "Count not read untagged-sentences file."
    sys.exit(1)

  # use NLTK to tag the clean file
  for line in fp:
    B.append(nltk.pos_tag(nltk.word_tokenize(line)))

  fp.close()

  # initialize the confusion matrix
  dim = len(tags) + 1
  matrix = [[0]*dim for i in range(dim)]

  # populate the matrix
  # in theory, A and B are exactly the same size.
  if len(A) != len(B):
    print "A/B mismatch: %s to %s" % (len(A), len(B))
    sys.exit(1)


  for i in range(len(A)):
    sentence_a = A[i]
    sentence_b = B[i]

    if len(sentence_a) != len(sentence_b):
      continue

    for j in range(len(sentence_a)):
      word_a = sentence_a[j]
      word_b = sentence_b[j]

      x = tag_index[ word_a[1] ]

      if word_b[1] in tag_index:
        y = tag_index[ word_b[1] ]
      else:
        y = len(tags)

      if x != y:
        errors += 1
      else:
        correct += 1

      try: 
        matrix[x][y] += 1
      except:
        continue

  # pretty-print the matrix
  print "    "
  for tag in tags:
    print tag.center(4),
  print

  for i in range(len(tags)):
    print tags[i].center(4),
    for j in range(len(tags) + 1):
      print repr(matrix[i][j]).rjust(4),
    print 

  # some useful figures
  print
  print
  print "errors  = " + str(errors)
  print "correct = " + str(correct)

if __name__ == '__main__':
  main()
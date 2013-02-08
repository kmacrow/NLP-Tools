#!/usr/bin/env python

'''
  Copyright (C) 2013 Kalan MacRow <kalanwm@cs.ubc.ca>

  Calculate part-of-speech counts for plant* words 
  CPSC 503, Winter 2012.
  Department of Computer Science
  The University of British Columbia, Vancouver 
'''

import sys
import re

# print the usage instructions
def usage():
  print "Usage: ./plants.py TAGGED-SENTENCES"

def main():
  # file pointer
  fp = None
  # counts of plant* words by tag type
  plants = {} 

  if len(sys.argv) != 2:
    usage()
    sys.exit(1)  

  try:
    # open tagged speech in line-buffered mode
    fp = open(sys.argv[1], 'r', 1)
  except:
    print "Invalid tagged-sentences file."
    sys.exit(1)

  # compile out RE for speed
  prog = re.compile(r"(plant\w*)_([^\s]+)")
  
  # count instances of plant* by POS
  for line in fp:
    results = prog.findall(line)
    for result in results:
      if result[1] in plants:
        plants[result[1]] += 1
      else:
        plants[result[1]] = 1

  fp.close()

  # print some useful output
  for pos in plants:
    print pos + ' = ' + str(plants[pos])


if __name__ == '__main__':
  main()

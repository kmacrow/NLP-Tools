#!/usr/bin/env python

'''
  Copyright (C) 2013 Kalan MacRow <kalanwm@cs.ubc.ca>

  Quick + Dirty part-of-speech tag stripper
  CPSC 503, Winter 2012.
  Department of Computer Science
  The University of British Columbia, Vancouver 
'''

import sys
import re

def main():

  if len(sys.argv) != 2:
    print "Usage: ./clean-tags.py TAGGED-SENTENCES"
    sys.exit(1)

  fp = open(sys.argv[1])

  prog = re.compile(r"([\-\`\,\$\.\'\"\w]+)_[^\s]+")
  for line in fp:
    results = prog.findall(line)
    output = ''
    #print results
    for result in results:
      output += ' ' + result
    print output
    
  fp.close()

if __name__ == '__main__':
  main()
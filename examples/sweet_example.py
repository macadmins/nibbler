#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from nibbler import *

try:
    script_path = os.path.dirname(os.path.realpath(__file__))
    n = Nibbler(os.path.join(script_path, 'sweet.nib'))
except IOError, ImportError:
    print "Unable to load nib!"
    exit(20)

def test():
    print "hi (no quit)"

def test2():
    print "hi (politely quit)"
    n.quit()

n.attach(test, 'pushy')
n.attach(test2, 'less_pushy')

n.hidden = True
n.run()

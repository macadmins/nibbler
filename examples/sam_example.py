#!/usr/bin/python
# -*- coding: utf-8 -*-

from nibbler import *

# --- necessary for evil hacks ---
import objc
MapKit = objc.loadBundle('MapKit', globals(), bundle_path='/System/Library/Frameworks/MapKit.framework')
# ---

try:
    script_path = os.path.dirname(os.path.realpath(__file__))
    n = Nibbler(os.path.join(script_path, 'sam.nib'))
except IOError, ImportError:
    print "Unable to load nib!"
    exit(20)

def test():
    print "hi - let's print some handles"
    print n.nib_contents
    print n.views['the_text'].stringValue()

def test2():
    print "hi (politely quit)"
    n.quit()

n.attach(test, 'pushy')
n.attach(test2, u'😘')

n.hidden = True
n.run()

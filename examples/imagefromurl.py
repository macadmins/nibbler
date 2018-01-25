#!/usr/bin/python
'''
Runs a gui for enrolling a Mac into Munki based on serial manifests
'''
#https://km.support.apple.com/kb/securedImage.jsp?&size=240x240&configcode=
# -*- coding: utf-8 -*-
# pylint: disable=W0614
import sys
import AppKit
import Foundation
from nibbler import *

try:
    script_path = os.path.dirname(os.path.realpath(__file__))
    n = Nibbler(os.path.join(script_path, 'imagefromurl.nib'))
except IOError, ImportError:
    print "Unable to load nib!"
    sys.exit(20)
Quiting = False

IOKit_bundle = NSBundle.bundleWithIdentifier_('com.apple.framework.IOKit')

functions = [
    ("IOServiceGetMatchingService", b"II@"),
    ("IOServiceMatching", b"@*"),
    ("IORegistryEntryCreateCFProperty", b"@I@@I"),
]

objc.loadBundleFunctions(IOKit_bundle, globals(), functions)

# pylint: disable=E0602
def io_key(keyname):
    '''
    frogor/pudquick magic
    '''
    return IORegistryEntryCreateCFProperty(IOServiceGetMatchingService(0,\
     IOServiceMatching("IOPlatformExpertDevice")), keyname, None, 0)


# pylint: enable=E0602


def get_hardware_serial():
    '''
    Get's serial directly from the Board via frogor magic
    '''
    return io_key("IOPlatformSerialNumber")


def quitgui():
    '''
    Quit GUI and Script
    '''
    n.quit()
    sys.exit()


def progress(message):
    '''
    Output value to the "progress" box
    '''
    feedback = n.views['output']
    feedback.setStringValue_(" ")
    feedback.setStringValue_(message)

def get_config_code(serial):
    if len(serial) > 11:
        configcode = serial[-4:]
    else:
        configcode = serial[-3:]
    return configcode

def get_image_url():
    code = get_config_code(get_hardware_serial())
    urlbase = 'https://km.support.apple.com/kb/securedImage.jsp?&size=240x240&configcode='
    finalurl = urlbase+code
    return finalurl

def main():
    '''
    Run this thing!
    '''
    url =  Foundation.NSURL.URLWithString_(get_image_url())

    imagedata = Foundation.NSData.dataWithContentsOfURL_(url)
    image = AppKit.NSImage.alloc().initWithData_(imagedata)
    n.views['machine_deviceimage'].setImage_(image)
    n.attach(n.views['serialfield'].setStringValue_(get_hardware_serial()),
             'serialfield')
    n.attach(quitgui, 'quitbutton')
    n.run()


if __name__ == '__main__':
    main()

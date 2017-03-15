#!/usr/bin/python
"""Setup assistant showing how to automate tasks based on timing."""

from nibbler import *

import objc
from AppKit import NSTimer
from OpenDirectory import *

import argparse
import logging
import os

VALID_PASSWORD = False
PASSWORD = ''
global showed_up_once
showed_up_once = False
global IamQuitting
IamQuitting = False
global on_run_trigger
on_run_trigger = False

try:
  # Because of how this loads, this should be an absolute path if you don't
  # want to run this from the same directory as the script
  n = Nibbler('setup_assistant.nib')
except IOError:
  print "Unable to load nib!"
  exit(20)

logging.basicConfig(
  format='%(asctime)s your-tag-goes-here %(levelname)s: %(message)s',
  datefmt='%m/%d/%Y %I:%M:%S %p',
  filename=os.path.expanduser('~/Library/Logs/nibbler_tool.log'),
  level=logging.DEBUG
)


# System interaction functions
def get_console_user():
    """Use SystemConfiguration framework to get the current console user."""
    from SystemConfiguration import SCDynamicStoreCopyConsoleUser
    cfuser = SCDynamicStoreCopyConsoleUser(None, None, None)
    return cfuser[0]


def check_authentication(username, password):
  """Validate password.

  Utilizes OpenDirectory to validate the password of the user.
  Returns True if valid, otherwise False
  """
  # Credit to Greg Neagle for this
  class ODException(Exception):
    """Base exception for OpenDirectory."""

  class ODSessionException(Exception):
      """ODSessionException."""

  class ODNodeException(ODException):
      """ODNode exception."""

  class ODQueryException(ODException):
      """ODQueryException."""

  class ODRecordException(ODException):
      """ODRecordException."""

  class ODPasswordException(ODException):
      """ODPasswordException."""

  session = ODSession.defaultSession()
  if not session:
    raise ODSessionException('Could not get default Open Directory session')

  node, error = ODNode.nodeWithSession_name_error_(session, '/Search', None)
  if error:
    raise ODNodeException(error)

  query, error = ODQuery.queryWithNode_forRecordTypes_attribute_matchType_queryValues_returnAttributes_maximumResults_error_(
    node,
    kODRecordTypeUsers,
    kODAttributeTypeRecordName,
    kODMatchEqualTo,
    username,
    kODAttributeTypeStandardOnly,
    1,
    None
  )

  if error:
    raise ODQueryException(error)

  results, error = query.resultsAllowingPartial_error_(False, None)
  if error:
    raise ODQueryException(error)

  if results:
    record = results[0]
    passwordVerified, error = record.verifyPassword_error_(password, None)
    if error and error.code() != 5000:
      # 5000 means invalid user or password
      raise ODPasswordException(error)

    return passwordVerified
  else:
    # no matching username in DS, so return False
    return False


# Output functions
def output(message):
  """Output to both nibbler field and log."""
  logging.info(str(message))
  n.views['label.progress'].setStringValue_(str(message))


def die(message):
  """Log a message and exit the script."""
  logging.critical(str(message))
  exit(1)


# Nibbler loading functions
class genericWindowCloseController(NSObject):
  """This class represents the window controller."""

  def setClose_(self, f_obj):
    """Call the function passed in when the window closes."""
    self.f = f_obj

  def setMain_(self, f_obj):
    """Call the function passed in when the window gains focus."""
    self.e = f_obj

  def windowWillClose_(self, sender):
    """"Respond to the window closing event."""
    if hasattr(self, 'f'):
      self.f()

  def windowDidBecomeMain_(self, sender):
    """Respond to the window focus event."""
    if hasattr(self, 'e'):
      self.e()

  def automaticTimerResponder_(self, timer):
    """Respond to the automatic timer."""
    go_time()


def close_window():
  """Trigger when closing the window."""
  global IamQuitting
  if not IamQuitting:
    print "Window closed, quitting"
    IamQuitting = True
    n.quit()


def became_main():
  """Trigger when window becomes main."""
  # This will run every time the window becomes the 'main' focused window.
  # If you want things to run only once when the window loads, put your
  # function calls down below.
  global showed_up_once
  if not showed_up_once:
    showed_up_once = True
    print "Window loaded for the first time!"
    if on_run_trigger:
      # Set by the '--auto' argument down below.
      on_run()


# Button definitions
def button_outlook():
  """Configure Outlook."""
  output('Configuring Outlook')
  # Configure Outlook


def button_chef():
  """Run Chef."""
  output((
    'Running Chef...\n'
    'Watch the Chef outputs file for live results.')
  )
  # Run Chef


def button_filetask():
  """File a trouble ticket."""
  output('Filing a task...')
  # Insert your ticketing system API code here.
  output('Task filed.')


def button_msc():
  """Open Managed Software Center."""
  output('Running Managed Sofware Center...')
  # Run Managed Software Center
  output('MSC run completed.')


def button_mscbootstrap():
  """Open Managed Software Center."""
  output('Touching Munki bootstrap file...')
  # Touch the Munki bootstrap
  output((
    "Created Munki bootstrap file...\n"
    "Please log out to complete Munki bootstrap.")
  )


def button_password():
  """Validate password."""
  output('Validating password...')
  print 'Getting console user'
  username = get_console_user()
  print 'Console user: %s' % username
  password = n.views['field.password'].stringValue()
  print 'Validating password'
  result = check_authentication(username, password)
  global VALID_PASSWORD
  global PASSWORD
  if result:
    print 'Correct password.'
    n.views['label.progress'].setStringValue_('Password is correct!')
    n.views['label.password'].setStringValue_('Valid.')
    VALID_PASSWORD = True
    PASSWORD = password
    # Enable other buttons
    n.views['button.outlook'].setEnabled_(True)
    n.views['button.chef'].setEnabled_(True)
    n.views['button.msc'].setEnabled_(True)
    n.views['button.mscbootstrap'].setEnabled_(True)
    # Disable password button and field
    n.views['button.validate'].setEnabled_(False)
    n.views['field.password'].setEnabled_(False)
  else:
    print 'Incorrect password.'
    n.views['label.progress'].setStringValue_('Invalid password.')


def button_quit():
  """Quit."""
  output('Quitting.')
  global IamQuitting
  IamQuitting = True
  n.quit()


def on_run():
  """Run only once when the tool is launched."""
  # Put all of your "things that should happen immediately on launch" code here
  # This happens before the window finishes loading, so no changes to the
  # window state will happen "live" until this function completes.
  print 'On run operations'


def go_time():
  """Run the actual automatic actions."""
  # This function responds to an automatic timer, so it will be triggered
  # after the window has finished loading and on_run() completes.
  # If you want your tool to automatically execute code after the window is
  # ready, this is where you'd put it.
  print 'Go do magic on a timer!'


def main():
  """Main magic."""
  parser = argparse.ArgumentParser(
    description='Setup and configuration tool.')
  parser.add_argument(
    '-a', '--auto', help='Automatically run all configuration.',
    action='store_true')
  args = parser.parse_args()

  if args.auto:
    # We want to do stuff automatically
    global on_run_trigger
    on_run_trigger = True
    # If `on_run_trigger` is true, then the on_run() function will be called
    # when the window loads for the first time.

  # Attach all the buttons to functions
  n.attach(button_outlook, 'button.outlook')
  n.attach(button_chef, 'button.chef')
  n.attach(button_msc, 'button.msc')
  n.attach(button_mscbootstrap, 'button.mscbootstrap')
  n.attach(button_filetask, 'button.filetask')
  n.attach(button_password, 'button.validate')
  n.attach(button_quit, 'button.quit')
  # Set up our window controller and delegate
  n.hidden = True
  closer = genericWindowCloseController.alloc().init()
  closer.setClose_(close_window)
  closer.setMain_(became_main)
  n.win.setDelegate_(closer)
  # Trigger an automatic timer that will kick off code
  # that we want to run automatically on launch
  NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
    5,  # seconds before timer fires
    closer,  # controller to be used
    'automaticTimerResponder:',  # function to be called on controller
    None,  # always None
    False  # repeat the timer
  )
  # Launch the window
  n.run()


if __name__ == '__main__':
  main()

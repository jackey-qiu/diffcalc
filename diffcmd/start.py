"""
start the diffcmd environemt using a script from startup.
This should normally be run by the main diffcalc.py program.

with diffcalc on PYTHONPATH
$ ipython -i -m diffcm.diffcmd module_name_string debug_bool
"""
from __future__ import absolute_import

import diffcalc
import diffcalc.settings
import os
import sys
from diffcalc.ub.persistence import UBCalculationJSONPersister

DIFFCALC_ROOT = os.path.realpath(diffcalc.__file__).split('diffcalc/__init__.py')[0]


try:
    __IPYTHON__  # @UndefinedVariable
    IPYTHON = True
except NameError:
    IPYTHON = False


print "module:", module_name
print "debug:", debug


# configure persisentence
DIFFCALC_VAR = os.path.join(os.path.expanduser('~'), '.diffcalc', module_name)
if not os.path.exists(DIFFCALC_VAR):
    print "Making diffcalc var folder:'%s'" % DIFFCALC_VAR
    os.makedirs(DIFFCALC_VAR)
diffcalc.settings.ubcalc_persister = UBCalculationJSONPersister(DIFFCALC_VAR)

# configure debug
diffcalc.util.DEBUG = debug
if debug:
    print "WARNING: debug mode on; help for command syntax errors disabled."

# import script
script = os.path.join(DIFFCALC_ROOT, 'startup', module_name) + '.py'
print '-' * 79
print "Executing startup script: '%s'" % script    
namespace = {}
execfile(script, namespace)
globals().update(namespace)
print '-' * 79

# magic commands if IPython
if IPYTHON:
    from diffcmd.ipython import magic_commands
    magic_commands(globals())
    print '-' * 79
    
if 'MANUALS_TO_MAKE' in locals():
    from diffcmd.make_manual import make_manual
    for source_path in MANUALS_TO_MAKE:  # @UndefinedVariable
        target_path = source_path.split('_template.py')[0] + '_generated.py'
        print '@' * 79
        print "Making manual"
        print "    Source:", source_path
        print "    Target:", target_path
        
    make_manual(source_path, None)
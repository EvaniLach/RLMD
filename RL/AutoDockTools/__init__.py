#############################################################################
#
# Author: Ruth HUEY, Michel F. SANNER
#
# Copyright: M. Sanner TSRI 2000
#
#############################################################################
#
# $Header: /opt/cvs/python/packages/share1.5/AutoDockTools/__init__.py,v 1.54 2011/06/30 20:37:27 sargis Exp $
#
# $Id: __init__.py,v 1.54 2011/06/30 20:37:27 sargis Exp $
# this makes this directory a package

import os
import sys
import getopt
import time
import socket

# from Support.version import __version__
from mglutil import __revision__

# create hostDict with hostMacros accessible by anyone
from AutoDockTools.adthosts import hostMacros
from AutoDockTools.autodockHosts import AutoDockHosts

hostDict = AutoDockHosts(hostMacros)

h = socket.gethostname()
hostDict[h] = hostDict["localhost"]
hostDict[h]["host"] = h
del hostDict["localhost"]

# try to extend that dictionary with user specific hostMacros

# first try to find a adthost file in current directory
if os.path.isfile("./adthosts.py"):
    exec(compile(open("./adthosts.py", "rb").read(), "./adthosts.py", 'exec'))
    if "hostMacros" in globals():
        hostDict.update(hostMacros)
elif os.name != "nt":  # sys.platform!='win32':
    # try to find the user's home directory
    import posix

    if "HOME" in list(posix.environ.keys()):
        try:
            exec(compile(open(os.path.join(posix.environ["HOME"], "adthosts.py"), "rb").read(), os.path.join(posix.environ["HOME"], "adthosts.py"), 'exec'))
            if "hostMacros" in globals():
                hostDict.update(hostMacros)
        except:
            pass

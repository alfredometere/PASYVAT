#!/usr/bin/env python
greeter = """
PASYVAT version 1.0
PA.rticle SY.stems V.isual A.nalysis T.ool

(C) Alfredo Metere, 2012. All rights reserved.

This software is licensed as GPLv3.
"""

print greeter

print "Loading general modules:"
print "Qt4.QtGui ...",
from PyQt4.QtGui import QApplication
print "Done!"

print "Sys ...",
import sys
print "Done!"

print "\nLoading GUI descriptors modules:"
print "Mainwin ... ",
from modules.gui import mainwin
#from modules.gui import mainwin
print "Done!"

print "\nLoading Analysis Modules:"
print "RDist ... ",
from modules.analysis import rdist
print "Done!"

print "\nInitializing application ..."
app = QApplication(sys.argv)
mw = mainwin.MainWindow()
print "Enjoy!"

mw.show()

sys.exit(app.exec_())

**** PASYVAT ****

-- INSTALLATION INSTRUCTIONS FOR WINDOWS --
-- WINDOWS PREREQUISITES --

In this directory you can find all the prerequisites for Windows, ready to be installed.

Currently PASYVAT is tested to work in Windows 7 32/64 bit.

The installation order is the following:

 1) python-2.7.9.msi
 2) vcredist_x86.exe
 3) winsdk_web.exe
 4) Install Microsoft Visual C++ 2008 Express SP1 (exactly this version)
 5) mingw-get-inst-20120426.exe
 6) numpy-MKL-1.7.1win32-py2.7.exe
 7) PyQt-Py2.7-x32-gpl-4.9.6-1.exe
 8) PyQwt-5.2.1-py2.7-x32-pyqt4.9.6-numpy1.7.1.exe
 9) formlayout-1.0.13.win32-py2.7.exe
10) guidata-1.6.1.win32-py2.7.exe
11) guiqwt-2.3.1.win32-py2.7.exe

GENERAL RULE:
DO NOT CHANGE THE STANDARD INSTALLATION PATHS. LET THE INSTALLERS PROCEED AS AUTOMATIC AS POSSIBLE.

SPECIFIC NOTES (same numbering scheme as above):
1) Tick the option to include python.exe in your PATH
4) Download it from Microsoft. It's free!
3,4,5) If you change installation paths from default, you must update pasyvat.bat with your own installation paths. Avoid it if possible.

Have fun!

Alfredo Metere


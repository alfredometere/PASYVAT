from PyQt4.QtGui import *
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *
from guiqwt import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


from guiqwt.plot import *
from guiqwt.tools import *
from guiqwt.config import *
from guiqwt.builder import *


import vtk
import sys
import csv
import os

from modules.analysis.rdist import rdist
from modules.analysis.bsel  import bsel

from modules.gui import rdfplotwin

from modules.gui import renderwin

#from modules import mainwin

class RDFWin(QWidget):
    def __init__(self,renwin):
        super(RDFWin,self).__init__()
        self.renwin = renwin
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Radial Distribution Calculation")
        self.setMinimumSize(400,400)
        
############################# BUTTONS

        self.calcButton = QPushButton(self)
        self.calcButton.setGeometry(QRect(20,20,98,27))
        self.calcButton.setText("Calculate")
        self.calcButton.setDisabled(True)
        self.calcButton.clicked.connect(self.calcFunc)
        
        self.plotButton = QPushButton(self)
        self.plotButton.setGeometry(QRect(20,60,98,27))
        self.plotButton.setText("Plot")
        self.plotButton.setDisabled(True)
        self.plotButton.clicked.connect(self.plotFunc)

       
############################ BOXES

        self.npxbox = QSpinBox(self)
        self.npxbox.setGeometry(QRect(20,130,98,42))
        self.npxbox.setMinimum(100)
        self.npxbox.setMaximum(1000000)
        self.npxbox.setValue(200)
        self.npxbox.valueChanged.connect(self.changeFunc)
        
        self.rcutbox = QDoubleSpinBox(self)
        self.rcutbox.setGeometry(QRect(20,180,98,42))
        self.rcutbox.setValue(3.5)
        self.rcutbox.valueChanged.connect(self.changeFunc)
#        
#        self.memlimit = QSpinBox(self)
#        self.memlimit.setGeometry(QRect(20,230,98,42))
#        self.memlimit.setMinimum(128)
#        self.memlimit.setMaximum(1048576)
#        self.memlimit.setValue(32768)
#        self.memlimit.valueChanged.connect(self.changeFunc)

########################### LABELS
        
        self.npxlabel = QLabel(self)
        self.npxlabel.setGeometry(QRect(130,140,201,20))
        self.npxlabel.setText("Histogram Points")
    
        self.rcutlabel = QLabel(self)
        self.rcutlabel.setGeometry(QRect(130,190,201,20))
        self.rcutlabel.setText("Cut-off Radius")
        

        
########################## FUNCTIONS

    def changeFunc(self):
        self.plotButton.setDisabled(True)
        try:
            self.plotwin.hide()
        except:
            print "No plot window generated"

    def importData(self,table_exp):
        self.table_exp = table_exp

    def calcRDFFunc(self):
        self.show()
        
    def calcFunc(self):
        print "Computing system radial distribution"
        print "Histogram points: ", self.npxbox.value()
        print "Cut-off radius: ", self.rcutbox.value()
        
        

        npx = self.npxbox.value()
        coords = self.table_exp
        rcut = self.rcutbox.value()

        self.rdf_y, self.rdf_x = rdist(npx,coords,rcut)

        print "done"
        self.plotButton.setEnabled(True)

    
    def plotFunc(self):
       
        # Plot for DAXPY Performance comparison
        plot_title = """
                Radial Distribution Function
                Points:   %g
                Cut-off:  %g
        """ % (self.npxbox.value(),self.rcutbox.value())

        self.plotwin = rdfplotwin.PlotWindow(self.table_exp, self.renwin)
        self.plotwin.show()
        self.plotwin.add_plot(self.rdf_x, self.rdf_y, "RDF")
        self.plotwin.setup_window()
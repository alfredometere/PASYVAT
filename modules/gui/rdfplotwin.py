from guidata.qt.QtGui import *
from guidata.qt.QtCore import *

#---Import plot widget base class
from guiqwt.plot import *
from guiqwt.builder import *
from guiqwt.tools import *
from guiqwt.shapes import *
from guiqwt.styles import *
from guidata.configtools import *
#---

from modules.analysis.bseek import *
from modules.analysis.bidx  import *

class PlotWidget(QWidget):
    """
    Filter testing widget
    parent: parent widget (QWidget)
    x, y: NumPy arrays
    func: function object (the signal filter to be tested)
    """
    def __init__(self, parent, x, y,positions,renwin):
        QWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        self.x = x
        self.y = y
        self.positions = positions
        self.renwin = renwin
        #---guiqwt related attributes:
        self.plot = None
        self.curve_item = None
        self.curve_range = None
        #---
        
    def setup_widget(self, title):
        #---Create the plot widget:
        self.plot = CurvePlot(self,xlabel="r",ylabel="g(r)")
        self.curve_item = make.curve([], [], color='b')
        self.plot.add_item(self.curve_item)
        
        self.plot.set_antialiasing(False)

        self.curve_range1 = make.range(0.2,0.8)
        self.curve_range2 = make.range(1.0,1.3)
        
        
        #self.curve_range3 = make.range(2.5,2.8)
        #self.plot.select_item(self.curve_item)

        #---


        self.selButton = QPushButton(u"Select Range")
        self.selButton.clicked.connect(self.select_data)
        
        self.button = QPushButton(u"Calculate Bonds")
        self.button.clicked.connect(self.process_data)
        self.button.setDisabled(True)
        
        self.resetButton = QPushButton(u"Reset")
        self.resetButton.clicked.connect(self.reset_view)
        self.resetButton.setDisabled(True)
        
        vlayout = QVBoxLayout()
        vlayout.addWidget(self.plot)
        vlayout.addWidget(self.selButton)
        vlayout.addWidget(self.button)
        vlayout.addWidget(self.resetButton)
        
        self.setLayout(vlayout)
        
        self.update_curve()

    def reset_view(self):
        self.resetButton.setDisabled(True)
        self.selButton.setEnabled(True)
        self.renwin.Clear()
        self.renwin.vtkrenderer.RemoveAllViewProps()
        self.renwin.DrawParticles(self.renwin.points,self.renwin.spheresrc\
                ,self.renwin.pread)
        self.renwin.Render()
        #self.plot.del_item(self.curve_range1)
        self.plot.del_item(self.curve_range2)
        self.update_curve()
    
    def process_data(self):
        self.renwin.Clear()
        if (self.curve_range1 and self.curve_range2):
            dr0 = self.curve_range1.get_range()
            dr1 = self.curve_range2.get_range()
            #dr2 = self.curve_range3.get_range()
            self.xmin0 = dr0[0]
            self.xmax0 = dr0[1]

            self.xmin1 = dr1[0]
            self.xmax1 = dr1[1]

            print "self.xmin0: ", self.xmin0
            print "self.xmax0: ", self.xmax0

            print "self.xmin1: ", self.xmin1
            print "self.xmax1: ", self.xmax1
            
            #self.xmin2 = dr2[0]
            #self.xmax2 = dr2[1]
            # Gets the number of bonds for each given range
            self.bn0 = bondseek(self.positions,self.xmin0,self.xmax0)
            self.bn1 = bondseek(self.positions,self.xmin1,self.xmax1)
            
            #self.bn2 = bondseek(self.couples,self.xmin2,self.xmax2)
            print "rdfplotwin: self.bn0",self.bn0
            print "rdfplotwin: self.bn1",self.bn1

            self.renwin.vtkrenderer.RemoveAllViewProps()
            self.renwin.DrawParticles(self.renwin.points,self.renwin.spheresrc\
                ,self.renwin.pread)
            
            if (self.bn0 > 0):
                self.b0, self.b1 = bond_id(self.positions,self.xmin0,self.xmax0,self.bn0)
                #self.renwin.vtkrenderer.RemoveAllViewProps()
                
                self.renwin.DrawBonds(self.b0,self.b1,0.3,0.7,1.0)
                
                # Checks that the second range has values. If so, it
                # draws the bonds
                
            if (self.bn1 > 0):            
                self.b2, self.b3 = bond_id(self.positions,self.xmin1, self.xmax1, self.bn1)            
                #self.b4, self.b5 = bond_id(self.couples,self.xmin2, self.xmax2, self.bn2)                
                self.renwin.DrawBonds(self.b2,self.b3,1,0.5,0)
                #self.renwin.DrawBonds(self.b4,self.b5,1,0,0.5)
            
            self.renwin.Render()
        
    def select_data(self):
        self.button.setEnabled(True)
        self.selButton.setDisabled(True)
        self.resetButton.setEnabled(True)
        
        self.plot.add_item(self.curve_range1)
        self.plot.add_item(self.curve_range2)
        #self.plot.add_item(self.curve_range3)
        self.update_curve()
        
    def update_curve(self):
        #---Update curve
        self.curve_item.set_data(self.x, self.y)
        self.plot.replot()
        #---
    
    
class PlotWindow(QMainWindow):
    def __init__(self,positions,renwin):
        QMainWindow.__init__(self)
        
        self.positions = positions
        self.renwin = renwin
        
        print "Imported particles: ", len(self.positions)
        self.setWindowTitle("Radial Distribution Function Plot")
        
        hlayout = QHBoxLayout()
        central_widget = QWidget(self)
        central_widget.setLayout(hlayout)
        self.setCentralWidget(central_widget)
        #---guiqwt plot manager
        self.manager = PlotManager(self)
        #---
        self.show()
        
    def add_plot(self, x, y, title):
        widget = PlotWidget(self, x, y, self.positions, self.renwin)
        widget.setup_widget(title)
        self.centralWidget().layout().addWidget(widget)
        #---Register plot to manager
        self.manager.add_plot(widget.plot)
        #---
        
    def setup_window(self):
        #---Add toolbar and register manager tools
        toolbar = self.addToolBar("tools")
        self.manager.add_toolbar(toolbar, id(toolbar))
        for tools in (SelectTool,\
                      SelectPointTool,\
                      PrintTool,\
                      SaveAsTool):
                          self.manager.add_tool(tools)
                          
        self.manager.set_default_tool(SelectTool)
        #self.manager.activate_default_tool()

#!/usr/bin/env python
print "\n --- MainWin modules load:"

print " --- Qt4 ...",
from PyQt4.QtCore import *
from PyQt4.QtGui import *
print "Done!"

print " --- Qt4-QWT ...",
#import PyQt4.Qwt5 as qwt
#from PyQt4.Qwt5 import *
#from PyQt4.Qwt5.qplt import *
from guiqwt import *
from guiqwt.tools import *
from guiqwt.config import _
from guiqwt.plot import CurveDialog
from guiqwt.builder import make
print "Done!"

print " --- Qt4-VTK ...",
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
print "Done!"

print " --- VTK ...",
import vtk
print "Done!"

print " --- Sys ...",
import sys
print "Done!"

print " --- OS ...",
import os
print "Done!"

print " --- GUI: RenderWin ...",
from modules.gui import renderwin
print "Done!"
print " --- GUI: RDFWin ...",
from modules.gui import rdfwin
print "Done!"

from modules.gui import viztooldlg


#########################################################

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        #Definition of dependent Windows
        
        self.rw = renderwin.RenWin()
        self.rdfw = rdfwin.RDFWin(self.rw)
        self.vtb = viztooldlg.VizToolDlg(self.rw)

        # GUI Interface Design
        self.wks = QWorkspace()
        self.setCentralWidget(self.wks)

        # Table for showing particle coordinates
        
        self.PosTabWin = QTableWidget()
        self.PosTabWin.setWindowTitle('Positions')

        self.BondsTable = QTableWidget()
        self.BondsTable.setWindowTitle('Connections')

        self.wks.addWindow(self.PosTabWin)
        self.wks.addWindow(self.BondsTable)
        #self.wks.addWindow(self.rdfw)
        #self.wks.addWindow(self.vtb)
        
        self.BondsTable.hide()
        self.PosTabWin.hide()
        self.rdfw.hide()
        self.vtb.hide()

        self.statusbar = QStatusBar()

        # File Menu Items
        self.openASFile = QAction('Open ...', self)
        self.openASFile.setShortcut('Ctrl+O')
        self.openASFile.triggered.connect(self.fOpenDlg)
        
        self.saveASFile = QAction('Save Snapshot...', self)
        self.saveASFile.setShortcut('Ctrl+S')
        self.saveASFile.triggered.connect(self.fSaveDlg)

        self.exitprog = QAction('Quit', self)
        self.exitprog.setShortcut('Ctrl+Q')
        self.exitprog.triggered.connect(self.exitP)

        # Edit Menu Items
        self.MenuBgColor = QAction("Change &Background Color", self)
        self.MenuBgColor.triggered.connect(self.BgColorPicker)
        
        self.MenuObjColor = QAction("Change &Object Color", self)
        self.MenuObjColor.triggered.connect(self.ObjColorPicker)

        self.MenuSelColor = QAction("Change &Selection Color", self)
        self.MenuSelColor.triggered.connect(self.SelColorPicker)

        self.CropStructure = QAction('Crop structure ...',self)
        self.CropStructure.triggered.connect(self.fCropStruct)
        self.SaveStates = QAction ('Save 3D transformations ...', self)
        self.LoadStates = QAction ('Load 3D transformations ...', self)

        # Window Menu Items
        self.showRenWin = QAction('Render Window', self)
        self.showRenWin.setShortcut('Ctrl+R')
        self.showRenWin.setStatusTip('Shows render window')
        self.showRenWin.triggered.connect(self.rw.showRenWinFunc)

        self.showPosWin = QAction('Particle positions',self)
        self.showPosWin.setShortcut('Ctrl+Alt+P')
        self.showPosWin.setStatusTip('Shows particle positions table window')
        self.showPosWin.triggered.connect(self.showPosWinFunc)
        
        self.showVizTool = QAction("Render Toolbar",self)
        self.showVizTool.triggered.connect(lambda e: self.vtb.show())

        # Calculate Menu Items
        self.calcRDFWin = QAction('RDF', self)
        self.calcRDFWin.triggered.connect(self.rdfw.calcRDFFunc)

        # Visualization Menu Items

        self.showSphere = QAction('Spheres representation', self)
        self.showSphere.triggered.connect(self.rw.ReprSpheres)
        
        self.showPoints = QAction('Points representation', self)
        self.showPoints.triggered.connect(self.rw.ReprPoints)
        
        self.showHiResSphere = QAction('HiRes Spheres', self)
        self.showHiResSphere.triggered.connect(self.rw.ReprHires)
        
        
        self.OrthoView = QAction('&Orthogonal',self)
        self.OrthoView.triggered.connect(self.rw.OrthoFunc)
        
        self.PerspView = QAction('&Perspective',self)
        self.PerspView.triggered.connect(self.rw.PerspFunc)

        self.ResetCam = QAction('&Reset Camera', self)
        self.ResetCam.triggered.connect(self.rw.ResetCamFunc)

        # Menu Bar items
        self.menubar = self.menuBar()
        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.openASFile)
        self.fileMenu.addAction(self.saveASFile)
        self.fileMenu.addAction(self.exitprog)

        self.editMenu = self.menubar.addMenu('&Edit')
        self.editMenu.addAction(self.MenuBgColor)
        self.editMenu.addAction(self.MenuObjColor)
        self.editMenu.addAction(self.MenuSelColor)
        self.editMenu.addAction(self.CropStructure)
        self.editMenu.addAction(self.SaveStates)
        self.editMenu.addAction(self.LoadStates)

        self.WinMenu = self.menubar.addMenu('&Windows')
        self.WinMenu.addAction(self.showPosWin)
        self.WinMenu.addAction(self.showRenWin)
        self.WinMenu.addAction(self.showVizTool)

        self.RenMenu = self.menubar.addMenu('&View')
        self.RenMenu.addAction(self.showSphere)
        self.RenMenu.addAction(self.showPoints)
        self.RenMenu.addAction(self.showHiResSphere)
        self.RenMenu.addAction(self.OrthoView)
        self.RenMenu.addAction(self.PerspView)
        self.RenMenu.addAction(self.ResetCam)

        self.CalcMenu = self.menubar.addMenu('&Compute')
        self.CalcMenu.addAction(self.calcRDFWin)

        self.setGeometry(300, 300, 650, 600)
        self.setWindowTitle('PASYVAT v. 0.9.0')

        self.saveASFile.setDisabled(True)
        self.showPosWin.setDisabled(True)
        self.showRenWin.setDisabled(True)
        self.OrthoView.setDisabled(True)
        self.PerspView.setDisabled(True)
        self.calcRDFWin.setDisabled(True)
        self.SaveStates.setDisabled(True)
        self.LoadStates.setDisabled(True)
        
    def BgColorPicker(self):
        self.colPickerDlg = QColorDialog(self)
        self.color = self.colPickerDlg.getColor()
        rgb = [self.color.redF(), self.color.greenF(), self.color.blueF()]
        self.rw.vtkrenderer.SetBackground(rgb)
        self.rw.Render()
        
    def ObjColorPicker(self):
        self.colPickerDlg = QColorDialog(self)
        self.color = self.colPickerDlg.getColor()
        rgb = [self.color.redF(), self.color.greenF(), self.color.blueF()]
        self.rw.psetAct.GetProperty().SetColor(rgb)
        self.rw.Render()

    def SelColorPicker(self):
        self.colPickerDlg = QColorDialog(self)
        self.color = self.colPickerDlg.getColor()
        rgb = [self.color.redF(), self.color.greenF(), self.color.blueF()]
        self.rw.selectActor.GetProperty().SetColor(rgb)
        self.rw.Render()
        
    def fOpenDlg(self,ifilename = None):
        self.ifname = QFileDialog.getOpenFileName(self, 'Open file', './',\
                     'CSV (*.csv);;OUT(*.out)')

        # If you cancel in the file selection dialog, this condition will be
        # equal to 0. No meaning to proceed further
        if (len(self.ifname) > 0):
            self.f = open(self.ifname, 'r')
            self.PosTabWin_title = 'Positions ' + str(self.ifname)

            self.PosTabWin.setWindowTitle(self.PosTabWin_title)
            self.if_name, self.if_ext = os.path.splitext(str(self.ifname))

        #file_filters        
        # Important that everything happens only if a file is selected from the
        # file dialog
            #self.rw = renderwin.RenWin()

            self.preader = vtk.vtkParticleReader();            
            
            if (self.if_ext == ".csv"):

#Particle Reader
                self.preader.SetFileName(str(self.ifname))
                self.preader.SetDataByteOrderToBigEndian()
                self.preader.Update()
                
                from modules.fio.csv_reader import csv_reader
                self.t_exp,                             \
                self.pn,                                \
                self.points = csv_reader(self.ifname)
                
            if (self.if_ext == ".out"):
                from modules.fio.out_reader import out_reader
                self.t_exp,                             \
                self.pn,                                \
                self.points = out_reader(self.ifname)
            # Updates positions table
            self.updatePosTable()
            
            # Draws the particles
            self.rw.importData(self.t_exp)

            #self.rw.preader(self.preader)            
                # VTK Version
    
            vtkHver = vtk.vtkVersion().GetVTKMajorVersion()
            vtkLver = vtk.vtkVersion().GetVTKMinorVersion()
            
            if (vtkHver > 5):
                self.rw.DrawParticles(self.points,self.rw.pointsrc,self.preader)
            else:
                self.rw.DrawParticles(self.points,self.rw.pointsrc,self.preader)
            #self.rw.DrawParticles(self.points,self.rw.pointsrc) #quadsrc//pointsrc

            #self.rw.show()
            #self.rw.drawAxes()
            #self.rw.Render()

            
            # Enables RDF Calculation
            self.rdfw.importData(self.t_exp)
            self.rdfw.calcButton.setEnabled(True)
            self.rw.show()
            
            self.saveASFile.setEnabled(True)
            self.showPosWin.setEnabled(True)
            self.showRenWin.setEnabled(True)
            self.OrthoView.setEnabled(True)
            self.PerspView.setEnabled(True)
            self.calcRDFWin.setEnabled(True)

    def fSaveDlg(self):
        self.ofname = QFileDialog.getSaveFileNameAndFilter(self, 'Save file', './', \
                      'JPEG (*.jpg);;TIFF (*.tif);;BMP (*.bmp)')
         
        self.rw.CaptureImage(str(self.ofname[0]),str(self.ofname[1]))

    def exitP(self):
        quit()

    def closeFunc(self):
        quit()
    
    def closeEvent(self, ce):
        quit()

    def fCropStruct(self):
        from modules.analysis import cseek
        print cseek.__doc__
        self.t = vtk.vtkTransform()
        self.t2 = vtk.vtkTransform()
        self.rw.boxWidget.GetTransform(self.t)
        print "----- CropStruct ----------------------"
        print "Orientation: ", self.t.GetOrientation()
        print "Position: ", self.t.GetPosition()
        print "Scale: ", self.t.GetScale()
        print "---------------------------------------"
        print "Camera orientation: ", self.rw.scenecam.GetOrientation()

        cpn = self.rw.clipper.GetOutput().GetVerts().GetNumberOfCells()
        
        print "Number of particles selected: ", cpn


        print self.rw.clipper.GetOutput().GetPointData()
        
        #print self.rw.clipper.GetClippedOutput()
        
        clippedpoints = self.rw.clipper.GetOutput()
        
        print clippedpoints

        #alpha,beta,gamma = self.rw.scenecam.GetOrientation()

        #print alpha,beta,gamma        

        #xmin, xmax, ymin, ymax, zmin, zmax = self.rw.selectActor.GetBounds()
        
        #print xmin, ymin, zmin
        #print xmax, ymax, zmax

        #cseek.cseek(xmin,xmax,ymin,ymax,zmin,zmax,self.t_exp)        
        
        #self.t2 = self.rw.scenecam.GetViewTransformObject()
        
        
        #self.rw.boxWidget.SetTransform(self.t2)
        #self.rw.Render()
        
        #self.clipdata = self.rw.clipper.GetClippedOutput()
        
        #print self.clipdata
        
    def updatePosTable(self):
        
        self.PosTabWin.setRowCount(self.pn)
        self.PosTabWin.setColumnCount(3)
        self.PosTabWin.setHorizontalHeaderLabels(['X','Y','Z'])
        for i in range(0,self.pn):
            x = str(self.t_exp[i][0])
            y = str(self.t_exp[i][1])
            z = str(self.t_exp[i][2])
            
            tx = QTableWidgetItem()
            tx.setText(x)         

            ty = QTableWidgetItem()
            ty.setText(y)
            
            tz = QTableWidgetItem()
            tz.setText(z)

            self.PosTabWin.setItem(i,0,tx)
            self.PosTabWin.setItem(i,1,ty)
            self.PosTabWin.setItem(i,2,tz)
            
        self.PosTabWin.showMaximized()

    def showPosWinFunc(self):
        self.PosTabWin.show()        

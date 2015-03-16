#!/usr/bin/env python
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qwt5 import *
from PyQt4.Qwt5.qplt import *
from guiqwt import *
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

import vtk
import sys
import csv
import os

from modules.gui import viztooldlg


# This callback funciton does the actual work: updates the vtkPlanes
# implicit function.  This in turn causes the pipeline to update.
#def SelectPolygons(object, event):
#    # object will be the boxWidget
#    global selectActor, planes
#    object.GetPlanes(planes)
#    selectActor.VisibilityOn()

#def bSelectPolygons(object, event):
#    # object will be the boxWidget
#    global bselectActor, bplanes
#    object.GetPlanes(bplanes)
#    bselectActor.VisibilityOn()

    



  
class RenWin(QVTKRenderWindowInteractor):
    def __init__(self):
        super(RenWin,self).__init__()
        self.init_ui()

    def init_ui(self):
        #global self.scenecam
        # Initializes the Rendering window, defining only basic parameters
        # Window Title and Camera

        # Global Axes definition
        self.axact = vtk.vtkAxesActor()
        self.ormark = vtk.vtkOrientationMarkerWidget()
        self.ormark.SetOutlineColor(0.93,0.57,0.13)
        self.ormark.SetOrientationMarker(self.axact)
        
        #self.ormark.SetViewport(0.0,0.0,0.2,0.2)
        

        self.boxinit = bool
        self.boxinit = False


        # Sphere radii l = low res, H = hi res
        self.rl = 0.175
        self.rh = 0.175        
        
        # Sphere resolution L = low res, H = hi res
        self.phiL = 8
        self.thetaL = 8
        self.phiH = 32
        self.thetaH = 32        
        
        self.apd = vtk.vtkAppendPolyData()

        #self.vtb = viztooldlg.VizToolDlg(self)

        #self.vtb.show()
        
        self.selectActor = vtk.vtkActor()
        self.psetAct = vtk.vtkActor()

        self.spheresrc = vtk.vtkSphereSource()
        self.spheresrc.SetCenter(0, 0, 0)
        self.spheresrc.SetRadius(self.rl)
        # self.spheresrc.SetRadius(0.275)
        # This value has been used for the PRL paper
        self.spheresrc.SetPhiResolution(self.phiL)
        self.spheresrc.SetThetaResolution(self.thetaL)
        
        self.hispheresrc = vtk.vtkSphereSource()
        self.hispheresrc.SetCenter(0, 0, 0)
        self.hispheresrc.SetRadius(self.rh)
        # self.spheresrc.SetRadius(0.275)
        # This value has been used for the PRL paper
        self.hispheresrc.SetPhiResolution(self.phiH)
        self.hispheresrc.SetThetaResolution(self.thetaH)

        self.quadsrc = vtk.vtkPlaneSource()        

        self.quadsrc.SetCenter(0.0, 0.0, 0.0)

        
        self.pointsrc = vtk.vtkPointSource()
        
        self.mapper = vtk.vtkPolyDataMapper()

        self.setWindowTitle('PASYVAT Render Window')
        
        # By default parallel projection is selected
        self.scenecam = vtk.vtkCamera()
        self.scenecam.ParallelProjectionOn()

        self.vtkrenderer = vtk.vtkRenderer()        
        
        self.vtkrenderer.SetActiveCamera(self.scenecam)
        self.vtkrenderer.ResetCamera()

        self.boxWidget = vtk.vtkBoxWidget()        
        self.clipper = vtk.vtkClipPolyData()
        
        
        self.glyph = vtk.vtkGlyph3D()

        self.planes = vtk.vtkPlanes()
        self.selectMapper = vtk.vtkPainterPolyDataMapper()

        #self.SetInteractorStyle(vtk.vtkInteractorStyleUser())
        #self.SetInteractorFuncs()
        self.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.GetRenderWindow().AddRenderer(self.vtkrenderer)
        self.vtkrenderer.SetBackground(0.0,0.4,1.0)
        #self.vtkrenderer.SetBackground(0,0,0)
        #self.drawAxes()
        self.AddObserver("StartInteractionEvent",self.KeypressEVT)
        self.AddObserver("KeyPressEvent", self.KeypressEVT)
        
    def SetInteractorFuncs(self):
        
        self.AddObserver("KeyPressEvent", self.KeypressEVT)
        
        self.AddObserver("LeftButtonPressEvent", vtk.Rotate())
        #self.AddObserver("LeftButtonPressEvent", self.SetRotating(0))
        
    def Clear(self):
        self.vtkrenderer.RemoveAllViewProps()
        self.vtkrenderer.ResetCamera()
        self.Render()        

    def OrthoFunc(self,idd):
        self.scenecam.ParallelProjectionOn()
        self.Render()

    def PerspFunc(self,idd):
        self.scenecam.ParallelProjectionOff()
        self.Render()

    def showRenWinFunc(self):
        self.show()
    
    def ResetCamFunc(self):
        self.vtkrenderer.ResetCamera()
        self.Render()

    def importData(self,table_exp):
        self.table_exp = table_exp

    def drawAxes(self):
        self.ormark.SetInteractor(self)
        self.ormark.SetEnabled(1)
        self.ormark.InteractiveOff()
        self.ormark.On()
        
#        self.Render()

    def KeypressEVT(self,object,event):
    
        key = object.GetKeyCode()


        
        if key == "e":
            quit()
        
        if key == "i":
            #self.drawAxes()
            self.Render()
        
        if key == "b":
            print "Starting Slicing Tool"
            self.boxinit = True
            self.Interaction(object,event)
            
            
        if key == "n":
            #print key, " pressed"
            #print "boxinit = ", self.boxinit
            if self.boxinit == True:
                print "Restarting Slicing Tool"
                self.boxWidget.On()
                #self.drawAxes()
                self.Render()
                
        if key == "m":
            #print key, " pressed"
            #print "boxinit = ", self.boxinit
            if self.boxinit == True:
                print "Deactivating Slicing Tool"
                self.boxWidget.Off()
                #self.drawAxes()
                self.Render()
                
        if key == "v":
            if self.boxinit == True:
                print "Toggle handles"
                if self.handles_status == True:
                    self.boxWidget.HandlesOff()
                    self.boxWidget.OutlineCursorWiresOff()
                    self.boxWidget.TranslationEnabledOff()
                    self.boxWidget.ScalingEnabledOff()
                    self.boxWidget.RotationEnabledOff()
                    self.handles_status = False
                else:
                    if self.handles_status == False:
                        self.boxWidget.HandlesOn()
                        self.boxWidget.OutlineCursorWiresOn()
                        self.boxWidget.TranslationEnabledOn()
                        self.boxWidget.ScalingEnabledOn()
                        self.boxWidget.RotationEnabledOn()
                        self.handles_status = True
                    
            self.Render()
        
        if key == "+":
            rl = self.spheresrc.GetRadius() + (0.01 * self.rl )
            rh = self.hispheresrc.GetRadius() + (0.01 * self.rh )
            # In the csv_reader module I scaled the coordinates to:
            #                                         2 * self.rl = 0.35
            # For this reason the displayed value is diameter and not radius
            print "Increased sphere diameter (Reduced units): %f" % (rl / self.rl)
            #print "Increased Hi-Sphere diameter (Reduced units): %f" % (rh / self.rh)
            self.spheresrc.SetRadius(rl)
            self.hispheresrc.SetRadius(rh)
            
            self.Render()
            
        if key == "-":
            rl = self.spheresrc.GetRadius() - (0.01 * self.rl)
            rh = self.hispheresrc.GetRadius() - (0.01 * self.rh)
            

            self.spheresrc.SetRadius(rl)
            self.hispheresrc.SetRadius(rh)
            print "Decreased sphere diameter (Reduced units) to   : %f" % (rl / self.rl)
            #print "Decreased Hi-Sphere diameter (Reduced units) to: %f" % (rh / self.rh)
            self.Render()              

        if key == "=":
            rl = self.rl
            rh = self.rh
            self.spheresrc.SetRadius(rl)
            self.hispheresrc.SetRadius(rh)
            print "Reset sphere diameter to (Reduced units)  : %f" % (rl / self.rl)
            #print "Reset hi-res sphere diameter to (Reduced units): %f" % (rh / self.rh)
            self.Render()              

        
        if key == "h":
            print key, " pressed"
            helpmessage = """
Render Window Commands Help
    b - Start Slicing Tool
    n - Restart Slicing Tool
    m - Deactivate Slicing Tool
    v - Toggle Handles
    + - Increase sphere radius
    - - Decrease sphere radius
    h - Show this message
"""
            print helpmessage
            

    def DrawParticles(self,points,source,pread):
        self.points = points
        self.pread = pread
        self.handles_status = True;
        # Creates the source geometry
        #geomsrc = vtk.vtkSphereSource()
        #geomsrc = vtk.vtkPointSource()
        
        self.pointsrc.SetNumberOfPoints(1)
        self.pointsrc.SetCenter(0,0,0)
        self.pointsrc.SetRadius(1.0)


        
        # Basically creates a display list
        self.pset = vtk.vtkPolyData()
        self.pset.SetPoints(points)
        
        # Associates display list with geometry source

        
        self.glyph.SetInputConnection(self.pset.GetProducerPort())
        #self.glyph.SetOrient(1)
        #self.glyph.SetColorMode(2)
        #self.glyph.SetScaleMode(2)
        #self.glyph.SetScaleFactor(0.5)
        self.glyph.GeneratePointIdsOn()
        self.glyph.SetSourceConnection(source.GetOutputPort())
        
     
        self.mapper.SetInputConnection(self.glyph.GetOutputPort())

        #self.mapper.SetInputConnection(self.pread.GetOutputPort())        
        
        self.mapper.ImmediateModeRenderingOn()
        self.mapper.UseLookupTableScalarRangeOn()
        self.mapper.ScalarVisibilityOn()
        self.mapper.SetScalarModeToDefault()

        # Creates the Render Actor (Entity visible on the render window)
        
        self.psetAct.SetMapper(self.mapper)
        self.psetAct.GetProperty().LightingOn()
        #self.psetAct.GetProperty().SetOpacity(0.5)
        self.psetAct.GetProperty().BackfaceCullingOff()
        #self.psetAct.GetProperty().SetRepresentationToSurface()
        #self.psetAct.GetProperty().SetInterpolationToGouraud()
        self.psetAct.GetProperty().SetAmbient(0.15)
        self.psetAct.GetProperty().SetDiffuse(0.6)
        self.psetAct.GetProperty().SetSpecular(1.0)
        self.psetAct.GetProperty().SetSpecularPower(50)
        self.psetAct.GetProperty().SetSpecularColor(0.5,1,1)
        self.psetAct.GetProperty().LoadMaterial("materials/fog.xml")
        self.psetAct.GetProperty().SetPointSize(1.0)
        
        #self.psetAct.GetProperty().ShadingOn()
        
        # Adds the Render Actor to the Render Window
        
        self.apd.AddInput(self.glyph.GetOutput())
        
        # This portion of the code clips the bonds with the vtkPlanes implicit
        # function.  The clipped region is colored green.
       
        self.clipper.SetInputConnection(self.apd.GetOutputPort())
        
        
        self.clipper.SetClipFunction(self.planes)
       
        self.clipper.InsideOutOn()
        self.clipper.GenerateClippedOutputOn()

        
        
        self.selectMapper.SetInputConnection(self.clipper.GetOutputPort())

        self.selectActor.SetMapper(self.selectMapper)
        self.selectActor.GetProperty().SetColor(1, 0.4, 1)
        self.selectActor.VisibilityOff()
        self.selectActor.SetScale(1.0, 1.0, 1.0)
        self.selectActor.GetProperty().LoadMaterial("materials/fog.xml")
        #self.selectActor.GetProperty().ShadingOn()
        
        self.boxWidget.SetInteractor(self)
        self.boxWidget.SetPlaceFactor(1.0)
        
        self.vtkrenderer.AddActor(self.psetAct)       
        self.vtkrenderer.AddActor(self.selectActor)

        self.boxWidget.SetInput(self.apd.GetOutput())
        #self.boxWidget.AddObserver("StartInteractionEvent", self.StartInteraction)
        #self.boxWidget.AddObserver("StartInteractionEvent", self.StartInteraction)
        self.boxWidget.AddObserver("InteractionEvent",self.Cutme)
        #self.boxWidget.AddObserver("EndInteractionEvent", self.EndInteraction)

     
        self.Initialize()
        self.GetRenderWindow().Render()
        self.Start()
        self.ResetCamFunc()
        #self.drawAxes()

    def StartInteraction(self,o,e):
        self.psetAct.VisibilityOff()
        self.boxWidget.PlaceWidget()
        self.boxWidget.SetEnabled(1)
        self.boxWidget.GetPlanes(self.planes)
        self.selectActor.VisibilityOn()

        self.Render()

    def Interaction(self,o,e):
        print o.GetKeyCode(),"pressed"
        #self.drawAxes()
        #
        self.psetAct.VisibilityOff()
        #
        self.boxWidget.PlaceWidget()
        self.boxWidget.SetEnabled(1)
        self.boxWidget.On()
        self.boxWidget.GetPlanes(self.planes)
        
        
        self.selectActor.VisibilityOn()
        #self.drawAxes()
        self.Render()
        
        
    def Cutme(self,o,e):
        self.boxWidget.GetPlanes(self.planes)
        self.Render()
        
    def EndInteraction(self,o,e):
        #self.drawAxes()
        self.Render()

    def ReprHires(self):
        self.glyph.SetSourceConnection(self.hispheresrc.GetOutputPort())
        self.Render()
        
    def ReprSpheres(self):
        self.glyph.SetSourceConnection(self.spheresrc.GetOutputPort())
        self.Render()
        
    def ReprPoints(self):
        self.glyph.SetSourceConnection(self.pointsrc.GetOutputPort())
        self.Render()

    def DrawBonds(self,b0,b1,r,g,b):

     
        bn = len(b0)
        
        points = vtk.vtkPoints()
        for i in range(0,bn):

            x0 = self.table_exp[b0[i]][0]
            y0 = self.table_exp[b0[i]][1]
            z0 = self.table_exp[b0[i]][2]

            points.InsertNextPoint(x0,y0,z0)

        for j in range(0,bn):

            x1 = self.table_exp[b1[j]][0]
            y1 = self.table_exp[b1[j]][1]
            z1 = self.table_exp[b1[j]][2]

            points.InsertNextPoint(x1,y1,z1)
        
        lines = vtk.vtkCellArray()
        for i in range(0,bn):
            lines.InsertNextCell(2)
            lines.InsertCellPoint(i)
            lines.InsertCellPoint(i+bn)
        
        
        self.pd = vtk.vtkPolyData()
        self.pd.SetPoints(points)
        self.pd.SetLines(lines)
        
        self.tube = vtk.vtkTubeFilter()
        self.tube.SetInput(self.pd)
        self.tube.SetRadius(0.05)
        self.tube.SetNumberOfSides(16)
 
#       Cut function implemented in bonds mode       
#        apd.AddInput(tube.GetOutput())

        self.bmapper = vtk.vtkPolyDataMapper()
        self.bmapper.SetInputConnection(self.tube.GetOutputPort())
        self.bmapper.ScalarVisibilityOn()
        self.bmapper.SetScalarModeToUsePointFieldData()

        self.act = vtk.vtkActor()
        self.act.SetMapper(self.bmapper)
        self.act.GetProperty().SetColor(r,g,b)

        #self.apd.AddInput(pd)
        self.Render()
        #self.glyph.Update()
        self.vtkrenderer.AddActor(self.act)
        #self.drawAxes()
    
    def CaptureImage(self,fname,fformat):

        w2i = vtk.vtkWindowToImageFilter()

        if fformat == 'TIFF (*.tif)':
            writer = vtk.vtkTIFFWriter()
            self.fname = fname + ".tif"
        if fformat == 'BMP (*.bmp)':
            writer = vtk.vtkBMPWriter()
            self.fname = fname + ".bmp"
        if fformat == 'JPEG (*.jpg)':
            writer = vtk.vtkJPEGWriter()
            self.fname = fname + ".jpg"
        
        w2i.SetInput(self.GetRenderWindow())
        w2i.Update()

        print "Generating Large image"

        renderlarge=vtk.vtkRenderLargeImage()
        renderlarge.SetInput(self.vtkrenderer)
        renderlarge.SetMagnification(10)        
        
        writer.SetInputConnection(renderlarge.GetOutputPort())
        writer.SetFileName(self.fname)
        
        writer.Write()        
        
           
        

        

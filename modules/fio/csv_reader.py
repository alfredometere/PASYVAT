# -*- coding: utf-8 -*-
"""
CSV File Format Reader

table_exp, pn, points = csv_reader(fname)

Input: File name
Output: Positions Array, Number of Particles, VTK Point Elements
"""
import vtk
  
def csv_reader(fname):

    # VTK Version
    
    vtkHver = vtk.vtkVersion().GetVTKMajorVersion()
    vtkLver = vtk.vtkVersion().GetVTKMinorVersion()
    
    reader = vtk.vtkDelimitedTextReader()
    reader.DetectNumericColumnsOn()
    reader.SetFieldDelimiterCharacters(",")
    reader.SetFileName(str(fname))
    # Trying to use VTK 6 
    if (vtkHver <= 5):
        reader.GetOutput().ReleaseDataFlagOn()
    reader.Update()
    print 'Creating a Data Table for the file: ',fname

    PosTable = reader.GetOutput()
    points = vtk.vtkPoints()
           
    pn = PosTable.GetNumberOfRows()
    table_exp = pn * [None]
    
    print 'Number of atoms: ',pn
    for i in range(0,pn):
        x,y,z = PosTable.GetValue(i,0).ToDouble(),\
                PosTable.GetValue(i,1).ToDouble(),\
                PosTable.GetValue(i,2).ToDouble()
    
        # Debug output of x,y,z
        # print 'P',i,': ',x,y,z
        x, y, z = x * 0.35, y * 0.35, z * 0.35
        table_exp[i] = [x,y,z]
        points.InsertNextPoint(x, y, z)

    print 'Particles loaded: ', points.GetNumberOfPoints()
   
    return table_exp, pn, points

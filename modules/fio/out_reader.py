# -*- coding: utf-8 -*-
"""
OUT File Format Reader

table_exp, pn, points = out_reader(fname)

Input: File name
Output: Positions Array, Number of Particles, VTK Point Elements
"""
import vtk
    
def out_reader(fname):
   
    reader = vtk.vtkDelimitedTextReader()
    reader.DetectNumericColumnsOn()
    reader.SetFieldDelimiterCharacters(" ")
    reader.SetFileName(str(fname))
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
        table_exp[i] = [x,y,z]
        points.InsertNextPoint(x, y, z)

    print 'Particles loaded: ', points.GetNumberOfPoints()

    return table_exp, pn, points
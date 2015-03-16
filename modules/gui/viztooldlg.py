# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 18:02:14 2012

@author: alfredo
"""

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

class VizToolDlg(QWidget):
    def __init__(self, renwin):
        super(VizToolDlg,self).__init__()
        self.renwin = renwin
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Parametric Rotation Controls")
        self.setMinimumSize(868,505)
        
        self.gamma_angle_counter = QwtCounter(self)
        self.gamma_angle_slider = QwtSlider(self)
        self.gamma_angle_label = QLabel(self)
        self.beta_angle_label = QLabel(self)
        self.alpha_angle_label = QLabel(self)
        self.gamma_angle_counter_2 = QwtCounter(self)
        self.gamma_angle_slider_2 = QwtSlider(self)
        self.gamma_angle_counter_3 = QwtCounter(self)
        self.gamma_angle_slider_3 = QwtSlider(self)
        self.gamma_angle_counter_4 = QwtCounter(self)
        self.gamma_angle_counter_5 = QwtCounter(self)
        self.gamma_angle_slider_4 = QwtSlider(self)
        self.gamma_angle_counter_6 = QwtCounter(self)
        self.gamma_angle_slider_5 = QwtSlider(self)
        self.gamma_angle_slider_6 = QwtSlider(self)
        self.gamma_angle_counter_7 = QwtCounter(self)
        self.gamma_angle_counter_8 = QwtCounter(self)
        self.gamma_angle_slider_7 = QwtSlider(self)
        self.gamma_angle_counter_9 = QwtCounter(self)
        self.gamma_angle_slider_8 = QwtSlider(self)
        self.gamma_angle_slider_9 = QwtSlider(self)
        self.label = QLabel(self)
        self.label_2 = QLabel(self)
        self.label_3 = QLabel(self)
        self.label_4 = QLabel(self)
        self.label_5 = QLabel(self)
        self.label_6 = QLabel(self)
        self.label_7 = QLabel(self)
        self.label_8 = QLabel(self)
        self.label_9 = QLabel(self)
        self.line = QFrame(self)
        self.line_2 = QFrame(self)
        self.font = QFont(self)
        
        self.gamma_angle_counter.setObjectName(QString("gamma_angle_counter"))
        self.gamma_angle_counter.setGeometry(QRect(20, 410, 271, 29))
        
        self.gamma_angle_slider.setObjectName(QString("gamma_angle_slider"))
        self.gamma_angle_slider.setGeometry(QRect(20, 450, 271, 21))
        
        self.gamma_angle_label.setObjectName(QString("gamma_angle_label"))
        self.gamma_angle_label.setGeometry(QRect(400, 350, 66, 17))
        
        self.font.setBold(True)
        self.font.setItalic(True)
        self.font.setWeight(75)
        
        self.gamma_angle_label.setFont(self.font)
        self.gamma_angle_label.setAlignment(Qt.AlignCenter)
        self.gamma_angle_label.setText(QString("Gamma"))
        
        
        self.beta_angle_label.setObjectName(QString("beta_angle_label"))
        self.beta_angle_label.setGeometry(QRect(400, 200, 66, 17))
        self.beta_angle_label.setFont(self.font)
        self.beta_angle_label.setText(QString("Beta"))
        self.beta_angle_label.setAlignment(Qt.AlignCenter)
        
        self.alpha_angle_label.setObjectName(QString("alpha_angle_label"))
        self.alpha_angle_label.setGeometry(QRect(400, 60, 66, 17))
        self.alpha_angle_label.setFont(self.font)
        self.alpha_angle_label.setText(QString("Alpha"))
        self.alpha_angle_label.setAlignment(Qt.AlignCenter)
        
        self.gamma_angle_counter_2.setObjectName(QString("gamma_angle_counter_2"))
        self.gamma_angle_counter_2.setGeometry(QRect(300, 410, 271, 29))
        
        self.gamma_angle_slider_2.setObjectName(QString("gamma_angle_slider_2"))
        self.gamma_angle_slider_2.setGeometry(QRect(300, 450, 271, 21))
        
        self.gamma_angle_counter_3.setObjectName(QString("gamma_angle_counter_3"))
        self.gamma_angle_counter_3.setGeometry(QRect(580, 410, 271, 29))
        
        self.gamma_angle_slider_3.setObjectName(QString("gamma_angle_slider_3"))
        self.gamma_angle_slider_3.setGeometry(QRect(580, 450, 271, 21))
        
        self.gamma_angle_counter_4.setObjectName(QString("gamma_angle_counter_4"))
        self.gamma_angle_counter_4.setGeometry(QRect(20, 260, 271, 29))
        
        self.gamma_angle_counter_5.setObjectName(QString("gamma_angle_counter_5"))
        self.gamma_angle_counter_5.setGeometry(QRect(300, 260, 271, 29))
        
        self.gamma_angle_slider_4.setObjectName(QString("gamma_angle_slider_4"))
        self.gamma_angle_slider_4.setGeometry(QRect(300, 300, 271, 21))
        
        self.gamma_angle_counter_6.setObjectName(QString("gamma_angle_counter_6"))
        self.gamma_angle_counter_6.setGeometry(QRect(580, 260, 271, 29))
        
        self.gamma_angle_slider_5.setObjectName(QString("gamma_angle_slider_5"))
        self.gamma_angle_slider_5.setGeometry(QRect(20, 300, 271, 21))
        
        self.gamma_angle_slider_6.setObjectName(QString("gamma_angle_slider_6"))
        self.gamma_angle_slider_6.setGeometry(QRect(580, 300, 271, 21))
        
        self.gamma_angle_counter_7.setObjectName(QString("gamma_angle_counter_7"))
        self.gamma_angle_counter_7.setGeometry(QRect(20, 120, 271, 29))
        
        self.gamma_angle_counter_8.setObjectName(QString("gamma_angle_counter_8"))
        self.gamma_angle_counter_8.setGeometry(QRect(300, 120, 271, 29))
        
        self.gamma_angle_slider_7.setObjectName(QString("gamma_angle_slider_7"))
        self.gamma_angle_slider_7.setGeometry(QRect(300, 160, 271, 21))
        
        self.gamma_angle_counter_9.setObjectName(QString("gamma_angle_counter_9"))
        self.gamma_angle_counter_9.setGeometry(QRect(580, 120, 271, 29))
        
        self.gamma_angle_slider_8.setObjectName(QString("gamma_angle_slider_8"))
        self.gamma_angle_slider_8.setGeometry(QRect(20, 160, 271, 21))
        
        self.gamma_angle_slider_9.setObjectName(QString("gamma_angle_slider_9"))
        self.gamma_angle_slider_9.setGeometry(QRect(580, 160, 271, 21))
        
        self.label.setObjectName(QString("label"))
        self.label.setGeometry(QRect(120, 100, 66, 17))

        self.font1 = QFont(self)
        self.font1.setItalic(True)
        
        self.label.setFont(self.font1)
        self.label.setText(QString("Camera"))
        self.label.setAlignment(Qt.AlignCenter)

        self.label_2.setObjectName(QString("label_2"))
        self.label_2.setGeometry(QRect(400, 100, 66, 17))
        self.label_2.setFont(self.font1)
        self.label_2.setText(QString("Object"))
        self.label_2.setAlignment(Qt.AlignCenter)
        
        self.label_3.setObjectName(QString("label_3"))
        self.label_3.setGeometry(QRect(680, 100, 66, 17))
        self.label_3.setFont(self.font1)
        self.label_3.setText(QString("Slicer"))
        self.label_3.setAlignment(Qt.AlignCenter)
        
        self.label_4.setObjectName(QString("label_4"))
        self.label_4.setGeometry(QRect(680, 240, 66, 17))
        self.label_4.setFont(self.font1)
        self.label_4.setText(QString("Slicer"))
        self.label_4.setAlignment(Qt.AlignCenter)
        
        self.label_5.setObjectName(QString("label_5"))
        self.label_5.setGeometry(QRect(120, 240, 66, 17))
        self.label_5.setFont(self.font1)
        self.label_5.setText(QString("Camera"))
        self.label_5.setAlignment(Qt.AlignCenter)
        
        self.label_6.setObjectName(QString("label_6"))
        self.label_6.setGeometry(QRect(400, 240, 66, 17))
        self.label_6.setFont(self.font1)
        self.label_6.setText(QString("Object"))
        self.label_6.setAlignment(Qt.AlignCenter)
        
        self.label_7.setObjectName(QString("label_7"))
        self.label_7.setGeometry(QRect(680, 390, 66, 17))
        self.label_7.setFont(self.font1)
        self.label_7.setText(QString("Slicer"))
        self.label_7.setAlignment(Qt.AlignCenter)
        
        self.label_8.setObjectName(QString("label_8"))
        self.label_8.setGeometry(QRect(120, 390, 66, 17))
        self.label_8.setFont(self.font1)
        self.label_8.setText(QString("Camera"))
        self.label_8.setAlignment(Qt.AlignCenter)
        
        self.label_9.setObjectName(QString("label_9"))
        self.label_9.setGeometry(QRect(400, 390, 66, 17))
        self.label_9.setFont(self.font1)
        self.label_9.setText(QString("Object"))
        self.label_9.setAlignment(Qt.AlignCenter)
        
        self.line.setObjectName(QString("line"))
        self.line.setGeometry(QRect(20, 180, 831, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        self.line_2.setObjectName(QString("line_2"))
        self.line_2.setGeometry(QRect(20, 320, 831, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
    
        
    def UpdateCoords(self, object,event,actor):
        pos = str(actor.GetPosition())
        print pos
        #self._poslabel.setText(str(actor.GetPosition())
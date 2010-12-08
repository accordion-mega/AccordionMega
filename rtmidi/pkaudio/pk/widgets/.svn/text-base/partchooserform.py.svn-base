# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'partchooserform.ui'
#
# Created: Sun Jan  8 01:21:56 2006
#      by: PyQt4 UI code generator v0.4
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtGui, QtCore

class Ui_PartChooserForm(object):
    def setupUi(self, PartChooserForm):
        PartChooserForm.setObjectName("PartChooserForm")
        PartChooserForm.resize(QtCore.QSize(QtCore.QRect(0,0,251,100).size()).expandedTo(PartChooserForm.minimumSizeHint()))
        
        self.gridlayout = QtGui.QGridLayout(PartChooserForm)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        
        self.comboBox = QtGui.QComboBox(PartChooserForm)
        self.comboBox.setObjectName("comboBox")
        self.gridlayout.addWidget(self.comboBox,1,0,1,1)
        
        self.textLabel1 = QtGui.QLabel(PartChooserForm)
        self.textLabel1.setObjectName("textLabel1")
        self.gridlayout.addWidget(self.textLabel1,0,0,1,1)
        
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        
        spacerItem = QtGui.QSpacerItem(131,31,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        
        self.okButton = QtGui.QPushButton(PartChooserForm)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        
        self.cancelButton = QtGui.QPushButton(PartChooserForm)
        self.cancelButton.setObjectName("cancelButton")
        self.hboxlayout.addWidget(self.cancelButton)
        self.gridlayout.addLayout(self.hboxlayout,2,0,1,1)
        
        self.retranslateUi(PartChooserForm)

        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),PartChooserForm.accept)
        QtCore.QObject.connect(self.cancelButton,QtCore.SIGNAL("clicked()"),PartChooserForm.reject)
    
    def tr(self, string):
        return QtGui.QApplication.translate("PartChooserForm", string, None, QtGui.QApplication.UnicodeUTF8)
    
    def retranslateUi(self, PartChooserForm):
        PartChooserForm.setWindowTitle(self.tr("Part Chooser"))
        self.textLabel1.setText(self.tr("Choose a source code editor..."))
        self.okButton.setText(self.tr("OK"))
        self.cancelButton.setText(self.tr("Cancel"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Truss_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TrussStructuralDesign(object):
    def setupUi(self, TrussStructuralDesign):
        TrussStructuralDesign.setObjectName("TrussStructuralDesign")
        TrussStructuralDesign.resize(1060, 1161)
        self.verticalLayout = QtWidgets.QVBoxLayout(TrussStructuralDesign)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grp_Load = QtWidgets.QGroupBox(TrussStructuralDesign)
        self.grp_Load.setObjectName("grp_Load")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.grp_Load)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_Open = QtWidgets.QPushButton(self.grp_Load)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_Open.sizePolicy().hasHeightForWidth())
        self.btn_Open.setSizePolicy(sizePolicy)
        self.btn_Open.setObjectName("btn_Open")
        self.horizontalLayout.addWidget(self.btn_Open, 0, QtCore.Qt.AlignTop)
        self.te_Path = QtWidgets.QTextEdit(self.grp_Load)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.te_Path.sizePolicy().hasHeightForWidth())
        self.te_Path.setSizePolicy(sizePolicy)
        self.te_Path.setMinimumSize(QtCore.QSize(700, 50))
        self.te_Path.setMaximumSize(QtCore.QSize(1000, 100))
        self.te_Path.setBaseSize(QtCore.QSize(500, 0))
        self.te_Path.setObjectName("te_Path")
        self.horizontalLayout.addWidget(self.te_Path)
        self.verticalLayout.addWidget(self.grp_Load)
        self.grp_DesignReport = QtWidgets.QGroupBox(TrussStructuralDesign)
        self.grp_DesignReport.setObjectName("grp_DesignReport")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.grp_DesignReport)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.te_DesignReport = QtWidgets.QTextEdit(self.grp_DesignReport)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.te_DesignReport.sizePolicy().hasHeightForWidth())
        self.te_DesignReport.setSizePolicy(sizePolicy)
        self.te_DesignReport.setMinimumSize(QtCore.QSize(300, 300))
        self.te_DesignReport.setMaximumSize(QtCore.QSize(1000, 700))
        self.te_DesignReport.setObjectName("te_DesignReport")
        self.horizontalLayout_2.addWidget(self.te_DesignReport)
        self.grp_LongestLink = QtWidgets.QGroupBox(self.grp_DesignReport)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grp_LongestLink.sizePolicy().hasHeightForWidth())
        self.grp_LongestLink.setSizePolicy(sizePolicy)
        self.grp_LongestLink.setObjectName("grp_LongestLink")
        self.gridLayout = QtWidgets.QGridLayout(self.grp_LongestLink)
        self.gridLayout.setObjectName("gridLayout")
        self.lbl_Node1Name = QtWidgets.QLabel(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_Node1Name.sizePolicy().hasHeightForWidth())
        self.lbl_Node1Name.setSizePolicy(sizePolicy)
        self.lbl_Node1Name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_Node1Name.setObjectName("lbl_Node1Name")
        self.gridLayout.addWidget(self.lbl_Node1Name, 1, 0, 1, 1, QtCore.Qt.AlignRight)
        self.le_Node1Name = QtWidgets.QLineEdit(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_Node1Name.sizePolicy().hasHeightForWidth())
        self.le_Node1Name.setSizePolicy(sizePolicy)
        self.le_Node1Name.setMinimumSize(QtCore.QSize(50, 0))
        self.le_Node1Name.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_Node1Name.setObjectName("le_Node1Name")
        self.gridLayout.addWidget(self.le_Node1Name, 1, 1, 1, 1)
        self.lbl_LinkName = QtWidgets.QLabel(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_LinkName.sizePolicy().hasHeightForWidth())
        self.lbl_LinkName.setSizePolicy(sizePolicy)
        self.lbl_LinkName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_LinkName.setObjectName("lbl_LinkName")
        self.gridLayout.addWidget(self.lbl_LinkName, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.le_LinkLength = QtWidgets.QLineEdit(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_LinkLength.sizePolicy().hasHeightForWidth())
        self.le_LinkLength.setSizePolicy(sizePolicy)
        self.le_LinkLength.setMinimumSize(QtCore.QSize(50, 0))
        self.le_LinkLength.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_LinkLength.setObjectName("le_LinkLength")
        self.gridLayout.addWidget(self.le_LinkLength, 3, 1, 1, 1)
        self.lbl_LinkLength = QtWidgets.QLabel(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_LinkLength.sizePolicy().hasHeightForWidth())
        self.lbl_LinkLength.setSizePolicy(sizePolicy)
        self.lbl_LinkLength.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_LinkLength.setObjectName("lbl_LinkLength")
        self.gridLayout.addWidget(self.lbl_LinkLength, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        self.le_Node2Name = QtWidgets.QLineEdit(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_Node2Name.sizePolicy().hasHeightForWidth())
        self.le_Node2Name.setSizePolicy(sizePolicy)
        self.le_Node2Name.setMinimumSize(QtCore.QSize(50, 0))
        self.le_Node2Name.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_Node2Name.setObjectName("le_Node2Name")
        self.gridLayout.addWidget(self.le_Node2Name, 2, 1, 1, 1)
        self.le_LinkName = QtWidgets.QLineEdit(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_LinkName.sizePolicy().hasHeightForWidth())
        self.le_LinkName.setSizePolicy(sizePolicy)
        self.le_LinkName.setMinimumSize(QtCore.QSize(50, 0))
        self.le_LinkName.setMaximumSize(QtCore.QSize(100, 16777215))
        self.le_LinkName.setObjectName("le_LinkName")
        self.gridLayout.addWidget(self.le_LinkName, 0, 1, 1, 1)
        self.lbl_Node2Name = QtWidgets.QLabel(self.grp_LongestLink)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_Node2Name.sizePolicy().hasHeightForWidth())
        self.lbl_Node2Name.setSizePolicy(sizePolicy)
        self.lbl_Node2Name.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_Node2Name.setObjectName("lbl_Node2Name")
        self.gridLayout.addWidget(self.lbl_Node2Name, 2, 0, 1, 1, QtCore.Qt.AlignRight)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.horizontalLayout_2.addWidget(self.grp_LongestLink)
        self.verticalLayout.addWidget(self.grp_DesignReport)
        self.gv_Main = QtWidgets.QGraphicsView(TrussStructuralDesign)
        self.gv_Main.setObjectName("gv_Main")
        self.verticalLayout.addWidget(self.gv_Main)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lbl_MousePos = QtWidgets.QLabel(TrussStructuralDesign)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_MousePos.sizePolicy().hasHeightForWidth())
        self.lbl_MousePos.setSizePolicy(sizePolicy)
        self.lbl_MousePos.setMinimumSize(QtCore.QSize(500, 0))
        self.lbl_MousePos.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.lbl_MousePos.setObjectName("lbl_MousePos")
        self.horizontalLayout_3.addWidget(self.lbl_MousePos, 0, QtCore.Qt.AlignLeft)
        self.lbl_Zoom = QtWidgets.QLabel(TrussStructuralDesign)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_Zoom.sizePolicy().hasHeightForWidth())
        self.lbl_Zoom.setSizePolicy(sizePolicy)
        self.lbl_Zoom.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_Zoom.setObjectName("lbl_Zoom")
        self.horizontalLayout_3.addWidget(self.lbl_Zoom)
        self.spnd_Zoom = QtWidgets.QDoubleSpinBox(TrussStructuralDesign)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spnd_Zoom.sizePolicy().hasHeightForWidth())
        self.spnd_Zoom.setSizePolicy(sizePolicy)
        self.spnd_Zoom.setMinimum(0.25)
        self.spnd_Zoom.setMaximum(10.0)
        self.spnd_Zoom.setSingleStep(0.25)
        self.spnd_Zoom.setObjectName("spnd_Zoom")
        self.horizontalLayout_3.addWidget(self.spnd_Zoom)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(TrussStructuralDesign)
        QtCore.QMetaObject.connectSlotsByName(TrussStructuralDesign)

    def retranslateUi(self, TrussStructuralDesign):
        _translate = QtCore.QCoreApplication.translate
        TrussStructuralDesign.setWindowTitle(_translate("TrussStructuralDesign", "Form"))
        self.grp_Load.setTitle(_translate("TrussStructuralDesign", "Truss File and Load Set"))
        self.btn_Open.setText(_translate("TrussStructuralDesign", "Open and Read a Truss File"))
        self.grp_DesignReport.setTitle(_translate("TrussStructuralDesign", "Design Report"))
        self.grp_LongestLink.setTitle(_translate("TrussStructuralDesign", "LongestLink"))
        self.lbl_Node1Name.setText(_translate("TrussStructuralDesign", "Node 1 Name"))
        self.lbl_LinkName.setText(_translate("TrussStructuralDesign", "Link Name"))
        self.lbl_LinkLength.setText(_translate("TrussStructuralDesign", "Link Length"))
        self.lbl_Node2Name.setText(_translate("TrussStructuralDesign", "Node 2 Name"))
        self.lbl_MousePos.setText(_translate("TrussStructuralDesign", "TextLabel"))
        self.lbl_Zoom.setText(_translate("TrussStructuralDesign", "Zoom"))


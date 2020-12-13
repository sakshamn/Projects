# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\snayyar\Desktop\evaluate_team_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(594, 376)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBox_team = QtWidgets.QComboBox(Form)
        self.comboBox_team.setObjectName("comboBox_team")
        self.horizontalLayout_3.addWidget(self.comboBox_team)
        self.comboBox_match = QtWidgets.QComboBox(Form)
        self.comboBox_match.setObjectName("comboBox_match")
        self.horizontalLayout_3.addWidget(self.comboBox_match)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.listWidget_players = QtWidgets.QListWidget(Form)
        self.listWidget_players.setAutoScroll(True)
        self.listWidget_players.setObjectName("listWidget_players")
        self.verticalLayout.addWidget(self.listWidget_players)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lab_points = QtWidgets.QLabel(Form)
        self.lab_points.setObjectName("lab_points")
        self.horizontalLayout_2.addWidget(self.lab_points)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem2)
        self.listWidget_points = QtWidgets.QListWidget(Form)
        self.listWidget_points.setAutoScroll(True)
        self.listWidget_points.setObjectName("listWidget_points")
        self.verticalLayout_2.addWidget(self.listWidget_points)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.btn_calculate_score = QtWidgets.QPushButton(Form)
        self.btn_calculate_score.setObjectName("btn_calculate_score")
        self.verticalLayout_3.addWidget(self.btn_calculate_score)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.listWidget_players.currentRowChanged.connect(self.set_row_listWidget_points)
        self.listWidget_points.currentRowChanged.connect(self.set_row_listWidget_players)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Evaluate the Performance of your Fantasy Team"))
        self.label_2.setText(_translate("Form", "Players"))
        self.label_3.setText(_translate("Form", "Points"))
        self.lab_points.setText(_translate("Form", "##"))
        self.btn_calculate_score.setText(_translate("Form", "Calculate Score"))


    def add_team(self, team) :
        """Add a new team to the comboBox_team."""
        self.comboBox_team.addItem(team)


    def add_match(self, match) :
        """Add a new match to the comboBox_match."""
        self.comboBox_match.addItem(match)


    def set_row_listWidget_players(self) :
        """Set the row of listWidget_players to be same as the listWidget_points always.
        """
        self.listWidget_players.setCurrentRow(self.listWidget_points.currentRow())


    def set_row_listWidget_points(self) :
        """Set the row of listWidget_points to be same as the listWidget_players always.
        """
        self.listWidget_points.setCurrentRow(self.listWidget_players.currentRow())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
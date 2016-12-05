# Title        : Making the GUI 
# Developed by : Yogesh Mahajan (y.mahajan456@gmail.com)    (14D070022 @ IITB EE)
#                OV Shashank    (shashank[at]ee.iitb.ac.in) (14D070021 @ IITB EE)
#                Avineil Jain   (avineil96[at]ee.iitb.ac.in)(14D170002 @ IITB EE)   
# Description  : Generating the User Interface for Elegant Viewing

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
"""
Dependencies : 
-------------- 
    1. PyQT5   (Python interface of QT5)
    2. Pickle  (Mostly included in official python distribution)
    3. binding.py (Python 3 Script)
    
### About 60% code is autogenerated by PyUIC5 (PyQt5) from user interface file
"""

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
"""
    Class UI_Dialog:
    -----------------
        1. setupUi(--)
            * Auto generated by PyUIC5
            * Declaration and Placement of QT objects
            
        2. retranslateUi(--)
            * Assign values to QT objects if they differ from defalut values
            * Auto generated with minor tweak
            
        3. connect_handles(--)
            * connect all slots and signals
            
        4. calculate(--)
            * takes inputs from user and generate dinding output
        
        5. get_file_name(--)
            
        6. store_binding(--)
            * store result of binding 
            
        7. update_display_vals(--)
            * update UI after binding
            
        8. update_delays(--)
                       
        9. get_user_alu_coutn(--)
        
        10. generate(--)
            * genetares other output files from binding result stores in '.yo' file
        
"""
#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------

# import dependencies    
from PyQt5 import QtCore, QtGui, QtWidgets
from binding import schedule_and_bind, op_time
from generate_vhdl import generate_vhdl
import pickle
from plot_tree import *
from gen_binding_text import *
#from copy import deepcopy

#--------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------
#___________________________AUTO GENERATED CODE STARTS_____________________________________
class Ui_Dialog(object):
    #--------------------------------------------------------------------------------------------------
    # Setup UI (Auto generated)
    #--------------------------------------------------------------------------------------------------
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 520)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(600, 520))
        Dialog.setMaximumSize(QtCore.QSize(600, 520))
        Dialog.setWhatsThis("")
        Dialog.setSizeGripEnabled(True)
        self.generate_button = QtWidgets.QPushButton(Dialog)
        self.generate_button.setGeometry(QtCore.QRect(494, 200, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.generate_button.setFont(font)
        self.generate_button.setObjectName("generate_button")
        self.start_button = QtWidgets.QPushButton(Dialog)
        self.start_button.setGeometry(QtCore.QRect(390, 200, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 581, 171))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label0 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label0.setFont(font)
        self.label0.setObjectName("label0")
        self.verticalLayout.addWidget(self.label0)
        self.infix_input_text = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.infix_input_text.setFont(font)
        self.infix_input_text.setObjectName("infix_input_text")
        self.verticalLayout.addWidget(self.infix_input_text)
        self.user_alu_count_text = QtWidgets.QLineEdit(Dialog)
        self.user_alu_count_text.setGeometry(QtCore.QRect(330, 190, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.user_alu_count_text.setFont(font)
        self.user_alu_count_text.setObjectName("user_alu_count_text")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 200, 321, 16))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 290, 139, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(160, 290, 51, 121))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ALU_used_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ALU_used_label.setFont(font)
        self.ALU_used_label.setText("")
        self.ALU_used_label.setObjectName("ALU_used_label")
        self.verticalLayout_3.addWidget(self.ALU_used_label)
        self.time_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.time_label.setFont(font)
        self.time_label.setText("")
        self.time_label.setObjectName("time_label")
        self.verticalLayout_3.addWidget(self.time_label)
        self.registers_used_label = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.registers_used_label.setFont(font)
        self.registers_used_label.setText("")
        self.registers_used_label.setObjectName("registers_used_label")
        self.verticalLayout_3.addWidget(self.registers_used_label)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(220, 260, 146, 151))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_11 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_5.addWidget(self.label_11)
        self.label_12 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_5.addWidget(self.label_12)
        self.label_15 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_5.addWidget(self.label_15)
        self.label_14 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_5.addWidget(self.label_14)
        self.label_13 = QtWidgets.QLabel(self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_5.addWidget(self.label_13)
        self.comment_browser = QtWidgets.QTextBrowser(Dialog)
        self.comment_browser.setGeometry(QtCore.QRect(10, 420, 411, 91))
        self.comment_browser.setObjectName("comment_browser")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(420, 260, 128, 151))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_16 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_6.addWidget(self.label_16)
        self.label_17 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_6.addWidget(self.label_17)
        self.label_18 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.verticalLayout_6.addWidget(self.label_18)
        self.label_19 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.verticalLayout_6.addWidget(self.label_19)
        self.label_20 = QtWidgets.QLabel(self.verticalLayoutWidget_6)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.verticalLayout_6.addWidget(self.label_20)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(370, 260, 41, 151))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.mult_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.mult_delay_text.setFont(font)
        self.mult_delay_text.setObjectName("mult_delay_text")
        self.verticalLayout_4.addWidget(self.mult_delay_text)
        self.divide_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.divide_delay_text.setFont(font)
        self.divide_delay_text.setObjectName("divide_delay_text")
        self.verticalLayout_4.addWidget(self.divide_delay_text)
        self.add_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.add_delay_text.setFont(font)
        self.add_delay_text.setObjectName("add_delay_text")
        self.verticalLayout_4.addWidget(self.add_delay_text)
        self.sub_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sub_delay_text.setFont(font)
        self.sub_delay_text.setObjectName("sub_delay_text")
        self.verticalLayout_4.addWidget(self.sub_delay_text)
        self.mod_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.mod_delay_text.setFont(font)
        self.mod_delay_text.setObjectName("mod_delay_text")
        self.verticalLayout_4.addWidget(self.mod_delay_text)
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(550, 260, 41, 151))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.exp_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.exp_delay_text.setFont(font)
        self.exp_delay_text.setObjectName("exp_delay_text")
        self.verticalLayout_7.addWidget(self.exp_delay_text)
        self.and_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.and_delay_text.setFont(font)
        self.and_delay_text.setObjectName("and_delay_text")
        self.verticalLayout_7.addWidget(self.and_delay_text)
        self.or_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.or_delay_text.setFont(font)
        self.or_delay_text.setObjectName("or_delay_text")
        self.verticalLayout_7.addWidget(self.or_delay_text)
        self.xor_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.xor_delay_text.setFont(font)
        self.xor_delay_text.setObjectName("xor_delay_text")
        self.verticalLayout_7.addWidget(self.xor_delay_text)
        self.not_delay_text = QtWidgets.QLineEdit(self.verticalLayoutWidget_7)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.not_delay_text.setFont(font)
        self.not_delay_text.setObjectName("not_delay_text")
        self.verticalLayout_7.addWidget(self.not_delay_text)
        self.line_2 = QtWidgets.QFrame(Dialog)
        self.line_2.setGeometry(QtCore.QRect(0, 406, 601, 21))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(205, 260, 21, 151))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.file_name_text = QtWidgets.QLineEdit(Dialog)
        self.file_name_text.setGeometry(QtCore.QRect(430, 470, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.file_name_text.setFont(font)
        self.file_name_text.setObjectName("file_name_text")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(460, 430, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.generate_diagrams_check_box = QtWidgets.QCheckBox(Dialog)
        self.generate_diagrams_check_box.setGeometry(QtCore.QRect(280, 230, 87, 22))
        self.generate_diagrams_check_box.setObjectName("generate_diagrams_check_box")
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(210, 245, 391, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.progress_bar = QtWidgets.QProgressBar(Dialog)
        self.progress_bar.setGeometry(QtCore.QRect(40, 250, 118, 23))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    #--------------------------------------------------------------------------------------------------
    # Retranslate UI (Auto generated with minor tweaks)
    #--------------------------------------------------------------------------------------------------
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Scheduling and Binding"))
        self.generate_button.setText(_translate("Dialog", "Generate"))
        self.start_button.setText(_translate("Dialog", "Start"))
        self.label0.setText(_translate("Dialog", "Enter  Expressions Here"))
        self.infix_input_text.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Calibri\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(a+b)+(c+d)</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(a+b)^(c+d)+(!(a+b))</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">(a+b)&(c+d)|(a^b)+(c|d)</p></body></html>"))
        self.user_alu_count_text.setText(_translate("Dialog", "5"))
        self.label.setText(_translate("Dialog", "Maximum Number of ALUs can be used :"))
        self.label_2.setText(_translate("Dialog", "ALUs Used         :"))
        self.label_3.setText(_translate("Dialog", "Execution Time :")) 
        self.label_4.setText(_translate("Dialog", "Registers Used  :"))
        self.label_11.setText(_translate("Dialog", "Multiply (*)        :"))
        self.label_12.setText(_translate("Dialog", "Divide ( / )          :"))
        self.label_15.setText(_translate("Dialog", "Add (+)               :"))
        self.label_14.setText(_translate("Dialog", "Subtract ( - )       :"))
        self.label_13.setText(_translate("Dialog", "Remainder ( % ) :"))
        self.label_16.setText(_translate("Dialog", "Exponent (@) :"))
        self.label_17.setText(_translate("Dialog", "AND ( & )        :"))
        self.label_18.setText(_translate("Dialog", "OR ( | )           :"))
        self.label_19.setText(_translate("Dialog", "XOP( ^ )          :"))
        self.label_20.setText(_translate("Dialog", "NOT ( ! )         :"))
        self.mult_delay_text.setText(_translate("Dialog", "3"))
        self.divide_delay_text.setText(_translate("Dialog", "3"))
        self.add_delay_text.setText(_translate("Dialog", "2"))
        self.sub_delay_text.setText(_translate("Dialog", "2"))
        self.mod_delay_text.setText(_translate("Dialog", "3"))
        self.exp_delay_text.setText(_translate("Dialog", "4"))
        self.and_delay_text.setText(_translate("Dialog", "1"))
        self.or_delay_text.setText(_translate("Dialog", "1"))
        self.xor_delay_text.setText(_translate("Dialog", "1"))
        self.not_delay_text.setText(_translate("Dialog", "1"))
        self.label_5.setText(_translate("Dialog", "File Name"))
        self.generate_diagrams_check_box.setText(_translate("Dialog", "Diagrams"))

    #___________________________AUTO GENERATED CODE ENDS_____________________________________
    
    
    
    #--------------------------------------------------------------------------------------------------
    """
    Connect Handles
        * Connect slots and signals
        * Start button -> calculate
        * Generate button -> generate
        * Append init strings
    """
    #--------------------------------------------------------------------------------------------------
    def connect_handles(self,Dialog):    
        self.start_button.clicked.connect(self.calculate)
        self.generate_button.clicked.connect(self.generate)
        self.generate_diagrams_check_box.setChecked(True)
        self.comment_browser.append("<font color=green>Enter name for binding solution file in adjoining text box</font>")
        self.comment_browser.append("File will be saved with extension '.yo'")
        
        
        

    #--------------------------------------------------------------------------------------------------
    """
    Calculate
    
        * Genarate Scheduling and Binding Result and store in '.yo' file
        * Processes
            1. Accepting and formating of inputs from user
            2. Calling binding function
            3. Storing result in file (.yo)
    """
    #--------------------------------------------------------------------------------------------------
    def calculate(self):
        ins = self.infix_input_text.toPlainText()
        ins = ins.replace(" ","")           # remove white spaces
        infix_in = list(str.split(ins,"\n")) #remove empty lines
        #print(infix_list)
        infix_list = [inp for inp in infix_in if (inp != "")]
        self.update_delays()
        user_alu_count = self.get_user_alu_coutn()
        self.progress_bar.setValue(10)
        move_forward = False 
        try:
            self.binding = schedule_and_bind(infix_list,user_alu_count)
            self.progress_bar.setValue(50)
            self.update_display_vals(self.binding[7],self.binding[6],self.binding[8],self.binding[9])
            move_forward = True
            self.progress_bar.setValue(60)
        except:
            self.comment_browser.append("<font color=red>Something Went Worng !!!</font>")
            self.progress_bar.setValue(100)
        if move_forward :
            try:
                self.store_binding()
            except:
                self.comment_browser.append("<font color=red>Unable to Store results in file !!!</font>") 
            self.progress_bar.setValue(100)   

    #----------------------------------------------------------------------------------------------        
    """
    Get File Name from User
    * Takes the desired file name from the user
    """
    #----------------------------------------------------------------------------------------------
    def get_file_name(self):
        in_string = self.file_name_text.text()
        if (in_string == ""):
            return None
        else:
            return in_string

            
            
    #----------------------------------------------------------------------------------------------
    """
    Store Binding Result
        * Stores the binding result in the file  by the user
        * If user has not specifed file name then name 'binding' is used by default.
        * Output file is stored with extension '.yo'. Its a binary file containing python objects
        * Outfile is stored using Pickle
    """
    #----------------------------------------------------------------------------------------------
    def store_binding(self):
        self.file_name = self.get_file_name()
        #print(self.file_name)
        if(self.file_name != None):
            f = open(self.file_name + ".yo",'wb')
            pickle.dump(self.binding,f)
            self.comment_browser.append("<font color=green>Binding output is stored in '%s.yo' </font>" % self.file_name)
            f.close()
            gen_binging_text(self.file_name,self.binding)
        else:
            self.file_name = "binding"
            f = open(self.file_name + ".yo",'wb')
            pickle.dump(self.binding,f)
            f.close()
            gen_binging_text(self.file_name,self.binding)
            self.comment_browser.append("<font color=red>Invalid File Name provided !</font>")
            self.comment_browser.append("<font color=red>Binding output is stored in 'binding.yo' </font>")
    

    
    #----------------------------------------------------------------------------------
    """
    Updates the values displays(such as ALU_count etc)
    """
    #----------------------------------------------------------------------------------------------
    def update_display_vals(self,alu_count,time,reg_count,limit_count):
        self.ALU_used_label.setText(str(alu_count))
        self.time_label.setText(str(time))
        self.registers_used_label.setText(str(reg_count))
        if(limit_count > alu_count):
            self.comment_browser.append("<font color=blue>More performance</font><font color=red> MAY</font> <font color=blue>be achieved using %d ALUs</font>" % limit_count)

            
    #----------------------------------------------------------------------------------------------    
    """
    Update Delays
		* Gets the delays from the GUI, that might have been updated by the user
    """
    #----------------------------------------------------------------------------------------------
    def update_delays(self):
        op_time['*'] = int(self.mult_delay_text.text())
        op_time['+'] = int(self.add_delay_text.text())
        op_time['-'] = int(self.sub_delay_text.text())
        op_time['/'] = int(self.divide_delay_text.text())
        op_time['%'] = int(self.mod_delay_text.text())
        op_time['@'] = int(self.exp_delay_text.text())
        op_time['&'] = int(self.and_delay_text.text())
        op_time['^'] = int(self.xor_delay_text.text())
        op_time['|'] = int(self.or_delay_text.text())
        op_time['!'] = int(self.not_delay_text.text())

        
    #----------------------------------------------------------------------------------------------
    def get_user_alu_coutn(self):
        return int(self.user_alu_count_text.text())
        
        
        
    #----------------------------------------------------------------------------------------------
    """
    Generates 
    
    """
    #----------------------------------------------------------------------------------------------
    def generate(self):
        self.file_name = self.get_file_name()
        file_opened = False
        if(self.file_name == None):
            self.file_name = "binding"
            self.comment_browser.append("<font color=red> Using 'binding.yo' file as file name is not specified </font>")
        self.progress_bar.setValue(5)    
        try:
            f = open(self.file_name+".yo",'rb')
            file_opened = True
            self.progress_bar.setValue(10)
        except:
            self.comment_browser.append("<font color=red> Unable to open file '%s.yo' </font>" % self.file_name)
            self.progress_bar.setValue(100)    
        if(file_opened):
            try:
                self.binding = pickle.load(f)
                if (self.generate_diagrams_check_box.isChecked()):
                    try:
                        generate_tree_dot_file(self.binding[0],self.file_name)
                        self.progress_bar.setValue(20) 
                        generate_data_path_dot_file(self.binding[10],self.binding[11],self.binding[12],self.binding[13],self.binding[14],self.file_name)
                        self.comment_browser.append("<font color=green>DOT files generated and stored</font>")
                        self.progress_bar.setValue(30) 
                        try:
                            gen_png_from_dot_file(self.file_name)
                            self.comment_browser.append("<font color=green>Image files generated and stored</font>")
                        except:
                            self.comment_browser.append("<font color=red> Unable to generate output Images</font>") 
                    except:
                        self.comment_browser.append("<font color=red> Unable to generate output graphs</font>")
                
                self.progress_bar.setValue(50)  
                try:
                    generate_vhdl(self.file_name,self.binding)
                    self.comment_browser.append("<font color=green>VHDL Files are generated and stored</font>") 
                    self.comment_browser.append("<font color=green>They can be found in the folder: " + self.file_name +"_VHDL</font>")
                    self.comment_browser.append("<font color=blue>NOTE: The ALU and REG files contain dummy architectures. \
                    	Replace the architectures with your own ones before using the code.</font>")
                except:
                    self.comment_browser.append("<font color=red> Unable to generate VHDL scripts </font>")     
                self.comment_browser.append("<font color=green>Outputs generated using '%s.yo' </font>" % self.file_name)
            except:
                self.comment_browser.append("<font color=red> Unable to generate outputs </font>") 
            self.progress_bar.setValue(100)  


            
#--------------------------------------------------------------------------------------------------
#_______________________________________Class Ends Here____________________________________________

##------Main Program-----------------
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.connect_handles(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
##------Main Program Ends-----------------

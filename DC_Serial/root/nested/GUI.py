'''
Created on Aug 20, 2016

@author: The_Beast
'''

#http://www.tutorialspoint.com/python/python_classes_objects.htm

import sys
import logging
import serial.tools.list_ports
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer
import traceback
import ctypes

#############LOGGING#######################
logging.basicConfig(stream=sys.stderr, level=logging.INFO)     #DEBUG prints all.  Set to INFO/WARNING/ERROR or CRITICAL to disable prints.
###########################################

###########################################
#########START GUI CLASS###################
###########################################
class GUI(QWidget):                                             #GUI class inherits from QWidget
    
    def __init__(self):                                         
        super().__init__()                                      #Call constructor to parent of GUI
        self.initUI()                                           #Call initUI method
        self.serialopen = 0
        self.getinitialvalues = 0   
        self.count = 0   
        self.dataready = 0 
        self.serialready = 0
        self.validdata = 0
        self.senddata = 0
        
    def initUI(self):      
        self.picture = QLabel(self)                                         #Picture
        pixmap = QPixmap(r".\images\Test.png")  
        self.picture.setPixmap(pixmap)  
        self.picture.resize(400, 100)
        self.picture.move(0, 260)  
        self.picture.setScaledContents(True)
        
          
        self.quitbtn = QPushButton('Quit', self)                            #Quit Button
        self.quitbtn.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.quitbtn.clicked.connect(self.quitButton)
        self.quitbtn.resize(75, 22)
        self.quitbtn.move(205, 220)       
        
        self.openbtn = QPushButton('Open', self)                            #Open Button
        self.openbtn.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.openbtn.clicked.connect(self.openButton)
        self.openbtn.resize(75, 22)
        self.openbtn.move(215, 20)
        
        self.setbtn = QPushButton('Set Values', self)                            #Set Values Button
        self.setbtn.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.setbtn.clicked.connect(self.setButton)
        self.setbtn.resize(75, 22)
        self.setbtn.move(120, 220)
        
        self.portlist = QComboBox(self)                                     #Port Combo Box
        self.portlist.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.portlist.resize(100, 20)
        self.portlist.move(105,20)
        
        self.baudedit = QLineEdit(self)                                     #Baud Rate Edit
        self.baudedit.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.baudedit.setText("115200")
        self.baudedit.resize(75, 20)
        self.baudedit.move(20, 20)
        
        self.bright1 = QLineEdit(self)                                     #Brightness 1 Edit
        self.bright1.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.bright1.setText("0")
        self.bright1.resize(40, 20)
        self.bright1.move(20, 60)
        
        self.bright2 = QLineEdit(self)                                     #Brightness 2 Edit
        self.bright2.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.bright2.setText("0")
        self.bright2.resize(40, 20)
        self.bright2.move(20, 90)
        
        self.bright3 = QLineEdit(self)                                     #Brightness 3 Edit
        self.bright3.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.bright3.setText("0")
        self.bright3.resize(40, 20)
        self.bright3.move(20, 120)
        
        self.tempedit = QLineEdit(self)                                     #Temperature Edit
        self.tempedit.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.tempedit.setText("0")
        self.tempedit.resize(40, 20)
        self.tempedit.move(20, 150)
        
        self.lowbattedit = QLineEdit(self)                                  #Low Batt Edit
        self.lowbattedit.setStyleSheet("background-color:#505160; color:#FFFFFF; border-style: outset; border-width: 1px; border-color:#FFFFFF")
        self.lowbattedit.setText("0")
        self.lowbattedit.resize(40, 20)
        self.lowbattedit.move(20, 180)
        
        self.statuslabel = QLabel(self)
        self.statuslabel.setStyleSheet("color:#FFFFFF; border-style: outset")
        self.statuslabel.setText("Status: Idle")
        self.statuslabel.resize(300, 20)
        self.statuslabel.move(20, 375)
        
        self.chan1label = QLabel(self)
        self.chan1label.setStyleSheet("color:#FFFFFF; border-style: outset")
        self.chan1label.setText("Channel 1 Max Brightness (%)")
        self.chan1label.resize(200, 20)
        self.chan1label.move(80, 60)
        
        self.chan2label = QLabel(self)
        self.chan2label.setStyleSheet("color:#FFFFFF; border-style: outset")
        self.chan2label.setText("Channel 2 Max Brightness (%)")
        self.chan2label.resize(200, 20)
        self.chan2label.move(80, 90)
        
        self.chan3label = QLabel(self)
        self.chan3label.setStyleSheet("color:#FFFFFF; border-style: outset")
        self.chan3label.setText("Channel 3 Max Brightness (%)")
        self.chan3label.resize(200, 20)
        self.chan3label.move(80, 120)
        
        self.templabel = QLabel(self)
        self.templabel.setStyleSheet("color:#FFFFFF; border-style: outset")
        self.templabel.setText("Max LED Temperature (Celsius)")
        self.templabel.resize(200, 20)
        self.templabel.move(80, 150)
        
        self.battlabel = QLabel(self)
        self.battlabel.setStyleSheet("color:#FFFFFF; border-style: outset")
        self.battlabel.setText("Low Battery Warning (Volts)")
        self.battlabel.resize(200, 20)
        self.battlabel.move(80, 180)
        
        self.move(300,300)
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color:#68829E")                            #THIS SETS BG COLOR
        self.setWindowTitle('Dauntless Concepts Configuration')    
        self.show()
        
    def openButton(self):
        if self.openbtn.text() == 'Open':
            self.serialport = SerialPort(self.portlist.currentText(), self.baudedit.text())
            if self.serialport.openport():
                self.openbtn.setText('Close')
                self.statuslabel.setText("Status: Connected")
                self.serialopen = 1
        elif self.openbtn.text() == 'Close':
            if self.serialport.closeport():
                self.openbtn.setText('Open')
                myapp.statuslabel.setStyleSheet("color:#FFFFFF")
                self.statuslabel.setText("Status: Idle")
                self.serialopen = 0
                self.count = 0
                self.getinitialvalues = 0
                
    def quitButton(self):
        if self.serialport.ser.isOpen():
            self.serialport.closeport()
        exit()
        
    def setButton(self):
        if(self.serialopen==1 and self.getinitialvalues==1):
            logging.debug('Setting values.')
            self.statuslabel.setText("Status: Setting values")
            self.senddata = 1
###########################################
#########END GUI CLASS#####################
###########################################

###########################################
#########START LED CLASS###################
###########################################      
class LED: 
    def __init__(self):
        self.brightness1 = 0;
        self.brightness2 = 0;
        self.brightness3 = 0;
        self.temp = 0;
        self.lowbatt = 0;
###########################################
#########END LED CLASS#####################
###########################################   

###########################################
#########START SERIAL CLASS################
###########################################
class SerialPort: 
    def __init__(self, port, baud):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 1
        self.ser.xonoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2
        self.open = 0
        
    def openport(self):                 #Open selected port
        logging.debug("Opening {} at {}.".format(self.ser.port, self.ser.baudrate))
        
        try: 
            self.ser.open()
            self.open = 1
            logging.debug("Port open.")
            return 1
        except Exception:
            logging.debug(traceback.format_exc())
            return 0
            exit()
        
    def closeport(self):                #Close selected port
        if self.ser.isOpen():
            self.ser.close()
            self.open = 0
            logging.debug("Port closed.")
            return 1
        else:
            return 0
        
    def send(self, command):
        if self.ser.isOpen():
            self.ser.write(command)
###########################################
#########END SERIAL CLASS##################
###########################################
        
###FUNCTION TO LIST ALL AVAILABLE SERIAL PORTS###    
def serial_ports(dc_gui):
    ports = list(serial.tools.list_ports.comports())
    ports.sort();
    for p in ports:
        logging.debug(p)
        dc_gui.portlist.addItem(p.device)
#################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r".\images\Icon.png"))           #Sets window and taskbar icon
    myappid = 'dc.dc.dc.dc' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    myapp = GUI()
    myLED = LED()
    serial_ports(myapp)
    
    def tick():   
        if(myapp.serialopen==1 and myapp.getinitialvalues==0):
            myapp.statuslabel.setStyleSheet("color:#FFFFFF")
            myapp.statuslabel.setText("Status: Getting Current Values")
            myapp.count+=1
            
            if(myapp.count==15):
                myapp.serialport.send('SOFTVALUES\n'.encode('utf-8'))
            elif(myapp.count==16):
                data = myapp.serialport.ser.read(myapp.serialport.ser.in_waiting)
                logging.debug(data)
                if(len(data)!=23):
                    myapp.validdata = 0
                else:
                    myapp.validdata = 1
                    data = data.decode('utf-8')
                    values = data.split("\r\n")
                    logging.debug(values[0])
                    myapp.bright1.setText(values[0])
                    logging.debug(values[1])
                    myapp.bright2.setText(values[1])
                    logging.debug(values[2])
                    myapp.bright3.setText(values[2])
                    logging.debug(values[3])
                    myapp.tempedit.setText(values[3])
                    logging.debug(values[4])
                    myapp.lowbattedit.setText(values[4])
                    myapp.getinitialvalues=1
                    myapp.count+=1
        elif(myapp.count>=17 and myapp.senddata==0):
            if(myapp.validdata==1):
                myapp.statuslabel.setStyleSheet("color:#00FF00")
                myapp.statuslabel.setText("Status: Connected")
            else:
                myapp.statuslabel.setStyleSheet("color:#FF0000")
                myapp.statuslabel.setText("Status: Connected to Unknown Device")
                    
            if(myapp.serialport.ser.in_waiting>0):
                data = myapp.serialport.ser.read(myapp.serialport.ser.in_waiting)
                logging.debug(data)
                
        if(myapp.serialopen==1 and myapp.senddata>0):
            if(myapp.senddata==1):
                myapp.statuslabel.setStyleSheet("color:#FFFFFF")
                myapp.statuslabel.setText("Status: Setting Channel 1 Brightness")
                myapp.serialport.send(b"BRIGHTNESS1_"+myapp.bright1.text().encode('utf-8')+b"\n")
                myapp.senddata+=1
            elif(myapp.senddata==2):
                if(myapp.serialport.ser.in_waiting>0):
                    data = myapp.serialport.ser.read(myapp.serialport.ser.in_waiting)
                    logging.debug(data)
                    if(b'Setting' in data):
                        myapp.statuslabel.setStyleSheet("color:#00FF00")
                        myapp.statuslabel.setText("Status: Successful")
                    elif(b'Invalid' in data):
                        myapp.statuslabel.setStyleSheet("color:#FF0000")
                        myapp.statuslabel.setText("Status: Failed")
                    myapp.senddata+=1
            elif(myapp.senddata==3):   
                myapp.statuslabel.setStyleSheet("color:#FFFFFF")
                myapp.statuslabel.setText("Status: Setting Channel 2 Brightness")     
                myapp.serialport.send(b"BRIGHTNESS2_"+myapp.bright2.text().encode('utf-8')+b"\n")
                myapp.senddata+=1
            elif(myapp.senddata==4):
                if(myapp.serialport.ser.in_waiting>0):
                    data = myapp.serialport.ser.read(myapp.serialport.ser.in_waiting)
                    logging.debug(data)
                    if(b'Setting' in data):
                        myapp.statuslabel.setStyleSheet("color:#00FF00")
                        myapp.statuslabel.setText("Status: Successful")
                    elif(b'Invalid' in data):
                        myapp.statuslabel.setStyleSheet("color:#FF0000")
                        myapp.statuslabel.setText("Status: Failed")
                    myapp.senddata+=1
            elif(myapp.senddata==5):  
                myapp.statuslabel.setStyleSheet("color:#FFFFFF")
                myapp.statuslabel.setText("Status: Setting Channel 3 Brightness") 
                myapp.serialport.send(b"BRIGHTNESS3_"+myapp.bright3.text().encode('utf-8')+b"\n")
                myapp.senddata+=1
            elif(myapp.senddata==6):
                if(myapp.serialport.ser.in_waiting>0):
                    data = myapp.serialport.ser.read(myapp.serialport.ser.in_waiting)
                    logging.debug(data)
                    if(b'Setting' in data):
                        myapp.statuslabel.setStyleSheet("color:#00FF00")
                        myapp.statuslabel.setText("Status: Successful")
                    elif(b'Invalid' in data):
                        myapp.statuslabel.setStyleSheet("color:#FF0000")
                        myapp.statuslabel.setText("Status: Failed")
                    myapp.senddata+=1
            elif(myapp.senddata==7):
                myapp.statuslabel.setStyleSheet("color:#FFFFFF")
                myapp.statuslabel.setText("Status: Setting Max LED Temperature")
                myapp.serialport.send(b"TEMP_"+myapp.tempedit.text().encode('utf-8')+b"\n")  
                myapp.senddata+=1
            elif(myapp.senddata==8):
                if(myapp.serialport.ser.in_waiting>0):
                    data = myapp.serialport.ser.read(myapp.serialport.ser.in_waiting)
                    logging.debug(data)
                    if(b'Setting' in data):
                        myapp.statuslabel.setStyleSheet("color:#00FF00")
                        myapp.statuslabel.setText("Status: Successful")
                    elif(b'Invalid' in data):
                        myapp.statuslabel.setStyleSheet("color:#FF0000")
                        myapp.statuslabel.setText("Status: Failed")
                    myapp.senddata+=1
            elif(myapp.senddata==9):
                myapp.statuslabel.setStyleSheet("color:#FFFFFF")
                myapp.statuslabel.setText("Status: Setting Min Battery Voltage")
                myapp.serialport.send(b"LOWBATT_"+myapp.lowbattedit.text().encode('utf-8')+b"\n")
                myapp.senddata+=1  
            elif(myapp.senddata==10):
                if(myapp.serialport.ser.in_waiting>0):
                    data = myapp.serialport.ser.read(myapp.serialport.ser.in_waiting)
                    logging.debug(data)
                    if(b'Setting' in data):
                        myapp.statuslabel.setStyleSheet("color:#00FF00")
                        myapp.statuslabel.setText("Status: Successful")
                    elif(b'Invalid' in data):
                        myapp.statuslabel.setStyleSheet("color:#FF0000")
                        myapp.statuslabel.setText("Status: Failed")
                    myapp.senddata=0    
                         

    timer = QTimer()
    timer.timeout.connect(tick)
    timer.start(100)
    
    sys.exit(app.exec_())       

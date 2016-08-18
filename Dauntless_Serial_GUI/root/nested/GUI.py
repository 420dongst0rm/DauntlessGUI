'''
Created on Aug 16, 2016

@author: The_Beast
'''

#http://zetcode.com/gui/pyqt5/firstprograms/
#http://stackoverflow.com/questions/16000361/accessing-gui-elements-from-outside-the-gui-class
#https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/

import sys
import glob
import serial
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QListWidget, QComboBox, QLineEdit
from PyQt5.QtCore import QCoreApplication


class GUI(QWidget):                                             #GUI class inherits from QWidget
    
    def __init__(self):                                         
        super().__init__()                                      #Call constructor to parent of GUI
        
        self.initUI()                                           #Call initUI method
        
        
    def initUI(self):               
        
        self.quitbtn = QPushButton('Quit', self)                            #Quit Button
        self.quitbtn.clicked.connect(self.exitprogram)
        self.quitbtn.resize(75, 20)
        self.quitbtn.move(150, 250)       
        
        self.openbtn = QPushButton('Open', self)                            #Quit Button
        self.openbtn.clicked.connect(self.setupport)
        self.openbtn.resize(75, 22)
        self.openbtn.move(240, 20)
        
        self.portlist = QComboBox(self)                                     #Port Combo Box
        self.portlist.resize(100, 20)
        self.portlist.move(130,20)
        
        self.baudedit = QLineEdit(self)                                     #Baud Rate Edit
        self.baudedit.setText("9600")
        self.baudedit.resize(100, 20)
        self.baudedit.move(20, 20)
        
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Dauntless Concepts Configuration')    
        self.show()
        
    def exitprogram(self):                                                  #Exit
        if self.ser.isOpen():
            self.ser.close()
            print("Port closed.")
        exit()
        
    def setupport(self):                #Set port up
        if self.openbtn.text() == 'Open':
            self.ser = serial.Serial()
            self.ser.port = self.portlist.currentText()
            self.ser.baudrate = int(self.baudedit.text())
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = 1
            self.ser.xonoff = False
            self.ser.rtscts = False
            self.ser.dsrdtr = False
            self.ser.writeTimeout = 2
            self.openport()
        elif self.openbtn.text() == 'Close':
            self.closeport()
            
    def closeport(self):                #Close selected port
        if self.ser.isOpen():
            self.ser.close()
            self.openbtn.setText('Open')
            print("Port closed.")
        
    def openport(self):                 #Open selected port
        print("Opening {} at {}.".format(self.ser.port, self.ser.baudrate))
        
        try: 
            self.ser.open()
            self.openbtn.setText('Close')
        except Exception:
            print("Error opening serial port.")
            exit()
            
        print("Port open.")
        
def serial_ports(qtWnd):
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(8)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
            qtWnd.portlist.addItem(port)
        except (OSError, serial.SerialException):
            pass
    return result
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = GUI()
    print(serial_ports(myapp))
    sys.exit(app.exec_())
    
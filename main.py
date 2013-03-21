#-*- coding = UTF-8 -*-

__author__ = "qlzhang"
__email__ = "qlzhangtju@gmail.com"
__version__ = "0.1"

"""
used in python27

This is a simple project for convert
data from a microController with hex
type to a format available for Serial Chart

Receive from a comm , convert the data,and then
send it to the other comm which is connected to
the Serial Chart
"""

from Convert import *
from Comm import *
import time
from Tkinter import *
import threading

class WinApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.bind('<Destroy>',self.__onDestory)
        self.startBtn = Button(self,text = "START",command = self.__startFn)
        self.startBtn.pack()
        self.stopBtn = Button(self,text = "STOP",command = self.__stopFn)
        self.stopBtn.pack()
        self.__createWidget()
        self.t = threading.Thread(target = self.__running)
        self.__stop = False
        self.__terminate = False
        self.t.start()

    def __onDestory(self,evnet):
        self.inComm.terminate()
        self.outComm.terminate()
        self.__terminate = True

    def __createWidget(self):
        self.inComm = Comm("COM4",57600)
        self.outComm = Comm("COM5",57600)
        self.inComm.start()
        self.outComm.start()
        self.conv = Convert(23,1.21,0)

    def __startFn(self):
        ret,msg = self.inComm.open()
        ret,msg = self.outComm.open()
        self.__stop = False
        
    def __stopFn(self):
        self.__stop = True
        time.sleep(0.5)
        self.inComm.close()
        self.outComm.close()
        

    def __running(self):
        while not self.__terminate:
            if self.__stop:
                continue
            
            ret,data = self.inComm.recv(3)
            if not ret:
                continue
            ret,data = self.conv.conv(data)
            if not ret:
                continue
            
            self.outComm.send((str(data)+'\n').encode('utf8'))


if __name__ == "__main__":
    app = WinApp()
    app.mainloop()

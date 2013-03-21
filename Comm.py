#-*- coding = UTF-8 -*-


import threading
import time
from serial import *

class Comm(threading.Thread):
    def __init__(self,port = "COM1",baund = 9600):
        threading.Thread.__init__(self)
        self.__stop = False
        self.ser = Serial(port,baund)
        if self.ser.isOpen():
            self.ser.close()

    def open(self):
        try:
            if not self.ser.isOpen():
                self.ser.open()
            self.ser.flushInput()
            self.ser.flushOutput()
        except Exception,msg:
            return False,msg.message.decode("gbk")

        return True,"Open Comm Success"

    def terminate(self):
        self.__stop = True

    def send(self,data):
        if self.__stop or not self.ser.isOpen():
            return False,"Comm is Stoped"
        
        self.ser.write(data)
        return True,"Send Ok"

    def recv(self,n = 1):
        if self.__stop or not self.ser.isOpen():
            return False,0

        if self.ser.inWaiting() < n:
            return False,0
        
        data = self.ser.read(n)
        return True,data

    def close(self):
        if self.ser.isOpen():
            self.ser.close()

    def run(self):
        while not self.__stop:
            time.sleep(1)
            pass
        
        self.close()


#-*- coding = UTF-8 -*-




class Convert():
    def __init__(self,bits = 8,posV = 1,negV = 0):
        self.bits = bits
        self.negV = negV
        self.posV = posV
        self.delta = (posV - negV)/((1 << bits)-1)

    def conv(self,data):
        val = 0
        for v in data:
            val = (val << 8) + ord(v)
        if val > 8388607:
            val = val - 16777216
        
        val = self.delta * val
        #print 'conv val : ',val
        return True,val

    def setFormat(self,bits = 8,posV = 1,negV = 0):
        self.bits = bits
        self.negV = negV
        self.posV = posV
        self.delta = (posV - negV)/((1 << bits)-1)

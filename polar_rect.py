import math

class Polar:
    def __init__(self, mag, ang):
        self.mag = mag
        self.ang = ang
    
    def __mul__(self, b):
        return Polar(self.mag*b.mag,self.ang+b.ang)

    def __truediv__(self, b):
        return Polar(self.mag/b.mag,self.ang-b.ang)

    def __add__(self, b):
        x = self.mag*math.cos(self.ang*math.pi/180)+b.mag*math.cos(b.ang*math.pi/180)
        y = self.mag*math.sin(self.ang*math.pi/180)+b.mag*math.sin(b.ang*math.pi/180)
        return Polar(math.sqrt(x**2+y**2),math.atan(y/x)*180/math.pi)
 
    def __sub__(self, b):
        x = self.mag*math.cos(self.ang*math.pi/180)-b.mag*math.cos(b.ang*math.pi/180)
        y = self.mag*math.sin(self.ang*math.pi/180)-b.mag*math.sin(b.ang*math.pi/180)
        return Polar(math.sqrt(x**2+y**2),math.atan(y/x)*180/math.pi)

    def getRect(self):
        return complex(self.mag*math.cos(self.ang*math.pi/180),self.mag*math.sin(self.ang*math.pi/180))

    def convertPolar(self, b): 
        x = b.real
        y = b.imag
        self.mag = math.sqrt(x**2+y**2)
        self.ang = math.atan(y/x)*180/math.pi

    def getVal(self):
        return [self.mag,self.ang]


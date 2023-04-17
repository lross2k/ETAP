# Matemática usada para muchos cálculos simples que no son soportados por defecto en math de
# stdlib o similares, numpy no se usa por detalles de compatibilidad aunque sería
# preferible

from math import sqrt, pi, cos, sin, atan, acos

# Declaración de funciones
cosd    = lambda x: cos(x*pi/180)
sind    = lambda x: sin(x*pi/180)
arctand = lambda x: atan(x)*180/pi
arccosd = lambda x: acos(x)*180/pi
pithag  = lambda x,y: sqrt(x**2 + y**2)
def polar(x):
    if x.real != 0:
        return Polar(sqrt(x.real**2+x.imag**2), arctand(x.imag/x.real))
    else:
        return Polar(x.imag,90*(1-2*(x.imag<0)))

# Declaración de clase polar
class Polar:
    def __init__(self,mag,ang):
        self.mag = mag
        self.ang = ang
    def __mul__(self, other):
        return Polar(self.mag * other.mag,self.ang + other.ang)
    def __truediv__(self, other):
        return Polar(self.mag / other.mag,self.ang - other.ang)
    def __add__(self, other):
        op = self.rect() + other.rect()
        r = Polar(sqrt(op.real**2+op.imag**2),arctand(op.imag/op.real))
        return r
    def __sub__(self, other):
        op = self.rect() - other.rect()
        r = Polar(sqrt(op.real**2+op.imag**2),arctand(op.imag/op.real))
        return r
    def __repr__(self):
        return "%.3f ∠ %.3f"%(self.mag,self.ang)
    def __sts__(self):
        return "%.3f ∠ %.3f"%(self.mag,self.ang)
    def rect(self):
        return complex(self.mag*cos(self.ang*pi/180),self.mag*sin(self.ang*pi/180))


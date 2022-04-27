# Este archivo espera proveer de clases y funciones que permitan facilitar el modelado y solución
# de problemas que involucren máquinas eléctricas, de momento sólo soporta las siguientes:
# niguna 🍆🍆🍆

# Importar el módulo de matemática custom que uso 🍆🍆🍆
from mymath import *

class maquina_sincrona:
    esY = False
    esD = False
    VL = 0
    FP = 0
    XS = 0
    RA = 0
    PM = 0
    Motor = False
    ARed = False
    ASol = False
    Atraso = False
    Adelanto = False
    # Constructor
    def __init__(self,esY,VL,FP,XS,RA,PM=0,S=0,Motor=False,ARed=False,ASol=False,Atraso=False):
        self.esY = esY      # Binario estrella
        self.esD = not esY  # Binario delta
        self.VL = VL        # Voltaje de terminal
        self.FP = FP        # Factor de potencia
        self.XS = XS        # Reactancia
        self.RA = RA        # Resistencia
        if PM != 0:
            self.PM = PM        # Potencia mecanica
        else:
            self.PM = S*FP     # Potencia mecanica de aparente
        # Determinar si es motor o alternador red/aislado
        if Motor:
            self.Motor = True
        elif ARed:
            self.ARed = True
        else:
            self.ASol = True
        if Atraso:
            self.Atraso = True
        else:
            self.Adelanto = True
    def __repr__(self):
        return self.XS
    # Metodo para resolver params dados
    def resolver(self,PM=0):
        # Resolucion en caso de aislado
        if self.Motor:
            print("Aún no implemento los motores")
        else:
            ang_FP = arccosd(self.FP)*self.Atraso-arccosd(self.FP)*(not self.Atraso)
            ang_IA = -ang_FP
            self.ang_IA = ang_IA
            # Convertir VL a Vf
            Vf = complex(self.VL/sqrt(3),0)
            polar_Vf = polar(Vf)
            self.polar_Vf = polar_Vf
            # de la potencia trifasica se despeja
            IA = self.PM/(sqrt(3)*self.VL*self.FP)
            IA = complex(IA*cosd(ang_IA),IA*sind(ang_IA))
            polar_IA = polar(IA)
            polar_IA.ang = ang_IA
            self.polar_IA = polar_IA
            # Se calcula EA
            EA = Vf + IA*self.RA + IA*self.XS
            polar_EA = polar(EA)
            self.polar_EA = polar_EA
            # se pasa a polar Se calcula el IA * XS
            polar_IAXS = polar(IA*self.XS)
            self.polar_IAXS = polar_IAXS
            # Se calcula el IA * RA
            polar_IARA = polar(IA*self.RA)
            self.polar_IARA = polar_IARA
    def inc_ia_ais(self,porcentaje,reg=True,constEA=True,constVf=False):
        # Por defecto asume regulacion de velocidad -> frec const, Ea dep If
        # Incrementar magnitud de IA segun esperado (por aumento de potencia)
        self.polar_IA.mag *= 1+(porcentaje/100)
        self.polar_IARA = Polar(self.RA,0) * self.polar_IA
        self.polar_IAXS = polar(self.XS) * self.polar_IA

        IAZ = pithag(self.polar_IARA.mag,self.polar_IAXS.mag)
        
        # Intentando iterar valores que cumplan todo
        EA = self.polar_EA
        Vf = self.polar_EA - self.polar_IARA - self.polar_IAXS
        while (Vf.ang > 0.1 and Vf.ang >= 0) or (Vf.ang < 0.1 and Vf.ang <= 0):
            EA.ang += 0.1
            Vf = EA - self.polar_IARA - self.polar_IAXS
        self.polar_Vf = Vf
        self.polar_EA = EA

    def imprimir(self):
        print(" ")
        if self.Atraso and self.FP != 1:
            print("En atraso")
        elif not self.Atraso and self.FP != 1:
            print("En adelanto")
        else:
            print("Unitario")
        print("Vf: "+str(self.polar_Vf)+" V")
        print("EA: "+str(self.polar_EA)+" V")
        print("IA: "+str(self.polar_IA)+" A")
        print("IA*RA: "+str(self.polar_IARA)+" V")
        print("IA*XS: "+str(self.polar_IAXS)+" V")













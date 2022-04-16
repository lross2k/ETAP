# nombres snake_case, paradigma funcional 'pythonesco', sin declarar variables

# Importacion de modulos
from csv import reader
from math import log10 as log
import matplotlib.pyplot as plt
import numpy as np

# Funcion para acortar abrir csv de archivo
aa = lambda nm: reader(open(nm+'.csv','r'))

# Funcion que retorna el caudal dado un diametro
q = lambda d: [float(i[1]) for i in aa('dc') if i[0]!='D' and float(i[0])>=d][0]

# Funcion que retorna velocidad dado un caudal
v = lambda q: [float(i[2]) for i in aa('dc') if i[0]!='D' and float(i[1])==q][0]

# Funcion que retorna numero de Reynolds
re = lambda v,d: v*d*1e-3*997/0.000891

# Funcion que retorna la friccion por Pavlov
ft = lambda d,re: (-2*log(1/3.7*(0.15/d)+(6.81/re)**0.9))**-2

# Funcion que retorna la longitud equivalente
le = lambda d,k: d/k

# Funciones que retornan el h
h = lambda ft,v,l,d: ft*(l/(d*1e-3))*(v**2/(2*9.81))
hk = lambda v,k: k*(v**2/(2*9.81))

# Funcion con calculos y generacion de h para union T
def en_t(di,c=0,ve=None):
    return hk(ve,(c*60+(1!=c)*80)*ft(di,re(ve,di))) if ve else en_t(di,c,v(q(di))) 
    
# Funcion con calculos y generacion de h para valvula de globo
globo = lambda di,ve=None: globo(di,v(q(di))) if not ve else hk(ve,340*ft(di,re(ve,di)))

# Funcion con calculos y generacion de h para segmento de tubo
tubo = lambda di,le,ve=None: tubo(di,le,v(q(di))) if not ve else h(ft(di,re(ve,di)),ve,le,di)

# Funcion con calculos y generacion de h para codo
codo = lambda di,ve=None: codo(di,v(q(di))) if not ve else hk(ve,20*ft(di,re(ve,di)))

# Funcion para obtener h del regulador
reg = lambda di,ve=None: reg(di,v(q(di))) if not ve else 4*hk(ve,340*ft(di,re(ve,di)))

# Funcion que calcula la potencia de una bomba segun du eficiencia y datos
pot = lambda q,ha,eff=0.76: ha*997*9.81*q*1e-3/eff

# Funcion que calcula las perdidas de un piso dado, sea intermedio o el final (con codo)
piso = lambda di,dp,u=0: reg(dp)+tubo(di-dp,4)+codo(di) if u else en_t(di)+reg(dp)+tubo(di-dp,4)

# Funcion que retorna el hA luego de pasarle los datos de la ecuacion de energia
energia = lambda z1,z2,hl,v2: hl + z2 - z1 + v2**2/(2*9.81)

# Funcion que calculca las perdidas para una torre de cierta cantidad de pisos dada
def torre(pisos,dp,di,h=0,up=1):
    return h+(torre(pisos,dp,di-dp*(up!=1),piso(di,dp),(up+1)) if up<pisos else piso(di,dp,1))

# Se calculan los valores para el problema dado (pisos, diam, altura piso)
def calc(pi,di,zp,h=0):
    if not h:
        return (calc(pi,di,zp,energia(6,zp*pi,torre(pi,di/pi,di)+tubo(di,16.8)+codo(di)+
            globo(di)+codo(di)+en_t(di,1)+codo(di),v(q(di-(pi-1)*di/pi)))))
    else:
        return ([h,pot(q(di),h/1000),q(di)])

# Funcion que grafica datos de 
def graficar(edificios,resultados):
    plt.plot([i[0] for i in edificios],[i[1] for i in resultados])
    plt.title('Potencia vs Pisos')
    plt.xlabel('Pisos del edificio')
    plt.ylabel('Potencia de la bomba')
    plt.show()

# Funcion con la llamada de procesos principales
def main(edificios,grafica=0,val=[]):
    if not grafica:
        for edf in edificios:
            val.append(calc(edf[0],edf[1],edf[2]))
        main(edificios,grafica=1)
    else:
        for i in range(len(edificios)):
            print("\nVariables ingresadas:")
            print("| Edificio de %i pisos"%(edificios[i][0]))
            print("| Altura entre pisos %.2f m"%(edificios[i][2]))
            print("| Diametro de %.2f mm"%(edificios[i][1]))
            print("Carga agregada por bomba %.4f m"%(val[i][0]))
            print("Potencia de %.4f kW"%(val[i][1]))
            print("Caudal de %.4f m^3/s"%(val[i][2]))
        if grafica and len(edificios)>1:
            graficar(edificios,val)

# Llamada a funcion main para Python
main([[2,60,5],[3,60,5],[4,100,5],[5,100,5],[6,100,5],[7,100,5],[8,100,5],[9,100,5],[10,100,5]])
#main([[5,100,4]])


from maquinas import *

# Sintaxis deseada
# Instanciar maquina
maquina1 = maquina_sincrona(True,
                            13.8e3,
                            0.9,
                            complex(0,2.5),
                            0.2,
                            S=25e6,
                            ASol=True,
                            Atraso=True)
# Solicitar que se resuleva
maquina1.resolver()
# Imprimir valores resueltos
maquina1.imprimir()
# Incrementar corriente por un porcentaje
maquina1.inc_ia_ais(10)

maquina1.imprimir()


# tentacion de scrapping https://www.enteoperador.org:7778/ords/f?p=102:1:2423742479116:::::
import matplotlib.pyplot as plt
import http.client as httplib
import requests
import csv
import re

DATOS_POR_PAIS = 0
DATOS_REGION = 1

tipo_de_grafico = 0 # Por defecto grafica para cada país
regex_fecha = re.compile(r"\d\d-\d\d-\d\d\d\d \d\d:\d\d [ap]m")
regex_ssid = re.compile(r"=\w*\b")
regex_ora = re.compile(r"ORA_WWV-\S{24}")

host = "www.enteoperador.org:7778"
url1 = "/ords/f?p=102:1"
url2 = "/ords/f?p=101:1"
headers = {
    'Host': 'www.enteoperador.org:7778',
    'Accept': '*/*',
}

conn = httplib.HTTPSConnection(host)
conn.request("GET", url1, "", headers)
r102 = conn.getresponse()
if r102.status != 302:
    print("No tengo idea de qué salió mal con el 302")
    conn.close()
    exit()

conn.request("GET", url2, "", headers)
r101 = conn.getresponse()
if r101.status != 302:
    print("No tengo idea de qué salió mal con el 302")
    conn.close()
    exit()

cookies_ora = [regex_ora.search(r101.getheaders()[8][1])[0],regex_ora.search(r102.getheaders()[8][1])[0]]
series = None
ssid=regex_ssid.search(requests.get("https://www.enteoperador.org/inicio-2/curva-de-demanda-por-paises/").headers['set-cookie'])[0].replace('=','')
url = "https://www.enteoperador.org:7778/ords/wwv_flow.ajax"
headers = {
    'Host': 'www.enteoperador.org:7778',
    #'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept': '*/*',
    'Origin': 'https://www.enteoperador.org:7778',
    'Cookie': 'ORA_WWV_APP_102='+cookies_ora[0]+'; '+ 'ORA_WWV_APP_101='+cookies_ora[1]+'; '+'PHPSESSID='+ssid,
}
data = ["p_flow_id=102&p_flow_step_id=1&p_instance=2423742479116&p_request=PLUGIN%3D7x0WsT-JayVjLOVSSJzeAV7NMB9htnIGVopMx_DC7po",
        "p_flow_id=101&p_flow_step_id=1&p_instance=4520926339291&p_request=PLUGIN%3DjlLF5rAZ9Oahk1vfrJHI2dBiaLNzzthP-05kQMhjRbo"]

# PROBAAAANDOOOOOOOOOOO
url3 = "/ords/wwv_flow.ajax"
conn = httplib.HTTPSConnection(host)
conn.request("POST", url3, data[0], headers)
rfinal = conn.getresponse()
print(headers)
print(rfinal.status)
print(rfinal.reason)

def obtener_series():
    global series
    r = requests.post(url, headers=headers, data=data[tipo_de_grafico]
)
    if r.status_code != 200:
        print("No se pudo contactar al servicio web")
        exit()
    series = r.json()['series']

# Función que grafica todas las curvas de demanda en un sólo plano
def graficar(archivo="combinada.png", modo=0):
    valores_plot = []
    for serie in series:
        valores = []
        for item in serie['items']:
            # Se toman todos los valores de cada país
            valores.append(item['value'])
        valores_plot.append(valores[:])

    for grafica in valores_plot:
        # Se agregan todos los plots en uno sólo
        plt.plot(grafica)
    if modo == 0:
        plt.show()
    elif modo == 1:
        plt.savefig(archivo)
    plt.clf()

# Función que retorna las listas con los mismo datos que se 
# usan para llenar el CSV
def obtener_datos():
    # Se llena la fila superior con fechas y horas
    fila_superior = ['']
    for item in series[0]['items']:
        fila_superior.append(regex_fecha.search(item['shortDesc'])[0])
    otras_filas = []
    # Se llenan las siguientes filas con el consumo de cada país
    for pais in series:
        siguiente_fila = [pais['name']]
        for item in pais['items']:
            siguiente_fila.append(item['value'])
        otras_filas.append(siguiente_fila[:])
    return(fila_superior, otras_filas)

# Función que se encarga de escribir los datos a un CSV con el 
# siguiente formato

#    FechaInicio . . . FechaFinal
# 1  x           . . . x
# 2  x           . . . x
# .
# .
# .
# N  x           . . . x
def escribir_csv(archivo="datos.csv"):
    # Se ordenan los datos
    [fila_superior, otras_filas] = obtener_datos()

    # Sólo se escribe hasta el final para reducir al mínimo 
    # el uso de comunicación externa del SO
    with open(archivo, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        # Se escriben los valores de todas las columnas en el CSV
        csvwriter.writerow(fila_superior) 
        for fila in otras_filas:
            csvwriter.writerow(fila)

# Se usa para cambiar entre gráfica de region o por país
def elegir_modo(modo=0):
    global tipo_de_grafico
    tipo_de_grafico = modo
    obtener_series()
   
""" -------------- """
""" EJEMPLO DE USO """

# Este es el modo activo por defecto
elegir_modo(DATOS_POR_PAIS)

# Se guardan los datos en un csv
#escribir_csv("datos_pais_24_mar.csv")

# Se muestra una gráfica simple
graficar()
# Se guarda la gráfica en un archivo
#graficar("pais_22.png", modo=1)

# Se cambia al modo de región
#elegir_modo(DATOS_REGION)

# Guardar en otro csv
#escribir_csv("datos_pais_24_mar.csv")
#graficar("region_22.png", modo=1)

# Mostrar gráfica de región
#graficar()

""" EJEMPLO DE USO """
""" -------------- """

conn.close()
  
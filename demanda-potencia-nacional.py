import requests
import json
import pandas as pd
import numpy as np

# Obtiene datos en JSON mediante GET y retorna diccionario con datos ordenados por fecha
def ObtenerDemandaDiaria(inicio, fin, verbose=0):
    print("Waiting for API response...")
    # Enviar solicitud por metodo GET
    response = requests.get('https://apps.grupoice.com/CenceWeb/data/sen/json/DemandaMW', params={'inicio': inicio, 'fin': fin})
    # Si el metodo GET es recibido correctament
    if (response.status_code == 200):
        body = response.content.decode('utf-8')
        data = json.loads(body)
        # Muestra descripcion del GET de solicitar ser verbose
        if verbose:
            print(data['descripcion'])
        data = data['data'] # Extraer data del dicionario
        # Generar diccionario con las fechas como llave y valor de diccionario con los valores
        temp_dict = {}
        for entry in data:
            temp_dict[entry['fechaHora']] = dict([('MW',entry['MW']),('MW_P',entry['MW_P'])])
        data = {}
        # Ordenar el diccionario final por orden de fechas (llaves)
        for key in sorted(temp_dict.keys()):
            data[key] = temp_dict[key]
        #data = sorted(temp_dict)
        return data
    # Si la URL no retorna una solicitud exitosa
    else:
        print("HTTP error: ",response.status_code)
        exit()

def build_df(dic):
    print("sorting data...")
    frame = {'Fecha':[],'Hora':[],'Potencia':[]}
    for key in dic.keys():
        timestamp = pd.Timestamp(key)
        frame['Fecha'].append(str(timestamp.day)+'-'+str(timestamp.month)+'-'+str(timestamp.year))
        hora = str(timestamp.hour) if timestamp.hour>9 else '0'+str(timestamp.hour)
        minuto = str(timestamp.minute) if timestamp.minute>9 else '0'+str(timestamp.minute)
        frame['Hora'].append(hora+':'+minuto)
        frame['Potencia'].append(dic[key]['MW'])
    return pd.DataFrame(frame)

def main():
    inicio  = input("inicio  $ ") #20190101
    fin     = input("final   $ ") #20190102
    nombre  = input("archivo $ ")
    data=ObtenerDemandaDiaria(inicio, fin)
    df = build_df(data)
    df.to_excel(nombre+'.xlsx', sheet_name='Hoja1', index=False)
    
main()

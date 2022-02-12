import requests
import json
import pandas as pd
import numpy as np

def sort_data(data):
    fechas = {}
    by_planta = {}
    nombres_plantas = []
    for inst in data:
        if inst['fecha'] not in fechas.keys():
            fechas[inst['fecha']] = [inst]
        else:
            fechas[inst['fecha']].append(inst)
        if inst['planta'] not in nombres_plantas:
            nombres_plantas.append(inst['planta'])
        if inst['planta'] not in by_planta.keys():
            by_planta[inst['planta']] = [inst]
        else:
            by_planta[inst['planta']].append(inst)
    fechas_sort = sorted(fechas.keys())
    nombres_plantas = sorted(nombres_plantas)
    return [nombres_plantas,fechas_sort,fechas,by_planta]

def fetch_api(year, month, day):
    print("Esperando respuesta de CENCE...")
    response = requests.get('https://apps.grupoice.com/CenceWeb/data/sen/json/EnergiaHorariaFuentePlanta', params={'anno': year, 'mes': month, 'dia': day})
    if (response.status_code == 200):
        body = response.content.decode('utf-8')
        data = json.loads(body)['data']
        return data
    else:
        print("http error",response.status_code)
        exit()

def build_df(sorted_data):
    print("organizando datos...")
    df = 0
    plantas = sorted_data[0]
    fechas = sorted_data[1]
    data_by_fecha = sorted_data[2]
    data_by_planta = sorted_data[3]
    dic = {'plantas': []}
    for planta in plantas:
        dic['plantas'].append(planta)
    for fecha in fechas:
        dic[fecha] = []
        for planta in plantas:
            existe = False
            for objeto in data_by_planta[planta]:
                if objeto['fecha'] == fecha:
                    existe = True
                    dic[fecha].append(objeto['dato'])
            if not existe:
                dic[fecha].append(0)
    df = pd.DataFrame(dic)
    return df
    
def generar_entre_fechas(inicio, fin, file_name):
    dates = pd.date_range(start=inicio, end=fin)
    cont = 0
    with pd.ExcelWriter(file_name) as writer:
        for date in dates:
            data = fetch_api(date.year, date.month, date.day)
            vals = sort_data(data)
            df = build_df(vals)                             # data frame
            print("Escribiendo a archivo...")
            #genera excel
            df.to_excel(writer, sheet_name=str(date.day)+'-'+str(date.month)+'-'+str(date.year)[2]+''+str(date.year)[3], header=False, index=False)
            cont += 1
            print("Progreso: %.2f"%(cont/len(dates)*100),"%\n")
        print("Finalizado exitosamente")

def main():
    print("Fechas formato año mes día todo pegado")
    inicio = input("Fecha de inicio, ej 20190101\n$ ")
    fin = input("Fecha de fin, ej 20200101\n$ ")
    nombre = input("Nombre del archivo\n(No incluir extension .xlsx)\n$ ")
    print("")
    generar_entre_fechas(inicio, fin, nombre+".xlsx")
    
main()

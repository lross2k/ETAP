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
    print("Esperando servidor de CENCE...")
    response = requests.get('https://apps.grupoice.com/CenceWeb/data/sen/json/EnergiaHorariaFuentePlanta', params={'anno': year, 'mes': month, 'dia': day})
    if (response.status_code == 200):
        body = response.content.decode('utf-8')
        data = json.loads(body)['data']
        return data
    else:
        print("Error http",response.status_code)
        exit()

def build_df(sorted_data):
    print("Organizando datos...")
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

def generar_por_anno(fecha, dias, file_name):
    return pd.date_range(fecha, periods=dias)

def generar_por_annos(fecha, annos, file_name):
    return pd.date_range(fecha, periods=(int(annos)*365))

def generar_por_fechas(fecha1, fecha2, file_name):
    return pd.date_range(start=fecha1, end=fecha2)

def main():
    menu = input("¿Cómo desea ingresar las fechas?\n"+
                 "1. Rango de fechas exactas\n"+
                 "2. Cantidad de días a partir de fecha exacta\n"+
                 "3. Cantidad de años completos a partir de fecha exacta\n"+
                 "$ ")
    print("\nFormato de fechas AÑO MES DÍA todo pegado\n")
    nombre = input("nombre del archivo\n(No incluir extension .xlsx\n$ ")
    fecha1 = input("Fecha a iniciar\nej. 20191202 esto es 2 de Diciembre del 2019\n$ ")
    if menu == '1':
        fecha2 = input("Fecha a terminar\nej. 20191220 esto es 20 de Diciembre del 2019\n$ ")
        fechas = generar_por_fechas(fecha1, fecha2, nombre+".xlsx")
    elif menu == '2':
        dias = input("días que desea calcular\n$ ")
        fechas = generar_por_anno(fecha1, int(dias), nombre+".xlsx")
    elif menu == '3':
        annos = input("años que desea calcular\n$ ")
        fechas = generar_por_annos(fecha1, annos, nombre+".xlsx")
    with pd.ExcelWriter(nombre+".xlsx") as writer:
        for i in range(len(fechas)):
            data = fetch_api(fechas[i].year, fechas[i].month, fechas[i].day)
            vals = sort_data(data)
            df = build_df(vals)
            df.to_excel(writer, sheet_name=str(fechas[i].day)+'-'+str(fechas[i].month)+'-'+str(fechas[i].year)[2]+''+
                        str(fechas[i].year)[3], header=False, index=False)
            print("Completado %.3f%c" % (float(i+1)/float(len(fechas))*100.0, '%'))
    
if __name__ == "__main__":
    main()

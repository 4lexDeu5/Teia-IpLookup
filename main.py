# Teia (IpLookup) v2.1, Author @4lexDeu5 (Alejandro González)


import csv
import json
import re
from winotify import Notification, Notifier
import time
from collections import OrderedDict
from sys import exit
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import openpyxl
import pandas
import requests
from pandas import *

Tk().withdraw()

# Dialog box
imported_file = askopenfilename()  

execution_start = time.time()

direcciones = []
url1 = 'http://ip-api.com/batch?fields=message,country,city,isp,org,query'
url2 = 'https://api.abuseipdb.com/api/v2/check'
name = imported_file[:-4]
extension = imported_file.split('.')

print(imported_file)

# Lectura de CSV y extracción de lista de IPs

if extension[len(extension) - 1] == 'csv':  
    with open(imported_file, newline='') as oif:
        reader = csv.DictReader(oif)
        for row in reader:
            direcciones.append(row['Client_IP'])

# Lectura de TXT y extracción de lista de IPs

elif extension[len(extension) - 1] == 'txt':  
    ipv4_extract_pattern = "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    ipv6_extract_pattern = (r'^(?:(?:[0-9A-Fa-f]{1,4}:){6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}| \
                            (?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))| \
                                ::(?:[0-9A-Fa-f]{1,4}:){5}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]| \
                                    25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))| \
                                    (?:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4} \
                                        |(?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}| \
                                            2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}| \
                                                (?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))| \
                                                    (?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:){2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}| \
                                                        (?:(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))| \
                                                            (?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]| \
                                                                [1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))| \
                                                                    (?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]| \
                                                                        1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}(?:[0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))| \
                                                                            (?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::[0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:){,6}[0-9A-Fa-f]{1,4})?::)$')

    with open(imported_file, "r") as oif:
        lines = oif.read()
        for line in lines:
            direcciones_ipv4 = re.findall(ipv4_extract_pattern, lines)
            direcciones_ipv6 = re.findall(ipv6_extract_pattern, lines, re.M)

    direcciones = direcciones_ipv4 + direcciones_ipv6

else:
    print("ERROR: Introduzca un archivo compatible (.txt / .csv)", "[", extension[len(extension) - 1], "]")
    exit(1)

final_ip = list(OrderedDict.fromkeys(direcciones))


# Creación de documento Excel
archivo = name + '-teia.xlsx'
wb = openpyxl.Workbook(write_only=False)
wb.save(archivo)

# Whois
json_str = json.dumps(list(final_ip))

resp = requests.request(url=url1, method="POST", data=json_str)

if resp.status_code == 200:
    print(resp, "- OK")
    mensaje=str(resp.status_code) + " - OK"
else:
    print("ERROR. Code: ", resp.status_code)
    mensaje=str(resp.status_code) + " - ERROR"
    exit(1)

# Procesar JSON
decodedResponse = json.loads(resp.text)
df = json_normalize(resp.json())

# Mandar resultados a Excel
with pandas.ExcelWriter(archivo) as writer:
    df.to_excel(writer, sheet_name="Analysis")


headers = {
    'Accept': 'application/json',
    'Key': '' #YOUR AbuseIPDB API KEY
}

print(archivo)
fileEst = pandas.read_excel(archivo)
datos = fileEst['query']
xis = []
for row in datos:
    querystring = {
    'ipAddress': row
}
    print(querystring)

    response = requests.request(method='GET', url=url2, headers=headers, params=querystring)

# Formatted output

    try:
        decodedResponse = json.loads(response.text)
        data = decodedResponse['data']
        level1 = data['abuseConfidenceScore']
        print (level1)
        xis.append(level1)
    except:
        print("No data")
        xis.append("No data")

fileEst['abuseConfidence%']=pandas.DataFrame(xis)
fileEst.to_excel(archivo,index=False) 


execution_end = time.time()
ejecucion= round((execution_end - execution_start), 3)

toast = Notification(app_id=ejecucion,
                     title="TEIA",
                     msg=mensaje,
                     duration="short",
                     icon=r"C:\Users\alejandro.gonzalez\Desktop\Teia\icon.ico"
                     )

toast.add_actions(label="Abrir", launch=archivo)

toast.show()

exit(0)

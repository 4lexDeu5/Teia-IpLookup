#!/usr/bin/env python3

# Teia (IpLookup) v1.0, Author @4lex_deus (Alejandro González)

import csv
import json
import re
import sys
import time
from collections import OrderedDict

import openpyxl
import pandas
import requests
from pandas import *

execution_start = time.time()

imported_file = sys.argv[1]

direcciones = []
url = 'http://ip-api.com/batch?fields=message,country,city,isp,org,asname,query'
name = imported_file[:-4]
extension = imported_file.split('.')

if extension[1] == 'csv':  # Lectura de CSV y extracción de lista de IPs
    with open(imported_file, newline='') as oif:
        reader = csv.DictReader(oif)
        for row in reader:
            direcciones.append(row['Client_IP'])

elif extension[1] == 'txt':  # Lectura de TXT y extracción de lista de IPs
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
    print("ERROR: Introduzca un archivo compatible (.txt / .csv)")
    exit(1)

final_ip = list(OrderedDict.fromkeys(direcciones))

# Creación de documento Excel
wb = openpyxl.Workbook(write_only=False)
wb.save(name + '.xlsx')

# Whois
json_str = json.dumps(list(final_ip))

resp = requests.request(url=url, method="POST", data=json_str)

if resp.status_code == 200:
    print(resp, "- OK")
else:
    print("ERROR. Code: ", resp.status_code)
    exit(1)

# JSON Decode
decodedResponse = json.loads(resp.text)
df = json_normalize(resp.json())

# Mandar resultados a Excel
with pandas.ExcelWriter(name + '.xlsx') as writer:
    df.to_excel(writer, sheet_name="Analysis")

execution_end = time.time()
print("Tiempo de ejecución:", round((execution_end - execution_start), 3), "segundos.")

exit(0)

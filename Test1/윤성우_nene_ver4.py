import urllib.request
import os
from pandas import DataFrame
import xml.etree.ElementTree as ET
import time

print("START")

result = []
dir_name = "V4_BigData"
dir_nene = "Nene_data"
dir_delimiter = "\\"
file_name = "nene"
count = "nene_count.txt"
csv = '.csv'
result_limit = 12

def make_dir(number):
    os.mkdir(dir_name + dir_delimiter + dir_nene + str(number))
    return None

def make_nene(index_number,file_number):
    import csv

    number = 1

    with open(dir_name + dir_delimiter + "nene.csv", 'r') as infile:
        data = list(csv.reader(infile))

    while True:
        number_limit = number + 100
        f = open(dir_name + dir_delimiter + dir_nene + str(index_number) + dir_delimiter + file_name + str(file_number) +".csv", 'w', newline='')
        csvWrite = csv.writer(f)
        csvWrite.writerow(['store','sido','gungu','store_address'])
        for i in data[number:number_limit]:
            csvWrite.writerow(i)
        file_number += 1
        number = number_limit
        if file_number > result_limit:
            break

response = urllib.request.urlopen('http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'%(urllib.parse.quote('전체'),urllib.parse.quote('전체')))

xml = response.read().decode('UTF-8')
root = ET.fromstring(xml)

for element in root.findall('item'):
    store_name = element.findtext('aname1')
    store_sido = element.findtext('aname2')
    store_gungu = element.findtext('aname3')
    store_address = element.findtext('aname5')

    result.append([store_name]+[store_sido]+[store_gungu]+[store_address])

nene_table = DataFrame(result,columns=('store','sido','gungu','store_address'))

try:
    os.mkdir(dir_name)
    nene_table.to_csv(dir_name+dir_delimiter+"nene.csv",encoding='cp949',mode='w',index=False)
except:pass

try:
    with open(dir_name + dir_delimiter + count, 'r') as file:
        file_number = file.readline()
        file_number = int(file_number)
        make_dir(file_number)
        make_nene(file_number, 1)
        file_number +=1

    with open(dir_name + dir_delimiter + count, 'w') as file:
        file.write(str(file_number))

except FileNotFoundError:
    with open(dir_name + dir_delimiter + count, 'w') as file:
        file.write("2")
        make_dir(1)
        make_nene(1,1)
print("END!!!")
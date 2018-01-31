import urllib.request
import os
from pandas import DataFrame
import xml.etree.ElementTree as ET

print("START")

result = []
dir_name = "V2_BigData"
dir_nene = "Nene_data"
dir_delimiter = "\\"
file_name = "nene"
count = "nene_count.txt"
csv = '.csv'
result_limit = 3

def make_dir(number):
    os.mkdir(dir_name + dir_delimiter + dir_nene + str(number))
    return None

def make_nene(index_number,file_number):
    dir_totalname = dir_name + dir_delimiter + dir_nene + str(index_number) + dir_delimiter + file_name + str(file_number) + csv
    nene_table.to_csv(dir_totalname, encoding="cp949", mode='w', index=True)
    return None

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
except:pass

try:
    with open(dir_name + dir_delimiter + count, 'r') as file:
        file_number = file.readline()
        file_number = int(file_number)
        index_num = int(file_number/result_limit)
        if file_number % result_limit != 0:
            index_num += 1
        if file_number % result_limit == 1:
            make_dir(index_num)
        make_nene(index_num, file_number)
        file_number += 1

    with open(dir_name + dir_delimiter + count, 'w') as file:
        file.write(str(file_number))

except FileNotFoundError:
    with open(dir_name + dir_delimiter + count, 'w') as file:
        file.write("2")
        make_dir(1)
        make_nene(1,1)
print("END!!!")
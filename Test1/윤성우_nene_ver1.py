import urllib.request
import os
from pandas import DataFrame
import xml.etree.ElementTree as ET

print("START")
result = []
dir_name = "V1_BigData"
dir_delimiter = "\\"
file_name = "nene"
count = "nene_count.txt"
csv = '.csv'

def make_nene(number):
    dir_totalname = dir_name + dir_delimiter + file_name + str(number) + csv
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
        index_num = file.readline()
        index_num = int(index_num)
        make_nene(index_num)
        index_num += 1

    with open(dir_name + dir_delimiter + count, 'w') as file:
        file.write(str(index_num))

except FileNotFoundError:
    with open(dir_name + dir_delimiter + count, 'w') as file:
        file.write("2")
        make_nene(1)
print("END!!!")
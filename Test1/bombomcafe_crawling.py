import urllib.request
from pandas import DataFrame
from bs4 import BeautifulSoup

print("Web Crawling을 시작합니다.")

result = []
result_branch = []
result_address = []
result_region = []
region_groups = []
seoul = 0
kyeonggi = 0
kwangwon = 0
incheon = 0
chungbuk = 0
chungnam = 0
daegu = 0
keongbuk = 0
keongnam = 0
jeonbuk = 0
jeonnam = 0
kwangju = 0
ulsan = 0
busan = 0
jeju = 0
sejong = 0
dajeon = 0

for i in range(1,11):
    html = urllib.request.urlopen('http://cafebombom.co.kr/pg/bbs/board.php?bo_table=store01&page=%s'% i)
    soup = BeautifulSoup(html,'html.parser')

    print("Destination : 'http://cafebombom.co.kr/pg/bbs/board.php?bo_table=store01&page=%s'"% i)
    store = soup.findAll('td',attrs={'class':'list-subject'})
    address = soup.findAll('td',attrs={'class':'text-center en font-11'})
    region = soup.findAll('span',attrs={'class':'text-muted font-11'})

    for element in store:
        element_strip = element.get_text(strip=True)
        result_branch.append(element_strip)

    for element in address[:30]:
        address_inf = element.get_text(strip=True)
        result_address.append(address_inf)

    for element in region:
        element_strip = element.get_text(strip=True)
        if element_strip == '서울':
            seoul += 1
        elif element_strip == '경기':
            kyeonggi += 1
        elif element_strip == '인천':
            incheon += 1
        elif element_strip == '강원':
            kwangwon += 1
        elif element_strip == '충북':
            chungbuk += 1
        elif element_strip == '충남':
            chungnam += 1
        elif element_strip == '대전':
            dajeon += 1
        elif element_strip == '세종':
            sejong += 1
        elif element_strip == '대구':
            daegu += 1
        elif element_strip == '경북':
            keongbuk += 1
        elif element_strip == '경남':
            keongnam += 1
        elif element_strip == '부산':
            busan += 1
        elif element_strip == '울산':
            ulsan += 1
        elif element_strip == '광주':
            kwangju += 1
        elif element_strip == '전북':
            jeonbuk += 1
        elif element_strip == '전남':
            jeonnam += 1
        elif element_strip == '제주':
            jeju += 1
        result_region.append(element_strip)


for i in range(len(result_branch)):
    branch = result_branch[i]
    region = result_region[i]
    information = result_address[(2*i)+1]
    address = result_address[(2*i)+2]
    result.append([branch] + [region] + [information] + [address])


bombom_table = DataFrame(result,columns=('지점','지역','주소','전화번호'))
bombom_table.to_csv('bombom_수집데이터.csv', encoding="cp949",mode='w',index=False)


seoul_rate = "%0.2f%%" %(seoul/len(result_region)*100)
print("'경기'지역 매장 분포율 : %0.2f%%" %(kyeonggi/len(result_region)*100))
print("'인천'지역 매장 분포율 : %0.2f%%" %(incheon/len(result_region)*100))
print("'강원'지역 매장 분포율 : %0.2f%%" %(kwangwon/len(result_region)*100))
print("'충북'지역 매장 분포율 : %0.2f%%" %(chungbuk/len(result_region)*100))
print("'충남'지역 매장 분포율 : %0.2f%%" %(chungnam/len(result_region)*100))
print("'대전'지역 매장 분포율 : %0.2f%%" %(dajeon/len(result_region)*100))
print("'경북'지역 매장 분포율 : %0.2f%%" %(keongbuk/len(result_region)*100))
print("'경남'지역 매장 분포율 : %0.2f%%" %(keongnam/len(result_region)*100))
print("'대구'지역 매장 분포율 : %0.2f%%" %(daegu/len(result_region)*100))
print("'울산'지역 매장 분포율 : %0.2f%%" %(ulsan/len(result_region)*100))
print("'부산'지역 매장 분포율 : %0.2f%%" %(busan/len(result_region)*100))
print("'세종'지역 매장 분포율 : %0.2f%%" %(sejong/len(result_region)*100))
print("'전북'지역 매장 분포율 : %0.2f%%" %(jeonbuk/len(result_region)*100))
print("'전남'지역 매장 분포율 : %0.2f%%" %(jeonnam/len(result_region)*100))
print("'광주'지역 매장 분포율 : %0.2f%%" %(kwangju/len(result_region)*100))
print("'제주'지역 매장 분포율 : %0.2f%%" %(jeju/len(result_region)*100))



bombom_table = DataFrame(result_record,columns=('지역','지점수','비율'))
bombom_table.to_csv('bombom.csv', encoding="cp949",mode='w',index=False)
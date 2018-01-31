import urllib.request
from bs4 import BeautifulSoup
from pandas import DataFrame

html = urllib.request.urlopen('http://movie.naver.com/movie/sdb/rank/rmovie.nhn')
soup = BeautifulSoup(html,'html.parser')
# print(soup)
# print(soup.prettify())


tags =  soup.findAll('div', attrs={'class':'tit3'})
ranks = soup.findAll('td', attrs={'class':'range ac'})
up_down =  soup.find('img', attrs={'src':'http://imgmovie.naver.net/2007/img/common/icon_na_1.gif'})

result_movie = []
for i in tags:
    div_tag = list(i.strings)
    if(div_tag[1]):
        result_movie.append(div_tag[1])


result_change = []
for i in ranks:
    div_rank = list(i.strings)
    if(div_rank[0]):
        result_change.append(div_rank[0])
    # print(result_change)

result = []
for i in range(len(result_movie)):
    rank = i+1
    movie = result_movie[i]
    change = result_change[i]
    result.append([str(rank)] + [movie] + [change])

naver_realtime_table = DataFrame(result, columns=('순위', '영화명', '변동폭'))
naver_realtime_table.to_csv('윤성우_naver_realtime_movie_ranking.csv', encoding="cp949", mode='w', index=False)
# 과제
# 네이버 영화 랭킹 웹페이지를 분석하여 아래 형식으로 csv 파일을 생성하시오
# 순위 |      영화명       | 변동폭
#  1_23_bigdata   |       1987        |   0
#  2   |  신과함께-죄와 벌 |  +1_23_bigdata
#  3   |쥬만지: 새로운세계 |  -1_23_bigdata.
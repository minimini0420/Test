import json
import urllib.request
import datetime
import time
import threading
# HK Comment] 공통 사항
# 1. 변수명은 최대한 가독성 높게 (나쁜 예: dt ..)
# 2. 실시간 Update 할 떄나 인공지능 모드에 의해서 Scheduling 작업시 기상정보 가져온후
#    발코니창이 문닫는 조건이 된다면 문 닫는 로직 추가
# 시뮬레이션 데이터는 필요한 데이터만 저장하던지 아니면 실제 response 데이터를 조작하던지 할것
# 실시간 기상 정보 Update하면 장비제어와 관련된 기상정보는 따로 출력한다.

# 실제 홈네트워크 시스템처럼 한번 가동되면 꺼지지 않게.( 따라서 재시작에 대한 고려는 일단 X)
g_Radiator = False # 전역변수 지역변수 변수명에 표시( 회사에서 꼭 쓴다고 함. )
g_Gas_Valve = False
g_Balcony_Windows = False # 건축법 시행령에 따라 베란다가 아닌 폐쇄형 발코니가 정확한 표현
g_Door = False # 출입문
g_humidifier = False # 가습기
g_dehumidifier = False # 제습기
g_AI_Mode = False

def print_main_menu():
    print("\n<< SMART HOME NETWORK SERVICE ver1.0 >>")
    print("-" * 40)
    print("1. 장비 상태 확인")
    print("2. 장비 제어 모드 (수동)")
    print("3. 스마트 모드")
    print("4. 시뮬레이션 모드")
    print("5. 프로그램 종료")
    print("-" * 40)

def device_status(device, device_status, on_messege='', off_messege=''):
    print("%s : " % device, end = '')
    if device_status == True : print("작동(열림)")
    elif device_status == False : print("정지(닫힘)")

def check_device_status():
    print("\n" + "-" * 25)
    device_status('난방기', g_Radiator)
    device_status('가스밸브', g_Gas_Valve)
    device_status('발코니(베란다) 창문', g_Balcony_Windows)
    device_status('출입문', g_Door)
    device_status('가습기', g_humidifier)
    device_status('제습기', g_dehumidifier)
    print("-" * 25)

def print_device_menu():
    print("\n<< 작동 가능한 기기 >>")
    print("1. 난방기")
    print("2. 가스벨브")
    print("3. 발코니 창문")
    print("4. 출입문")
    print("5. 가습기")
    print("6. 제습기")
    print("7. 스마트 스피커( 영화 검색 )")
    print("0. 뒤로가기")

def control_device_menu():
    global g_Radiator, g_Gas_Valve, g_Balcony_window, g_Door , g_humidifier ,g_dehumidifier
    number = int(input("메뉴를 선택하세요 : "))
    if number > 0:
        check_device_status()
        if number == 1: g_Radiator  = not g_Radiator
        elif number == 2: g_Gas_Valve = not g_Gas_Valve
        elif number == 3: g_Balcony_window = not g_Balcony_window
        elif number == 4: g_Door = not g_Door
        elif number == 5: g_humidifier = not g_humidifier
        elif number == 6: g_dehumidifier = not g_dehumidifier
        check_device_status()
    else:
        return number

def getWeather(nx,ny) :
    access_key = "5X8xep2Y7D1S6%2BGl%2BnrnabFJiL%2FVdT8wO7ipvtPwWTvV7bgtEFuqBqGgmYS8Z1hnj0BWMtukD5u9QihQlbmGKQ%3D%3D"

    base_time = time.strftime("%H%M",time.localtime(time.time()))
    base_time = int(base_time) - 100
    base_time = str(base_time).zfill(4)

    end_point = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData"
    parameters = "?base_date=" + time.strftime("%Y%m%d", time.localtime(time.time()))
    parameters += "&base_time=" + base_time
    parameters += "&numOfRows=" + "30"
    parameters += "&nx=" + nx
    parameters += "&ny=" + ny
    parameters += "&_type=json&serviceKey=" + access_key

    url = end_point + parameters
    retData = get_request_url(url)

    if retData == None :
        return None
    else:
        return  json.loads(retData)

def show_weather_main():
    jsonResult = []
    nx = '89'
    ny = '91'
    jsonData = getWeather(nx,ny)

    if (jsonData['response']['header']['resultMsg'] == "OK"):
        for element in jsonData['response']['body']['items']['item']:
            jsonResult.append(element)
    return jsonResult

def weather_save(jsonResult):
    with open('%s_기상예보.json' % time.strftime("%Y%m%d",time.localtime(time.time())),'w',encoding='utf8') as outfile:
        retJson = json.dumps(jsonResult,indent=4,sort_keys=True,ensure_ascii=False)
        outfile.write(retJson)

    print("%s_기상예보.json" % time.strftime("%Y%m%d_%H%M",time.localtime(time.time())))

def smart_mode():
    global g_AI_Mode
    print("\n<< 스마트 모드 >>")
    print("1. 인공지능 모드 상태 조회")
    print("2. 인공지능 모드 상태 변경")
    print("3. 실시간 기상정보 Update")
    menu_num = int(input("메뉴를 선택하세요 : "))

    if menu_num == 1 :
        print("\n현재 인공지능 모드 : ", end="")
        if g_AI_Mode == True:  print("작동")
        else : print("중지")

    elif menu_num == 2 :
        print("인공지능 모드: ", end='')
        g_AI_Mode = not g_AI_Mode
        if g_AI_Mode == True:
            print("작동")
        else:
            print("정지")

    elif menu_num == 3 :
        if __name__ == "__main__":
            weather_save(show_weather_main())

    elif menu_num == 4 :
        global g_Balcony_window
        weather_list = []
        weather_info = {}
        weather_info["category"] = "RN1"
        weather_info["fcstValue"] = "10"
        weather_info["fsctTime"] =  1600
        weather_list.append(weather_info)

        with open("창문을닫자.json", "w", encoding="utf-8") as outfile:
            weather_record = json.dumps(weather_list, indent=4, sort_keys=True, ensure_ascii=False)
            outfile.write(weather_record)

        with open("창문을닫자.json", encoding="utf8") as json_file:
            json_object = json.load(json_file)
            json_string = json.dumps(json_object)
            jsonResult = json.loads(json_string)

        print("발코니 창문 상태 : ", end='')
        if g_Balcony_window == True:
            print("열림")
            if jsonResult[0]["fcstValue"] != "0":
                g_Balcony_window = not g_Balcony_window
                print("닫힘")
        elif g_Balcony_window == False:
            print("닫힘")

def simulation_mode():
    print("<< 시뮬레이션 모드 >>")
    print("1. 비 오는 날 시뮬레이션 (발코니창문 제어)")
    print("2. 습한 날 시뮬레이션 (제습기 제어)")
    print("3. 건조한 날 시뮬레이션 (가습기 제어)")
    print("4. 상쾌한 날 시뮬레이션 (제습기/가습기 제어)")

def get_request_url(url):
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" %datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL:%s" %(datetime.datetime.now(), url))
        return None

def update_scheduler():
    global g_Balcony_Windows
    while True:
        if g_AI_Mode == False:
            continue
        else:
            time.sleep(5)
            g_Balcony_Windows = not g_Balcony_Windows

t = threading.Thread(target=update_scheduler)
t.daemon = True
t.start()

while True:
    print_main_menu()
    menu_num = int(input("메뉴를 선택하세요 : "))

    if menu_num == 1 :
        check_device_status()

    elif menu_num == 2:
        number = print_device_menu()
        if control_device_menu() == 0 :
            continue

    elif menu_num == 3:
        smart_mode()

    elif menu_num == 4:
        simulation_mode()

    elif menu_num == 5:
        print("프로그램을 종료합니다......")
        break
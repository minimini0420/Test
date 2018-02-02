import json
import urllib.request
import datetime
import time
import threading
import random
# HK Comment] 공통 사항
# 1. 변수명은 최대한 가독성 높게 (나쁜 예: dt ..)
# 2. 실시간 Update 할 떄나 인공지능 모드에 의해서 Scheduling 작업시 기상정보 가져온후
#    발코니창이 문닫는 조건이 된다면 문 닫는 로직 추가
# 시뮬레이션 데이터는 필요한 데이터만 저장하던지 아니면 실제 response 데이터를 조작하던지 할것
# 실시간 기상 정보 Update하면 장비제어와 관련된 기상정보는 따로 출력한다.

# 실제 홈네트워크 시스템처럼 한번 가동되면 꺼지지 않게 해야함
g_Radiator = False         # 난방기
g_Gas_Valve = False        # 가스벨브
g_Balcony_Windows = False  # 폐쇄형 발코니가 옳은 표현
g_Door = False             # 출입문
g_humidifier = False       # 가습기
g_dehumidifier = False     # 제습기
g_AI_Mode = False          # 인공지능 모드
nx = '89'
ny = '91'
g_Max_Acceptable_humidity_level = 60
g_Min_Acceptable_humidity_level = 50

base_date = time.strftime("%Y%m%d", time.localtime(time.time()))
base_time = time.strftime("%H%M",time.localtime(time.time()))

def Auto_scheduler():
    time_check_45min = False
    while True:
        if g_AI_Mode == True :
            current_time = datetime.datetime.now()

            if current_time.minute == 45 and time_check_45min == False :
                weather_info_data = get_weather_info(nx,ny)
                auto_window(weather_info_data)
                auto_humidifier(weather_info_data)
                auto_dehumidifier(weather_info_data)
                time_check_45min = True

            elif current_time.minute != 45 :
                time_check_45min = False

def auto_start_show():

def auto_window(data):
    global g_Balcony_Windows
    device_status('발코니(베란다) 창문', g_Balcony_Windows)
    for i in range(len(data['response']['body']['items']['item'])):
        if data['response']['body']['items']['item'][i]['category'] == 'RN1' :
            if data['response']['body']['items']['item'][i]['fcstValue'] != 0:
                if g_Balcony_Windows == True :
                    print("- 비바람이 몰아치고 있습니다. 창문을 닫습니다.")
                    g_Balcony_Windows = not g_Balcony_Windows
                    device_status('발코니(베란다) 창문', g_Balcony_Windows)
                    print("- 창문이 닫혔습니다.")
                else : pass

def auto_humidifier(data):
    global g_humidifier
    device_status('가습기', g_humidifier)
    for i in range(len(data['response']['body']['items']['item'])):
        if data['response']['body']['items']['item'][i]['category'] == 'REH' :
            if data['response']['body']['items']['item'][i]['fcstValue'] > 70:
                if g_humidifier == False :
                    print("- 습도가 높은 날씨입니다. 가습기를 가동합니다.")
                    g_humidifier = not g_humidifier
                    device_status('가습기', g_humidifier)
                    print("- 가습기가 가동 중 입니다.")
                else : pass

def auto_dehumidifier(data):
    global g_dehumidifier
    device_status('제습기', g_dehumidifier)
    for i in range(len(data['response']['body']['items']['item'])):
        if data['response']['body']['items']['item'][i]['category'] == 'REH' :
            if data['response']['body']['items']['item'][i]['fcstValue'] < 31:
                if g_dehumidifier == False :
                    print("- 습도가 낮은 날씨입니다. 제습기를 가동합니다.")
                    g_dehumidifier = not g_dehumidifier
                    device_status('제습기', g_dehumidifier)
                    print("- 제습기가 가동 중 입니다.")
                else : pass

def print_main_menu():
    print("\n   << SMART HOME NETWORK SERVICE ver1.0 >>")
    print("-" * 45)
    print("1. 장비 상태 확인\n2. 장비 제어 모드 (수동)\n3. 스마트 모드\n4. 시뮬레이션 모드\n5. 프로그램 종료")
    print("-" * 45)

def device_status(device, device_status, on_messege = '- ON -', off_messege = '- OFF -'):
    print("%s :\t" % device, end = '')
    if device_status == True : print(on_messege)
    elif device_status == False : print(off_messege)

def check_device_status():
    print("\n" + "-" * 45)
    device_status('난방기', g_Radiator)
    device_status('가스밸브', g_Gas_Valve)
    device_status('발코니(베란다) 창문', g_Balcony_Windows)
    device_status('출입문', g_Door)
    device_status('가습기', g_humidifier)
    device_status('제습기', g_dehumidifier)
    print("-" * 45)

def print_device_menu():
    print("\n\t\t<< 작동 가능한 기기 >>")
    print("-" * 45)
    print("1. 난방기\n2. 가스벨브\n3. 발코니 창문\n4. 출입문\n5. 가습기\n6. 제습기\n0. 뒤로가기")
    print("-" * 45)

def control_device_menu():
    global g_Radiator, g_Gas_Valve, g_Balcony_Windows, g_Door , g_humidifier ,g_dehumidifier
    number = int(input("\n메뉴를 선택하세요 : "))
    if number > 0:
        check_device_status()
        if number == 1: g_Radiator  = not g_Radiator
        elif number == 2: g_Gas_Valve = not g_Gas_Valve
        elif number == 3: g_Balcony_Windows = not g_Balcony_Windows
        elif number == 4: g_Door = not g_Door
        elif number == 5: g_humidifier = not g_humidifier
        elif number == 6: g_dehumidifier = not g_dehumidifier
        check_device_status()
    else:
        return number

def get_weather_info(nx,ny) :
    global base_time, base_date
    access_key = "5X8xep2Y7D1S6%2BGl%2BnrnabFJiL%2FVdT8wO7ipvtPwWTvV7bgtEFuqBqGgmYS8Z1hnj0BWMtukD5u9QihQlbmGKQ%3D%3D"

    base_time = int(base_time) - 100
    base_time = str(base_time).zfill(4)

    end_point = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData"
    parameters = "?base_date=" + base_date
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
    global nx, ny
    jsonResult = []
    jsonData = get_weather_info(nx,ny)

    if (jsonData['response']['header']['resultMsg'] == "OK"):
        for element in jsonData['response']['body']['items']['item']:
            jsonResult.append(element)
    return jsonResult

def weather_save(jsonResult, json_name):
    with open('%s_동구_신암동_기상예보.json' % time.strftime("%Y%m%d",time.localtime(time.time())),'w',encoding='utf8') as outfile:
        retJson = json.dumps(jsonResult,indent=4,sort_keys=True,ensure_ascii=False)
        outfile.write(retJson)

    print("%s_동구_신암동_기상예보.json" % time.strftime("%Y%m%d_%H%M",time.localtime(time.time())))

def smart_mode():
    global g_AI_Mode
    print("\n\t\t\t<< 스마트 모드 >>")
    print("-" * 45)
    print("1. 인공지능 모드 상태 조회\n2. 인공지능 모드 상태 변경\n3. 실시간 기상정보 Update")
    print("-" * 45)
    menu_num = int(input("\n메뉴를 선택하세요 : "))

    if menu_num == 1 :
        print("\n\t\t<< 인공지능 모드 상태 조회 >>")
        print("-" * 45)
        device_status("인공지능 모드", g_AI_Mode)
        print("-" * 45)

    elif menu_num == 2 :
        print("\n\t\t<< 인공지능 모드 상태 변경 >>")
        print("-" * 45)
        device_status("인공지능 모드", g_AI_Mode)
        g_AI_Mode = not g_AI_Mode
        print("------- 변경 중 -------")
        device_status("인공지능 모드", g_AI_Mode)
        print("-" * 45)

    elif menu_num == 3 :
        if __name__ == "__main__":
            weather_save(show_weather_main())

def simulation_mode():
    print("\t\t\t<< 시뮬레이션 모드 >>")
    print("-" * 45)
    print("1. 비 오는 날 시뮬레이션 (발코니창문 제어)\n2. 습한 날 시뮬레이션 (제습기 제어)\n3. 건조한 날 시뮬레이션 (가습기 제어)\n4. 상쾌한 날 시뮬레이션 (제습기/가습기 제어)")
    print("-" * 45)

def situation_simulator(result):
    global g_dehumidifier, g_humidifier, g_Radiator, g_Door, g_Gas_Valve, g_Balcony_Windows

    print("\n" + "-" * 45)
    if result[0]['category'] == "RN1":

        if result[0]['fcstValue'] != 0 :
            print("- 현재 비가 오고 있습니다. 강수량 %s mm 입니다" %result[0]['fcstValue'])
            if g_Balcony_Windows == True :
                print("- 발코니 창문이 열려있습니다 !!!")
                g_Balcony_Windows = not g_Balcony_Windows
                print("- 발코니 창문을 닫았습니다")
            else : print("- 발코니 창문이 닫혀 있습니다 - ")

    elif result[0]['category'] == "REH":

        if result[0]['fcstValue'] < 31 :
            print("- 현재 습도가 낮습니다. 현재 습도 :  %s %% 입니다" % result[0]['fcstValue'])
            if g_humidifier == False:
                print("- 가습기가 꺼져 있습니다 !!!")
                g_humidifier = not g_humidifier
                print("- 가습기를 가동합니다")
            else: print("이미 가습기가 가동 중 입니다")

        elif result[0]['fcstValue'] > 70 :
            print("- 현재 습도가 높습니다. 현재 습도 :  %s %% 입니다" % result[0]['fcstValue'])
            if g_dehumidifier == False:
                print("- 제습기가 꺼져 있습니다 !!!")
                g_dehumidifier = not g_dehumidifier
                print("- 제습기를 가동합니다")
            else : print("이미 제습기가 가동 중 입니다")

        elif 70 > result[0]['fcstValue'] > 30 :
            print("- 상쾌한 날씨입니다. 현재 습도 :  %s %% 입니다" % result[0]['fcstValue'])
            if g_dehumidifier == True and g_dehumidifier == True:
                print("- 제습기가 작동 중 입니다")
                g_dehumidifier = not g_dehumidifier
                print("- 제습기 가동을 멈춥니다")

def simulation_controll():
    global g_dehumidifier, g_humidifier, g_Radiator, g_Door, g_Gas_Valve, g_Balcony_Windows
    simulation_weather_list = []
    simulation_weather = {}
    simulation_weather["basedate"] = base_date
    simulation_weather["basetime"] = base_time
    simulation_weather["fcstdate"] = base_date
    simulation_weather["fcsttime"] = base_time
    simulation_weather["nx"] = 89
    simulation_weather['ny'] = 91

    number = int(input("\n메뉴를 선택하세요 : "))
    if number == 1 :
        simulation_weather["category"] = "RN1"
        simulation_weather["fcstValue"] = random.randint(1,100)

    elif 5 > number > 1 :
        simulation_weather["category"] = "REH"
        simulation_weather["fcstValue"] = random.randint(1,100)

    simulation_weather_list.append(simulation_weather)
    return simulation_weather_list

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

AI_t = threading.Thread(target=Auto_scheduler)
AI_t.daemon = True
AI_t.start()

while True:
    print_main_menu()
    menu_num = int(input("\n메뉴를 선택하세요 : "))

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
        situation_simulator(simulation_controll())

    elif menu_num == 5:
        print("<< 프로그램을 종료합니다 >>")
        break
import time
import utime
import ujson
import os
import urequests
import network
from machine import I2C,Pin,RTC         #从machine模块导入I2C、Pin、RTC子模块
from oled import SSD1306_I2C     #从oled模块中导入SSD1306_I2C子模块

i2c = I2C(sda=Pin(4), scl=Pin(5),freq=1000000 ) #I2C初始化：sda--> P4, scl --> P5,频率8MHz
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

#  oled.text（"",x,y）x表示从第几列，y表示从第几行开始
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
start_time = time.time()  # 判断是否超时连接
ssid = "Q5-2024"          #连接的wifi账户
password = "15938510562"  #wifi密码

#创建User-Agent
headers: dict[str, str] = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:50.0) Gecko/20100101 Firefox/50.0'
}   

def convertTurple(tup):
    return (tup[0],tup[1],tup[2],tup[6],tup[3],tup[4],tup[5],0)
def fromTurpleToTimeStr(tup):
    return (str(tup[0]-30)+"-"+fromNumToStr(tup[1])+"-"+fromNumToStr(tup[2]),
            fromNumToStr(tup[4]+8)+":"+fromNumToStr(tup[5])+":"+fromNumToStr(tup[6]))
def fromNumToStr(n):
    result=str(n)
    if len(result)<2:
        result="0"+result
    return result

if not wlan.isconnected():
    oled.text("connecting", 0,  0)      #写入第1行内容
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():

        if time.time() - start_time > 15:  # 是否连接超时
            oled.text("fail", 0,  20)      #写入第1行内容
            break


oled.text('Micropython', 20, 5)
oled.show()
oled.invert(False)

while True:
    ## 连接淘宝API，获得时间戳Unix ，并将其转化为北京时间，存在RTC时钟中 ##
    gettime = urequests.get('http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',headers = headers)
    time_internet = ujson.loads(gettime.text)
    Unix_time = time_internet['data']['t'][:-3]   #获取时间戳  [:-3]为去掉字符串的后三位
    Time_now = utime.localtime(int(Unix_time))
    rtc=RTC()
    #设置RTC时间
    rtc.datetime(convertTurple(Time_now))
    
    ## 连接心知天气API，获得惠州、洛阳、开封的天气信息 并通过json解析存至字典中 ##
    result1 = urequests.get(
        'https://api.seniverse.com/v3/weather/now.json?key=SXMzpkrsCljzhG117&location=kaifeng&language=zh-Hans&unit=c')
    j1 = ujson.loads(result1.text)
    
    result2 = urequests.get(
        'https://api.seniverse.com/v3/weather/now.json?key=SXMzpkrsCljzhG117&location=huizhou&language=zh-Hans&unit=c')
    j2 = ujson.loads(result2.text)    
    
    result3 = urequests.get(
        'https://api.seniverse.com/v3/weather/now.json?key=SXMzpkrsCljzhG117&location=luoyang&language=zh-Hans&unit=c')
    j3 = ujson.loads(result3.text)
    
    i = 0           #每循环一百次，刷新一次天气信息#
    while True:
        #基于日期时间信息元组生成显示所需的日期、时间字符串元组
        timeNr=fromTurpleToTimeStr(rtc.datetime())
        #清空屏幕
        oled.fill(0)
        #显示日期
        oled.text(timeNr[0],26,20,1)
        #显示时间
        oled.text(timeNr[1],34,36,1)
        #执行显示
        oled.show()
        #休眠
        utime.sleep(0.3)
        
        time.sleep(3)
        
        i = i+1
        oled.fill(0)
        oled.show()
        oled.text('kaifeng', 25, 5)
        oled.text('temperature:' + j1['results'][0]['now']['temperature'], 0, 20)
        oled.text('humidity:' + j1['results'][0]['now']['humidity'] + '%', 0, 30)
        oled.text('pressure:' + j1['results'][0]['now']['pressure'] + 'Pa', 0, 40)
        oled.text('windspeed:' + j1['results'][0]['now']['wind_speed'] + 'km/h', 0, 50)
        oled.show()
        
        time.sleep(5)


        oled.fill(0)
        oled.show()
        
        oled.text('huizhou', 25, 5)
        oled.text('temperature:' + j2['results'][0]['now']['temperature'], 0, 20)
        oled.text('humidity:' + j2['results'][0]['now']['humidity'] + '%', 0, 30)
        oled.text('pressure:' + j2['results'][0]['now']['pressure'] + 'Pa', 0, 40)
        oled.text('windspeed:' + j2['results'][0]['now']['wind_speed'] + 'km/h', 0, 50)
        
        oled.show()
        time.sleep(5)




        oled.fill(0);
        oled.show();                   
        oled.text('luoyang', 25, 5)
        oled.text('temperature:' + j3['results'][0]['now']['temperature'] , 0, 20)
        oled.text('humidity:' + j3['results'][0]['now']['humidity'] + '%', 0, 30)
        oled.text('pressure:' + j3['results'][0]['now']['pressure'] + 'Pa', 0, 40)
        oled.text('windspeed:' + j3['results'][0]['now']['wind_speed'] + 'km/h', 0, 50)

        oled.show()

        time.sleep(5)
        if i==100:
            break



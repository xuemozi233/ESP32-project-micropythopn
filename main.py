import time
import ujson
import os
import urequests
import network
from machine import I2C,Pin         #从machine模块导入I2C、Pin子模块
from oled import SSD1306_I2C     #从oled模块中导入SSD1306_I2C子模块

i2c = I2C(sda=Pin(4), scl=Pin(5),freq=80000 ) #I2C初始化：sda--> P4, scl --> P5,频率8MHz
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

#  oled.text（"",x,y）x表示从第几列，y表示从第几行开始
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
start_time = time.time()  # 判断是否超时连接
ssid = "Q5-2024"
password = "15938510562"

if not wlan.isconnected():
    oled.text("connecting", 0,  0)      #写入第1行内容
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():

        if time.time() - start_time > 15:  # 是否连接超时
            oled.text("fail", 0,  20)      #写入第1行内容
            break

oled.text("connecting", 1,  1)      #写入第1行内容
oled.text('Micropython', 20, 5)
oled.show()
oled.invert(False)
while True:
    result1 = urequests.get(
        'https://api.seniverse.com/v3/weather/now.json?key=SXMzpkrsCljzhG117&location=kaifeng&language=zh-Hans&unit=c')
    j1 = ujson.loads(result1.text)
    
    result2 = urequests.get(
        'https://api.seniverse.com/v3/weather/now.json?key=SXMzpkrsCljzhG117&location=huizhou&language=zh-Hans&unit=c')
    j2 = ujson.loads(result2.text)    
    
    result3 = urequests.get(
        'https://api.seniverse.com/v3/weather/now.json?key=SXMzpkrsCljzhG117&location=luoyang&language=zh-Hans&unit=c')
    j3 = ujson.loads(result3.text)
    i = 0
    while True:
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


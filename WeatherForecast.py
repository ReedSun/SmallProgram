# -*- coding: utf-8 -*-

import os
import requests
from xml.parsers.expat import ParserCreate


class WeatherSaxHandler(object):
    def __init__(self):
        self.db = []

    def start_element(self, name, attrs):
        self.db.append(name)


    def end_element(self, name):
        pass

    def char_data(self, text):
        self.db.append(text)


def parse_weather(xml):
    handler = WeatherSaxHandler()
    parser = ParserCreate()
    parser.StartElementHandler = handler.start_element
    parser.EndElementHandler = handler.end_element
    parser.CharacterDataHandler = handler.char_data
    parser.Parse(xml)
    return handler.db


def check(place):
    gb2312_place = str(place.encode("GB2312"))[2:-1]
    right_place = gb2312_place.replace("\\x", "%" )
    ri = {"0": "今日", "1": "明日", "2": "后日"}

    for x in range(3):
        resq_place = requests.get("http://php.weather.sina.com.cn/xml.php?city="+right_place+"&password=DJOYnieT8234jlsK&day="+str(x))
        resq_place.encoding = "UTF-8"
        xml_place = resq_place.text
        result = parse_weather(xml_place)
        print("\n------------------------------%s(%s)天气预报------------------------------" % (ri[str(x)], result[result.index("savedate_weather")+1]))
        print("城市：%s" % result[result.index("city")+1])

        if result[result.index("status1")+1] == result[result.index("status2")+1]:
            print("天气：%s 最高温度：%s℃ 最低温度:%s℃ 风向：%s 风级：%s级\n" % (result[result.index("status1")+1], result[result.index("temperature1")+1], result[result.index("temperature2")+1], result[result.index("direction1")+1], result[result.index("power1")+1]))
        else:
            print("天气：%s转%s 最高温度：%s℃ 最低温度:%s℃ 风向：%s 风级：%s级\n" % (result[result.index("status1")+1], result[result.index("status2")+1], result[result.index("temperature1")+1], result[result.index("temperature2")+1], result[result.index("direction1")+1], result[result.index("power1")+1]))

        print("体感度指数：%s   %s" % (result[result.index("ssd_l")+1], result[result.index("ssd_s")+1]))
        print("紫外线指数：%s   %s" % (result[result.index("zwx_l")+1], result[result.index("zwx_s")+1]))
        print("空调指数：%s   %s" % (result[result.index("ktk_l")+1], result[result.index("ktk_s")+1]))
        print("污染指数：%s   %s" % (result[result.index("pollution_l")+1], result[result.index("pollution_s")+1]))
        if result[result.index("xcz_l")+1] != "暂无":
            print("洗车指数：%s   %s" % (result[result.index("xcz_l")+1], result[result.index("xcz_s")+1]))
        print("穿衣指数：%s   %s" % (result[result.index("chy_l")+1], result[result.index("chy_shuoming")+1]))
        print("感冒指数：%s   %s" % (result[result.index("gm_l")+1], result[result.index("gm_s")+1]))
        print("运动指数：%s   %s" % (result[result.index("yd_l")+1], result[result.index("yd_s")+1]))



try:
    city = input("请输入你要查询的城市")
    check(city)
except:
    print("没有找到您输入的城市")
finally:
    os.system("pause")
    


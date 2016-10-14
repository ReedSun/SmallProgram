# -*- coding: utf-8 -*-

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
    ri = {"1": "今日", "2": "明日", "3": "后日"}
    for x in range(1, 4):
        resq_place = requests.get("http://php.weather.sina.com.cn/xml.php?city="+right_place+"&password=DJOYnieT8234jlsK&day="+str(x))
        resq_place.encoding = "UTF-8"
        xml_place = resq_place.text
        result = parse_weather(xml_place)
        print("\n------------------------------%s(%s)天气预报------------------------------" % (ri[str(x)], result[139]))
        print("城市：%s" % result[5])
        print("天气：%s转%s 最高温度：%s℃ 最低温度:%s℃ 风向：%s 风级：%s级\n" % (result[8], result[11], result[32], result[35], result[20], result[26]))
        print("体感度指数：%s   %s" % (result[85], result[112]))
        print("紫外线指数：%s   %s" % (result[82], result[109]))
        print("空调指数：%s   %s" % (result[97], result[115]))
        print("污染指数：%s   %s" % (result[79], result[106]))
        print("洗车指数：%s   %s" % (result[100], result[118]))
        print("穿衣指数：%s   %s" % (result[94], result[76]))
        print("感冒指数：%s   %s" % (result[124], result[127]))
        print("运动指数：%s   %s" % (result[133], result[136]))


try:
    input

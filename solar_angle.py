from datetime import datetime
from math import sin, asin, cos, acos, tan, radians, pi, degrees

# 对a进行处理
def judge_a(Hour, snoon, a):

    if(a >= 0 and a <= pi and Hour < snoon):
        a = pi - a
    elif(a >= 0 and a <= pi and Hour == snoon):
        pass
    elif(a >= 0 and a <= pi and Hour > snoon):
        a = pi + a

    return a

# 显示hh:mm日出日落时间
def display_sunrise_time(snoon, ha):

    sunrise = snoon - ha/15
    sunset = snoon + ha/15
    
    hour_0 = int(sunrise)
    minute_0 = int(round(sunrise - hour_0, 6)*60)
    hour_1 = int(sunset)
    minute_1 = int(round(sunset - hour_1, 6)*60)       

    return f"日出时间: {hour_0:02}:{minute_0:02}，日落时间: {hour_1:02}:{minute_1:02}"

# 显示得到的结果
def display_output(string, time, h0, a):
    
    if(degrees(h0) <= 0):

        print(f"输入time: {time.hour:02}:{time.minute:02}，太阳未升起或已落下，不计算太阳高度角和方位角，{string}\n")
    elif(degrees(h0) > 0):
        h0 = round(degrees(h0), 2)
        a = round(degrees(a), 2)
        
        print(f"输入time: {time.hour:02}:{time.minute:02}，太阳高度角：{h0}°，太阳方位角：{a}°，{string}\n")

# 主函数
def get_h0_a(lon, lat, date, time, timezone):
    """计算太阳高度角、方位角和日出日落时间

    Arguments:
        lon {float} -- [经度(度)，分秒转换成小数，东经为正]

        lat {float} -- [纬度(度)，北纬为正]

        date {string} -- [日期，年/月/日，年4位，月日2位]

        time {string} -- [当地时间，时:分，各2位]

        timezone {float} -- [当地时区，如北京为8.0，洛杉矶-7.0]

    Returns:
        包含time, h0, a, sunrise和sunset的字符串

        time {string} -- [输入的时间]

        h0 {float} -- [太阳高度角(度)]

        a {float} -- [太阳方位角(度)]

        sunrise, sunset -- [日出日落时间]
    """
    # 第零步：将日期转化为日期序数，1,2,3......，365；将时间转化为24小时制浮点数，如18:30转为18.5
    date = datetime.strptime(date, '%Y/%m/%d')
    Dn = int(date.strftime('%j'))
    time = datetime.strptime(time, '%H:%M')
    Hour = time.hour + time.minute/60.0

    # 第一步：计算太阳倾角(太阳直射点纬度)decl和equation of time
    gamma = 2*pi*(Dn - 1 + (Hour - 12)/24)/365

    # 计算eqtime
    eqtime = 229.18*(0.000075 + 0.001868*cos(gamma) - 0.032077*sin(gamma) - 0.014615*cos(2*gamma) - 0.040849*sin(2*gamma))

    # 计算decl
    f1 = 0.006918
    f2 = 0.399912*cos(gamma)
    f3 = 0.070257*sin(gamma)
    f4 = 0.006758*cos(gamma*2)
    f5 = 0.000907*sin(gamma*2)
    f6 = 0.002697*cos(gamma*3)
    f7 = 0.001480*sin(gamma*3)
    decl = f1 - f2 + f3 - f4 + f5 - f6 + f7

    # 第二步：计算太阳时角和方位角180度时的时间
    time_offset = eqtime + 4*lon - 60*timezone
    tst = Hour*60 + time_offset
    ha = (tst/4 - 180)
    snoon = (720 - 4*lon - eqtime)/60 + timezone

    # 第三步：计算太阳高度角
    lat = radians(lat)
    ha = radians(ha)  # 注意转为弧度
    h0 = asin(sin(lat)*sin(decl) + cos(lat)*cos(decl)*cos(ha))

    # 第四步：计算太阳方位角
    a = acos((sin(lat)*sin(h0) - sin(decl))/(cos(lat)*cos(h0)))
    a = judge_a(Hour, snoon, a)

    # 第五步：计算日出日落时间
    zenith = radians(90.833)
    ha = acos(cos(zenith)/(cos(lat)*cos(decl)) - tan(lat)*tan(decl))
    ha = degrees(ha)  # 注意转为角度
    string = display_sunrise_time(snoon, ha)
        
    display_output(string, time, h0, a)   


get_h0_a(116.3, 39.9, '2023/06/02', '04:00', 8.0) # 北京04时

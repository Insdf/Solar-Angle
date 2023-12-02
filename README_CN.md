# 公式

在这里：

[General Solar Position Calculations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF)

只提一下需要注意的地方。

高度角公式：

$$
\cos \phi = \sin (lat) \sin (decl) + \cos (lat) \cos (decl) \cos (ha)
$$

文件中的cost应该是打错了。

这里 $\phi$ 是天顶角，和高度角 $\alpha$ 的关系是

$$
\phi = \frac \pi 2 - \alpha
$$

故有

$$
\cos \phi = \sin \alpha
$$

$$
\sin \phi = \cos \alpha
$$

方位角公式

$$
\cos (180 - \theta) = - \frac {\sin(lat) \cos(\phi) - \sin(decl)} {\cos(lat) \sin(\phi)}
$$

由前面 $\alpha$ 和 $\phi$ 的关系，以及 $\cos(180-\theta)=-\cos(\theta)$ 可知

$$
\cos (\theta) = \frac {\sin(lat) \sin(\alpha) - \sin(decl)} {\cos(lat) \cos(\alpha)}
$$

日出日落的计算文件中只有公式，可以到

[Solar Calculation Details](https://gml.noaa.gov/grad/solcalc/calcdetails.html)

下载表格文件看详细过程。

# 代码说明

计算高度角h0：

`h0 = asin(sin(lat)*sin(decl) + cos(lat)*cos(decl)*cos(ha))`

当h0 < 0时，太阳未升起或已落下，不计算高度角和方位角。

计算方位角，a为方位角，其余对应上面的公式：

`a = acos((sin(lat)*sin(h0) - sin(decl))/(cos(lat)*cos(h0)))`

将某地某天方位角a的数值从6:00到18:00列表，经测试若要将a转换为以北为零位的方位角，当 $0<=a<=\pi$ 且时间早于正午，有 $a=\pi-a$; 当 $0<=a<=\pi$ 且时间晚于正午，有 $a=\pi+a$.

转换成代码，Hour为小时浮点数，如18:30对应18.5，snoon为方位角180度(正午)时对应的当地时间：

```python
def judge_a(Hour, snoon, a):
    if(a >= 0 and a <= pi and Hour < snoon):
        a = pi - a
    elif(a >= 0 and a <= pi and Hour == snoon):
        pass
    elif(a >= 0 and a <= pi and Hour > snoon):
        a = pi + a

    return a
```

计算日出日落，首先计算时角ha并转为角度：

```python
zenith = radians(90.833)
ha = acos(cos(zenith)/(cos(lat)*cos(decl)) - tan(lat)*tan(decl))
ha = degrees(ha)
```

ha/15就是日出到正午或正午到日落的时间间隔，用正午时间snoon加减时间间隔就得到日出日落时间：

```python
snoon = (720 - 4*lon - eqtime)/60 + timezone

sunrise = snoon - ha/15
sunset = snoon + ha/15
```

得到的是小时浮点数，比如18.5应是18:30，将其转为hh:mm的格式：

```python
hour_0 = int(sunrise)
minute_0 = int(round(sunrise - hour_0, 6)*60)
hour_1 = int(sunset)
minute_1 = int(round(sunset - hour_1, 6)*60) 

return f"日出时间: {hour_0:02}:{minute_0:02}，日落时间: {hour_1:02}:{minute_1:02}"
```

另外增加了将日期转换为年积日、时间转化为浮点数，只需要输入年月日及时间，如2023/03/02、18:25就可以了：

```python
date = datetime.strptime(date, '%Y/%m/%d')
Dn = int(date.strftime('%j'))
time = datetime.strptime(time, '%H:%M')
Hour = time.hour + time.minute/60.0
```

# 使用

代码运行大概要求Python 3.7+，因为代码中多处使用了f"{}"，字符串中使用变量名，老版本需要将这些地方改掉。

调用get_h0_a(lon, lat, date, time, timezone)

lon {float} -- 经度(度)，分秒转换成小数，东经为正

lat {float} -- 纬度(度)，北纬为正

date {string} -- 日期，年/月/日，年4位，月日2位

time {string} -- 当地时间，时:分，各2位

timezone {float} -- 当地时区，如北京为8.0，洛杉矶-7.0

测试2023年6月2日，北京和洛杉矶不同时段：

```python
get_h0_a(116.3, 39.9, '2023/06/02', '04:00', 8.0) # 北京04时
get_h0_a(116.3, 39.9, '2023/06/02', '05:00', 8.0) # 北京05时
get_h0_a(-118, 34, '2023/06/02', '18:00', -7.0) # 洛杉矶18时
get_h0_a(-118, 34, '2023/06/02', '19:00', -7.0) # 洛杉矶19时


# 输入time: 04:00，太阳未升起或已落下，不计算太阳高度角和方位角，日出时间: 04:48，日落时间: 19:36

# 输入time: 05:00，太阳高度角：1.15°，太阳方位角：61.79°，日出时间: 04:48，日落时间: 19:36

# 输入time: 18:00，太阳高度角：22.06°，太阳方位角：282.52°，日出时间: 05:41，日落时间: 19:57

# 输入time: 19:00，太阳高度角：10.13°，太阳方位角：289.94°，日出时间: 05:41，日落时间: 19:57
```

# 协议

此项目使用 [MIT-0](/LICENSE) 协议，所用源代码的版权声明在此文件中：[NOTICE](/NOTICE)。

# 参考

[Converting time to a float](https://stackoverflow.com/questions/47043841/converting-time-to-a-float)

[in python how do I convert a single digit number into a double digits string?](https://stackoverflow.com/questions/3505831/in-python-how-do-i-convert-a-single-digit-number-into-a-double-digits-string)

[利用python根据经纬度、时间计算太阳高度角](https://zhuanlan.zhihu.com/p/431359778)

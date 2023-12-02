from datetime import datetime
from math import sin, asin, cos, acos, tan, radians, pi, degrees

# Handle a
def judge_a(Hour, snoon, a):

    if(a >= 0 and a <= pi and Hour < snoon):
        a = pi - a
    elif(a >= 0 and a <= pi and Hour == snoon):
        pass
    elif(a >= 0 and a <= pi and Hour > snoon):
        a = pi + a

    return a

# Displays hh:mm sunrise and sunset times
def display_sunrise_time(snoon, ha):

    sunrise = snoon - ha/15
    sunset = snoon + ha/15
    
    hour_0 = int(sunrise)
    minute_0 = int(round(sunrise - hour_0, 6)*60)
    hour_1 = int(sunset)
    minute_1 = int(round(sunset - hour_1, 6)*60)  

    return f"Sunrise time: {hour_0:02}:{minute_0:02}, Sunset time: {hour_1:02}:{minute_1:02}"
    
# Display the output
def display_output(string, time, h0, a):

    if(degrees(h0) <= 0):

        print(f"Input time: {time.hour:02}:{time.minute:02}, the Sun has not yet risen or has already set, Solar altitude and azimuth angle are not calculated, {string}\n")
    elif(degrees(h0) > 0):
        h0 = round(degrees(h0), 2)
        a = round(degrees(a), 2)

        print(f"Input time: {time.hour:02}:{time.minute:02}, Solar altitude angle: {h0}°, Solar azimuth angle: {a}°, {string}\n")

# main function
def get_h0_a(lon, lat, date, time, timezone):
    """Calculate solar altitude, azimuth angle and sunrise and sunset times

    Arguments:
        lon {float} -- [Longitude (degrees), minutes and seconds need to be converted to decimals, positive for east lontitude]

        lat {float} -- [Latitude (degrees), positive for north latitude]

        date {string} -- [Date, year/month/day, 4 digits for year, 2 digits for month and day]

        time {string} -- [Local time, hour:minute, 2 digits]

        timezone {float} -- [Local timezone, Beijing is 8.0, Los Angeles is -7.0]

    Returns:
        A string containing time, h0, a, sunrise, and sunset
        
        time {string} -- [Entered time]

        h0 {float} -- [Solar altitude angle (degrees)]

        a {float} -- [Solar azimuth angle (degrees)]

        sunrise, sunset -- [Sunrise and Sunset time]
    """
    # Zero: Convert dates to the day of year, 1,2,3...,365; convert time to 24-hour floating-point numbers, such as 18:30 to 18.5
    date = datetime.strptime(date, '%Y/%m/%d')
    Dn = int(date.strftime('%j'))
    time = datetime.strptime(time, '%H:%M')
    Hour = time.hour + time.minute/60.0

    # First: calculate current sun declination decl and equation of time
    gamma = 2*pi*(Dn - 1 + (Hour - 12)/24)/365

    # Calculate eqtime
    eqtime = 229.18*(0.000075 + 0.001868*cos(gamma) - 0.032077*sin(gamma) - 0.014615*cos(2*gamma) - 0.040849*sin(2*gamma))

    # Calculate decl
    f1 = 0.006918
    f2 = 0.399912*cos(gamma)
    f3 = 0.070257*sin(gamma)
    f4 = 0.006758*cos(gamma*2)
    f5 = 0.000907*sin(gamma*2)
    f6 = 0.002697*cos(gamma*3)
    f7 = 0.001480*sin(gamma*3)
    decl = f1 - f2 + f3 - f4 + f5 - f6 + f7

    # Second: calculate Solar hour angle and time when azimuth is 180 degree
    time_offset = eqtime + 4*lon - 60*timezone
    tst = Hour*60 + time_offset
    ha = (tst/4 - 180)
    snoon = (720 - 4*lon - eqtime)/60 + timezone

    # Third: calculate Solar altitude angle
    lat = radians(lat)
    ha = radians(ha)  # convet to radian
    h0 = asin(sin(lat)*sin(decl) + cos(lat)*cos(decl)*cos(ha))

    # Forth: Calculate solar azimuth angle
    a = acos((sin(lat)*sin(h0) - sin(decl))/(cos(lat)*cos(h0)))
    a = judge_a(Hour, snoon, a)

    # Fifth: calculate Sunrise and Sunset time
    zenith = radians(90.833)
    ha = acos(cos(zenith)/(cos(lat)*cos(decl)) - tan(lat)*tan(decl))
    ha = degrees(ha)  # convert to degree
    string = display_sunrise_time(snoon, ha)
        
    display_output(string, time, h0, a)  


get_h0_a(116.3, 39.9, '2023/06/02', '04:00', 8.0) # 04:00 at Beijing

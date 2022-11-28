# coding: utf8


import ephem
import datetime

import pytz

from datetime import date, timedelta



def sun_rise():

    # pass
    now = datetime.datetime.now() #get current time

    Boston = ephem.Observer()
    Boston.pressure = 1010 # millibar
    Boston.temp = 25 # deg. Celcius
    Boston.horizon = 0
    Boston.lat = '42.3462'
    Boston.lon = '-71.0978'
    Boston.elevation = 3 # meters
    Boston.date = now

    sun = ephem.Sun()

    # print(Boston.next_rising(sun))
    # print(ephem.localtime(Boston.next_rising(sun)))

    str_out = ''
    str_out += "Next sunrise in Boston will be: " + \
               str(ephem.localtime(Boston.next_rising(sun))) + "\n"
    str_out += "Next sunset in Boston will be: " + \
               str(ephem.localtime(Boston.next_setting(sun)))

    # print(str_out)

    return str_out



def moon_rise_set():

    now = datetime.datetime.now() #get current local time
    # print now
    now = ephem.now() # current UTC date and time
    # print now

    str_out2 = "Kharkov current time  " + show_time(ephem.now())


    place = ephem.Observer() # Kharkov
    # place.pressure = 1010 # millibar
    # place.temp = 25 # deg. Celcius
    place.horizon = 0
    place.lat = '50.0'
    place.lon = '36.15'
    # place.elevation = 3 # meters
    place.date = now

    sun = ephem.Sun()
    moon = ephem.Moon()


    str_out2 += "previous_rising Sun  :" + show_time(place.previous_rising(sun))
    str_out2 += "next_setting Sun     :" + show_time(place.next_setting(sun))
    str_out2 += "previous_rising Moon :" + show_time(place.previous_rising(moon))
    str_out2 += "next_setting Moon    :" + show_time(place.next_setting(moon))
    str_out2 += "\n"
    str_out2 += "previous_rising Sun  :" + show_time(place.previous_rising(sun))
    str_out2 += "previous_setting Sun :" + show_time(place.previous_setting(sun))
    str_out2 += "next_rising Sun      :" + show_time(place.next_rising(sun))
    str_out2 += "next_setting Sun     :" + show_time(place.next_setting(sun))


    # print str_out2
    return str_out2



def show_time(time):

    out_str_time = ""
    out_str_time += "UTC:"
    out_str_time += str(time)
    out_str_time += " {" + str(ephem.localtime(time))[:19] + "}\n"

    return out_str_time



# >>> atlanta.lat, atlanta.lon = '33.8', '-84.4'
# >>> atlanta.date = '2009/09/06 17:00' # noon EST
# >>> print(atlanta.previous_rising(ephem.Sun()))
# 2009/9/6 11:14:57
# >>> print(atlanta.next_setting(ephem.Sun()))
# 2009/9/6 23:56:10
# >>> print(atlanta.previous_rising(ephem.Moon()))
# 2009/9/6 00:16:32
# >>> print(atlanta.next_setting(ephem.Moon()))
# 2009/9/7 14:05:29



def prev_weekday(adate):
    adate -= timedelta(days=1)
    while adate.weekday() != 0: # Mon-Fri are 0-4
        adate -= timedelta(days=1)
    return adate







if __name__ == '__main__':

    # sun_rise()


    # a_date = ephem.now() # current UTC date and time
    # print show_time(ephem.now())

    # print "UTC:", a_date # note that fractional part is missing from seconds
    # print "localtime:", ephem.localtime(a_date)

    # print moon_rise_set()



    timezone='UTC'
    tz = pytz.timezone(timezone)
    print tz

    d = ephem.Date(str('2015/5/18 3:00:00'))
    equinox1 = d.datetime() + tz.utcoffset(d.datetime())

    print "d=", d
    print "tz.utcoffset(d.datetime())",tz.utcoffset(d.datetime())
    print "equinox1=", equinox1


    print "date.today()=", date.today()

    print "@@", date.today().weekday()

    print "prev_weekday=", prev_weekday(date.today())
    # print datetime.date(2012, 8, 20)
    prev_weekday(date(2012, 8, 20))



    cet = pytz.timezone('CET')

    dt = datetime.datetime(2010, 10, 21, 2, 12, 30)
    offset = cet.utcoffset(dt)
    print offset

    dt = datetime.datetime.utcfromtimestamp(1288483950)
    dt = pytz.utc.localize(dt)
    offset = dt.astimezone(cet).utcoffset()
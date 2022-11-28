# coding: utf8
#!/usr/bin/python


import datetime
import itertools
import math
import pprint
import time

import ephem
# import mysite.astro_routines.geo_preload as geopr
from ephem import *

# zodiac = 'AR TA GE CN LE VI LI SC SG CP AQ PI'.split()
# zodiac = u'Овен Телец Близнецы Рак Лев Дева Весы Скорпион Стрелец Козерог Водолей Рыбы'.split()
zodiac = u'Овн Тлц Блз Рак Лев Дев Вес Скп Стр Коз Вод Рыб'.split()


def format_zodiacal_longitude(longitude):
    """
    :param longitude:
    :return: Format longitude in zodiacal form (like '00AR00') and return as a string."
    """
    # print longitude
    l = math.degrees(longitude.norm)
    degrees = int(l % 30)
    sign = zodiac[int(l / 30)]
    minutes = int(round((l % 1) * 60))
    # return u'{0:02}{1}{2:02}'.format(degrees, sign, minutes)
    # return u'{0:02}{1}'.format(degrees, sign)
    return u'{1}{0:02}'.format(degrees, sign)


def format_angle_as_time(a):
    """Format angle as hours:minutes:seconds and return it as a string."""
    a = math.degrees(a) / 15.0
    hours = int(a)
    minutes = int((a % 1) * 60)
    seconds = int(((a * 60) % 1) * 60)
    return '{0:02}:{1:02}:{2:02}'.format(hours, minutes, seconds)


def print_ephemeris_for_date(date, bodies):
    date = Date(date)
    print(datetime.datetime(*date.tuple()[:3]).strftime('%A')[:2],)
    print('{0:02}'.format(date.tuple()[2]),)
    greenwich = Observer()
    greenwich.date = date
    print(format_angle_as_time(greenwich.sidereal_time()),)
    for b in bodies:
        b.compute(date, date)
        print(format_zodiacal_longitude(Ecliptic(b).long),)
    print


def print_ephemeris_for_month(year, month, bodies):
    print()
    print((datetime.date(year, month, 1).strftime('%B %Y').upper().center(14 + len(bodies) * 7)))
    print()
    print('DATE  SID.TIME',)
    for b in bodies:
        print('{0: <6}'.format(b.name[:6].upper()),)
    print()
    for day in itertools.count(1):
        try:
            datetuple = (year, month, day)
            datetime.date(*datetuple)
            print_ephemeris_for_date(datetuple, bodies)
        except ValueError:
            break


def print_ephemeris_for_year(year):
    bodies = [Sun(), Moon(), Mercury(), Venus(), Mars(), Jupiter(),
              Saturn(), Uranus(), Neptune(), Pluto()]
    for month in xrange(1, 13):
        print_ephemeris_for_month(year, month, bodies)
        print()


start_date = ephem.Date('2015/10/21 15:00')
stop_date  = ephem.Date('2016/02/21 15:00')

# cur_date = start_date
# while stop_date >= cur_date:
#
#     # print cur_date
#     body = ephem.Moon(cur_date)
#     body.compute(cur_date, cur_date)
#
#     str_pr = str(body) + " "
#     str_pr += "deg={:>15}".format(deg(body.ra)) + " - "
#     str_pr += "deg={:>15}".format(deg(body.a_ra)) + " - "
#     str_pr += "deg={:>15}".format(deg(body.g_ra)) + " "
#     # str_pr += "deg={:7.2f}".format(deg(deg(body.ra)))+ ""
#
#     str_pr += "deg={:>15}".format(deg(body.dec)) + " + "
#     str_pr += "deg={:>15}".format(deg(body.a_dec)) + " + "
#     str_pr += "deg={:>15}".format(deg(body.g_dec)) + " "
#
#     str_pr += ephem.constellation(body)[0]
#     str_pr += " ||| "
#     str_pr += str(Ecliptic(body, epoch='2015').long)
#     str_pr += " ??? "
#     str_pr += str(Ecliptic(body, epoch='1950').long)
#     print str_pr
#
#     # print format_zodiacal_longitude(Ecliptic(body, epoch='2000').long)
#
#     cur_date = ephem.Date(cur_date + 1.5)
#     # ===============================================


def get_zodiac(in_date_utc, body):

    """
    :param in_date_utc:
    :param body:
    :return: Format longitude in zodiacal form (like '00AR00') and return as a string.
    """

    if not body:
        return

    #####################################################################
    curr_date = ephem.Date(in_date_utc)

    ecl = ephem.Ecliptic(body, epoch=in_date_utc)
    # str_out += "\n" + str(ecl.epoch)
    # str_out += " ecl2 =" + str(deg(ecl.lon)) + " ; " + str(deg(ecl.lat))
    # str_out += " [{:7.3f}".format(ecl.lon * 180 / 3.14) + ";"
    # str_out += " {:7.3f}]".format(ecl.lat * 180 / 3.14)
    # ---------------------------------------------------------------------

    ecl_dict = {}
    ecl_dict["date_utc"] = curr_date
    ecl_dict["ecl.lon"] = ecl.lon * 180 / 3.14
    ecl_dict["ecl.lat"] = ecl.lat * 180 / 3.14

    ecl_dict["zod_lat"] = format_zodiacal_longitude(ecl.long)
    # =========================================================================

    return ecl_dict


def get_zodiac_local12place(in_aware_loc, in_unaware_utc, in_str_body, place):
    """
    Input: local unaware time and place, "Moon", "Sun"
    Returns coord for local time and place
    """
    tz_name, coord = geopr.set_tz(place)
    # print "place=", place, coord, tz_name

    body = None
    if in_str_body == "Moon":
        body = ephem.Moon(in_unaware_utc)
    elif in_str_body == "Sun":
        body = ephem.Sun(in_unaware_utc)

    ecl_dict_ext = get_zodiac(in_unaware_utc, body)
    # =========================================================================

    ecl_dict_ext.update({"date_utc": in_unaware_utc})
    ecl_dict_ext.update({"aware_loc": in_aware_loc})

    return ecl_dict_ext


def getInfo(body):

    str_out = "\n"
    str_out += str(body)
    str_out += " " + ephem.constellation(body)[0]
    # -----------------------------------------------------


    ###########################################################################
    str_out += "\n"
    str_out += " body.ra =" + str(deg(body.ra)) + ";" + str(deg(body.dec))
    str_out += " [{:7.3f}".format(body.ra * 180 / 3.14) + ";"
    str_out += " {:7.3f}]".format(body.dec * 180 / 3.14)
    # ---------------------------------------------------------------------


    ma = ephem.Equatorial(body.ra, body.dec)
    me = ephem.Ecliptic(ma)
    # str_out += "\n" + str(ma.epoch)

    # str_out += " Equatorial ma.ra=" + str(ma.ra) + "=" + str(ma.dec)
    #
    # str_out += " me.lon =" + str(deg(me.lon))
    # str_out += " & deg={:7.3f}".format(me.lon * 180 / 3.14) + " - "



    ###########################################################################
    ecl = ephem.Ecliptic(body, epoch=cur_date)

    str_out += "\n" + str(ecl.epoch)
    str_out += " ecl =" + str(deg(ecl.lon)) + " ; " + str(deg(ecl.lat))
    str_out += " [{:7.3f}".format(ecl.lon * 180 / 3.14) + ";"
    str_out += " {:7.3f}]".format(ecl.lat * 180 / 3.14)
    # ---------------------------------------------------------------------


    ###########################################################################
    ecl = ephem.Ecliptic(body, epoch='2000')

    str_out += "\n" + str(ecl.epoch)
    str_out += " ecl2 =" + str(deg(ecl.lon)) + " ; " + str(deg(ecl.lat))
    str_out += " [{:7.3f}".format(ecl.lon * 180 / 3.14) + ";"
    str_out += " {:7.3f}]".format(ecl.lat * 180 / 3.14)
    # ---------------------------------------------------------------------


    # body.compute(cur_date, cur_date)
    str_out += "\n"
    str_out += " ecl3 =" + format_zodiacal_longitude(Ecliptic(body, epoch='2000').long)

    return str_out





if __name__ == "__main__":


    deg = ephem.degrees

    cur_date = start_date
    cur_date = ephem.Date(datetime.datetime.now())
    # while stop_date >= cur_date:
    while True:

        cur_date = datetime.datetime.now()
        # print cur_date

        body = ephem.Moon(cur_date)
        # ---------------------------------------------------------------------

        pprint.pprint(get_zodiac(cur_date, body))

        place = "Kiev"
        pprint.pprint(get_zodiac_local12place(cur_date, body, place))


        # str_out = ""
        # str_out += getInfo(body)
        #
        #
        # body = ephem.Sun(cur_date)
        # # body.compute(cur_date, cur_date)
        #
        # str_out += getInfo(body)
        #
        # print str_out

        time.sleep(1)


        # cur_date = ephem.Date(cur_date + 0.5)
        # ===============================================


print("=============== END ====================")


# http://lyna.info/


# http://time.unitarium.com/moon/where.html
# http://www.satellite-calculations.com/Satellite/suncalc.htm
# http://www.moonsystem.to/justnowe.htm

# https://www.calsky.com/cs.cgi




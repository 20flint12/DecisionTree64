from datetime import datetime
import itertools
import math
import pprint

import ephem
import src.ephem_routines.ephem_package.geo_place as geo
'''
Огонь:      Овен, Лев, Стрелец          красным
Земля:      Телец, Дева, Козерог        коричневым
Воздух:     Близнецы, Весы, Водолей     синим
Вода:       Рак, Скорпион, Рыбы         зеленым
'''

zodiac = 'AR TA GE CN LE VI LI SC SG CP AQ PI'.split()
zodiac_full_rus = u'Овен Телец Близнецы Рак Лев Дева Весы Скорпион Стрелец Козерог Водолей Рыбы'.split()
zodiac_full_ukr = u'Овен Телець Близнюки Рак Лев Діва Терези Скорпіон Стрілець Козоріг Водолій Риби'.split()
zodiac_short_rus = u'Овн Тлц Блз Рак Лев Дев Вес Скп Стр Коз Вод Рыб'.split()
zodiac_short_ukr = u'Овн Тлц Блз Рак Лев Дів Тер Скп Стр Коз Вод Риб'.split()

elements_full_ukr = [
    u'Вогонь Tепло Білок',
    u'Земля Xолод Сіль',
    u'Повітря Cвітло Жири',
    u'Вода Вугле- води',
]


def format_zodiacal_longitude(longitude):
    """
    :param longitude:
    :return: Format longitude in zodiacal form (like '00AR00') and return as a string."
    """
    # print("longitude=", longitude, type(longitude))
    long = 0
    if type(longitude) == ephem.Angle:
        long = math.degrees(longitude.norm)
    if type(longitude) == int:
        long = longitude
    if type(longitude) == float:
        long = longitude

    degrees = int(long % 30)
    sign = zodiac_short_ukr[int(long / 30)]
    # minutes = int(round((long % 1) * 60))
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
    print(datetime.datetime(*date.tuple()[:3]).strftime('%A')[:2], )
    print('{0:02}'.format(date.tuple()[2]), )
    greenwich = Observer()
    greenwich.date = date
    print(format_angle_as_time(greenwich.sidereal_time()), )
    for b in bodies:
        b.compute(date, date)
        print(format_zodiacal_longitude(Ecliptic(b).long), )
    print


def print_ephemeris_for_month(year, month, bodies):
    print()
    print((datetime.date(year, month, 1).strftime('%B %Y').upper().center(14 + len(bodies) * 7)))
    print()
    print('DATE  SID.TIME', )
    for b in bodies:
        print('{0: <6}'.format(b.name[:6].upper()), )
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


# cur_date = start_date
# while stop_date >= cur_date:
#
#     # print cur_date
#     body = ephem_routines.Moon(cur_date)
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
#     str_pr += ephem_routines.constellation(body)[0]
#     str_pr += " ||| "
#     str_pr += str(Ecliptic(body, epoch='2015').long)
#     str_pr += " ??? "
#     str_pr += str(Ecliptic(body, epoch='1950').long)
#     print str_pr
#
#     # print format_zodiacal_longitude(Ecliptic(body, epoch='2000').long)
#
#     cur_date = ephem_routines.Date(cur_date + 1.5)
#     # ===============================================


def main_moon_lunation(observer=None):
    """Returns a floating-point number from 0-1. where 0=new, 0.5=full, 1=new"""
    # Ephem stores its date numbers as floating points, which the following uses
    # to conveniently extract the percent time between one new moon and the next
    # This corresponds (somewhat roughly) to the phase of the moon.

    # Use Year, Month, Day as arguments
    observer.unaware_update_utc()  # restore utc from previous calculation
    date = ephem.Date(datetime.date(observer.get_utc))

    nnm = ephem.next_new_moon(date)
    pnm = ephem.previous_new_moon(date)

    lunation = (date - pnm) / (nnm - pnm)

    # Note that there is a ephem.Moon().phase() command, but this returns the
    # percentage of the moon which is illuminated. This is not really what we want.

    return lunation


def main_zodiac_sun_moon(observer=None):
    """
    :param observer:
    :return:
        {'moon_lat': -2.33097500404082,
         'moon_lon': 249.4578276816824,
         'moon_zod': 'Стр09',
         'sun_lat': -0.00010429400758934978,
         'sun_lon': 270.0509101194461,
         'sun_zod': 'Коз00'}
    """
    result_text = ""

    #####################################################################
    observer.unaware_update_utc()  # restore utc from previous calculation
    # print(observer.get_utc)

    body_sun = ephem.Sun(observer.get_place)
    # body_sun.compute(observer.place)
    ecl_sun = ephem.Ecliptic(body_sun, epoch=observer.get_utc)

    body_moon = ephem.Moon(observer.get_place)
    # body_moon.compute(observer.place)
    ecl_moon = ephem.Ecliptic(body_moon, epoch=observer.get_utc)

    result_dict = {}
    result_dict["utc_date"] = observer.get_utc
    result_dict["sun_lon"] = ecl_sun.lon * 180 / 3.14159
    # result_dict["sun_lon"] = ecl_sun.long
    result_dict["sun_lat"] = ecl_sun.lat * 180 / 3.14159
    result_dict["moon_lon"] = ecl_moon.lon * 180 / 3.14159
    # result_dict["moon_lon"] = ecl_moon.long
    result_dict["moon_lat"] = ecl_moon.lat * 180 / 3.14159

    result_dict["sun_dist"] = body_sun.earth_distance
    # result_dict["sun_alt"] = body_sun.alt
    result_dict["moon_dist"] = body_moon.earth_distance
    # result_dict["moon_alt"] = body_moon.alt

    # Format longitude in zodiacal form (like '00AR00') and return as a string.
    result_dict["sun_zod"] = format_zodiacal_longitude(ecl_sun.lon)
    result_dict["sun_constel"] = ephem.constellation(body_sun)
    result_dict["moon_zod"] = format_zodiacal_longitude(ecl_moon.lon)
    result_dict["moon_constel"] = ephem.constellation(body_moon)
    # =========================================================================

    result_text += "\n"
    result_text += "\n" + str(result_dict["sun_zod"])
    result_text += " [{:7.3f},".format(result_dict["sun_lon"]) + " {:7.3f}]".format(result_dict["sun_lat"]) + " sun_zod"
    # result_text += "\n(" + str(deg(ecl_sun.lon)) + ", " + str(deg(ecl_sun.lat)) + ")"

    result_text += "\n" + str(result_dict["moon_zod"])
    result_text += " [{:7.3f},".format(result_dict["moon_lon"]) + " {:7.3f}]".format(
        result_dict["moon_lat"]) + " moon_zod"
    # result_text += "\n(" + str(deg(ecl_moon.lon)) + ", " + str(deg(ecl_moon.lat)) + ")"

    return result_dict, result_text


def main_moon_altitude(observer=None):
    result_text = ""
    result_text += "\n"

    observer.unaware_update_utc()  # restore utc from previous calculation
    moon = ephem.Moon(observer.get_place)
    moon.compute(observer.get_place)
    # ===============================================

    # print(moon.alt, observer.utc)
    # u_alt = ephem.unrefract(observer.place.pressure, observer.place.temperature, sun.alt)
    # print(u_alt)

    result_dict = {}
    result_dict["moon_angle"] = round(float(moon.alt) * 57.2957795, 3)
    del moon

    result_text += "\n" + "moon_angle: " + str(result_dict["moon_angle"])

    return result_dict, result_text


if __name__ == "__main__":
    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # in_unaware_datetime = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    in_unaware_datetime = datetime.today()
    # in_unaware_datetime = datetime.now()

    observer_obj = geo.Observer(geo_name=geo_name, input_unaware_datetime=in_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ###########################################################################

    zodiac_dict, zodiac_text = main_zodiac_sun_moon(observer=observer_obj)
    pprint.pprint(zodiac_dict)
    text += zodiac_text

    alt_dict, alt_text = main_moon_altitude(observer=observer_obj)
    text += alt_text

    print(text)

    # str_out = ""
    # str_out += getInfo(body)
    #
    # body = ephem_routines.Sun(cur_date)
    # # body.compute(cur_date, cur_date)
    #
    # str_out += getInfo(body)
    #
    # print str_out
    # ===============================================

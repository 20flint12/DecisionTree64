
# http://lyna.info/

# http://time.unitarium.com/moon/where.html
# http://www.satellite-calculations.com/Satellite/suncalc.htm
# http://www.moonsystem.to/justnowe.htm

# https://www.calsky.com/cs.cgi


from datetime import datetime
import itertools
import math
import pprint

import ephem
import src.ephem_routines.ephem_package.geo_place as geo


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


def main_zodiac_body(geographical_name, local_unaware_datetime, in_str_body):

    str_head = ""
    observer = geo.Observer(geo_name=geographical_name)
    observer.get_coords_by_name()
    observer.get_tz_by_coord()
    str_head += "geo_name= " + observer.geo_name + "\n[lat=" + str(observer.location.latitude) + " lon=" + str(
        observer.location.longitude) + "]"
    str_head += "\ntimezone= " + observer.timezone_name

    str_head += "\n\n*** unaware -> aware -> utc"
    observer.unaware = local_unaware_datetime
    observer.unaware_to_aware_by_tz()  # aware_datetime
    observer.aware_to_utc()  # utc_datetime
    str_head += "\nuna= " + observer.unaware.strftime(geo.dt_format)
    str_head += "\nawa= " + observer.aware.strftime(geo.dt_format)
    str_head += "\nutc= " + observer.utc.strftime(geo.dt_format)

    body = None
    if in_str_body == "Moon":
        body = ephem.Moon(observer.utc)
    elif in_str_body == "Sun":
        body = ephem.Sun(observer.utc)

    if not body: return

    str_head += "\n\nbody= " + in_str_body
    #####################################################################
    deg = ephem.degrees
    ecl = ephem.Ecliptic(body, epoch=observer.utc)

    ecl_dict = {}
    ecl_dict["aware_loc"] = observer.aware
    ecl_dict["date_utc"] = observer.utc
    ecl_dict["ecl.lon"] = ecl.lon * 180 / 3.14159
    ecl_dict["ecl.lat"] = ecl.lat * 180 / 3.14159

    # Format longitude in zodiacal form (like '00AR00') and return as a string.
    ecl_dict["zod_lat"] = format_zodiacal_longitude(ecl.long)
    '''
    {   'aware_loc': datetime.datetime(2022, 12, 1, 11, 58, 22, 442893, tzinfo=<DstTzInfo 'Europe/Warsaw' CET+1:00:00 STD>),
        'date_utc': datetime.datetime(2022, 12, 1, 10, 58, 22, 442893, tzinfo=<UTC>),
        'ecl.lat': -0.00015073491534261797,
        'ecl.lon': 249.22919614625383,
        'zod_lat': 'Стр09'}'''
    # =========================================================================

    # str_head += "\n" + str(ecl.epoch)
    str_head += "\necl2= " + str(deg(ecl.lon)) + "; " + str(deg(ecl.lat))
    str_head += "\n[{:7.3f}".format(ecl.lon * 180 / 3.14159) + " "
    str_head += "{:7.3f}]".format(ecl.lat * 180 / 3.14159)
    str_head += "\n" + str(ecl_dict["zod_lat"])

    return ecl_dict, str_head


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

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.today()
    # local_unaware_datetime = datetime.now()
    # ###########################################################################

    ecl_dict, str_head = main_zodiac_body(geo_name, local_unaware_datetime, "Sun")
    # pprint.pprint(ecl_dict)
    print(str_head)


    # ---------------------------------------------------------------------
    start_date = ephem.Date('2015/10/21 15:00')
    stop_date = ephem.Date('2016/02/21 15:00')

    cur_date = start_date
    cur_date = ephem.Date(datetime.now())
    # while stop_date >= cur_date:

    cur_date = datetime.now()
    # print cur_date

    # body = ephem.Moon(cur_date)
    # ---------------------------------------------------------------------




    # str_out = ""
    # str_out += getInfo(body)
    #
    #
    # body = ephem_routines.Sun(cur_date)
    # # body.compute(cur_date, cur_date)
    #
    # str_out += getInfo(body)
    #
    # print str_out



    # cur_date = ephem_routines.Date(cur_date + 0.5)
    # ===============================================






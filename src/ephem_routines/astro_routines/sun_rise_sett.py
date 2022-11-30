
from datetime import datetime

import ephem
import geo_preload as geopr
import geo_place as geo


def get_sun_rise_sett(place=None, in_date_utc=None):

    sun = ephem.Sun()
    place.date = in_date_utc
    # ===============================================

    prev_rise = place.previous_rising(sun, use_center=True)
    next_sett = place.next_setting(sun, use_center=True)
    # next_rise = ephem_routines.localtime(place.next_rising(sun))
    # prev_sett = ephem_routines.localtime(place.previous_setting(sun))

    sun_dict_utc = {"day_rise": prev_rise,
                    "day_sett": next_sett}

    # print("noon=", place.date)
    # print("prise=", prev_rise)
    # print("nsett=", next_sett)

    # print("nrise=", next_rise)
    # print("psett=", prev_sett)

    return sun_dict_utc


def get_sun_on_month(place):

    # start_date = datetime.datetime.now() #get current time
    # start_date = ephem_routines.Date(datetime.date(2015,4,1))
    # start_date = ephem_routines.Date('2015/4/27 12:00')

    start_date_loc = datetime.datetime(2015, 4, 29, 12)
    start_date_loc = datetime.date.today()  # get current time

    # Correct to nearest Monday
    start_date_mon = _prev_weekday(start_date_loc, 6)
    stop_date_loc = start_date_mon + datetime.timedelta(days=35)

    start_date_eph = ephem.Date(start_date_mon)
    stop_date_eph = ephem.Date(stop_date_loc)


    tz_name, coord = geopr.set_tz(place)
    print("place=", place, coord, tz_name)

    place = _set_Observer(coord)
    sun = ephem.Sun()

    total_list = []
    str_out2 = ""

    new_rise = start_date_eph

    i = 0
    while stop_date_eph >= new_rise:

        day_rise = place.next_rising(sun)
        place.date = day_rise
        day_sett = place.next_setting(sun)
        place.date = day_sett
        new_rise = place.next_rising(sun)

        # ===============================================
        str_out2 += "rising Sun  :" + _print_UTC_time(day_rise)
        str_out2 += "setting Sun :" + _print_UTC_time(day_sett)
        str_out2 += "\n"

        i += 1
        sun_dict = {}
        sun_dict["id"] = i
        sun_dict["day_rise"] = day_rise
        sun_dict["str_day_rise"] = _print_UTC_time(day_rise)
        sun_dict["day_sett"] = day_sett
        sun_dict["str_day_sett"] = _print_UTC_time(day_sett)

        total_list.append(sun_dict)

    # print str_out2
    return total_list


def _prev_weekday(adate, wd): # 6 - sunday
    # Find previous weekday
    while adate.weekday() != wd: # Mon-Fri are 0-4
        adate -= datetime.timedelta(days=1)
    return adate


def _print_UTC_time(time):

    out_str_time = ""
    out_str_time += "UTC:"
    out_str_time += str(time)
    out_str_time += " {" + str(ephem.localtime(time))[:19] + "}"

    return out_str_time


if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'
    # ###########################################################################

    observer = geo.Observer(geo_name=geo_name)
    observer.get_coords_by_name()
    print("geo_name=", observer.geo_name, "[lat=", observer.location.latitude, "lon=", observer.location.longitude, "]")
    observer.get_tz_by_coord()
    print("timezone=", observer.timezone_name)
    # print(observer.place, "\n")

    print("\n*** unaware -> aware12 -> utc")
    # observer.unaware = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)    # "%Y-%m-%d %H:%M:%S"
    observer.unaware = datetime.today()
    observer.aware12_to_utc()       # utc_datetime
    print("una=", observer.unaware.strftime(geo.dt_format))
    print("utc=", observer.utc.strftime(geo.dt_format))

    print("\n*** get_sun_rise_sett(observer.utc)")
    sun_dict = get_sun_rise_sett(place=observer.place, in_date_utc=observer.utc)
    day_rise = observer.dt_utc_to_aware_by_tz((sun_dict["day_rise"].datetime()))
    day_sett = observer.dt_utc_to_aware_by_tz((sun_dict["day_sett"].datetime()))
    print("day_rise=", day_rise.strftime(geo.dt_format))
    print("day_sett=", day_sett.strftime(geo.dt_format))


    # out_list = get_sun_on_month(cur_place)
    # for d in out_list:
    #     for k in sorted(d):
    #         print(k, d[k])
    #     # print sorted(item),item

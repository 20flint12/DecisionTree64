
from datetime import datetime

import ephem
import src.ephem_routines.ephem_package.geo_place as geo


def get_sun_rise_sett(place=None, in_date_utc=None):

    sun = ephem.Sun()
    place.date = in_date_utc
    # ===============================================

    prev_rise = place.previous_rising(sun, use_center=False)
    next_sett = place.next_setting(sun, use_center=False)

    sun_dict_utc = {"sun_rise": prev_rise,
                    "sun_sett": next_sett}

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


def main_sun_rise_sett(observer=None):

    result_text = ""
    result_text += "\n"

    result_dict = get_sun_rise_sett(place=observer.place, in_date_utc=observer.utc12)
    day_rise = observer.dt_utc_to_aware_by_tz((result_dict["sun_rise"].datetime()))
    day_sett = observer.dt_utc_to_aware_by_tz((result_dict["sun_sett"].datetime()))
    result_text += "\n" + day_rise.strftime(geo.dt_format) + " sun_rise"
    result_text += "\n" + day_sett.strftime(geo.dt_format) + " sun_sett"

    return result_dict, result_text


if __name__ == '__main__':

    geo_name = 'Mragowo'
    # geo_name = 'Boston'
    # geo_name = 'Kharkiv'

    # local_unaware_datetime = datetime.strptime("1976-07-13 02:37:21", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.today()
    # local_unaware_datetime = datetime.now()

    observer_obj, observer_text = geo.main_observer(geo_name=geo_name, unaware_datetime=local_unaware_datetime)
    text = ""
    text += observer_text[0]
    # text += observer_text[1]
    text += observer_text[2]
    # ###########################################################################

    sun_dict, sun_text = main_sun_rise_sett(observer=observer_obj)
    text += sun_text
    print(text)


    # out_list = get_sun_on_month(cur_place)
    # for d in out_list:
    #     for k in sorted(d):
    #         print(k, d[k])
    #     # print sorted(item),item

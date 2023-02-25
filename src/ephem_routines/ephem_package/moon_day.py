
from datetime import datetime
import pprint

import ephem
import src.ephem_routines.ephem_package.geo_place as geo


def _form_str_moon_day(cur_day, day_rise, day_sett, new_rise, str_mark):
    str_out = ""
    str_out += "{:2d} #".format(cur_day)
    str_out += " rise:{0:<18}".format(str(day_rise))
    str_out += " set:{0:<18}".format(str(day_sett))
    str_out += " to:{0:<18}".format(str(new_rise))
    str_out += str_mark

    md_dict = {}
    md_dict["moon_day"] = cur_day
    md_dict["day_rise"] = day_rise
    md_dict["day_sett"] = day_sett
    md_dict["new_rise"] = new_rise

    return str_out, md_dict


def get_moons_in_year(year):
    """Returns a list of the full and new moons in a year. The list contains tuples
    of either the form (DATE,'full') or the form (DATE,'new')"""
    moons=[]

    date=ephem.Date(datetime.date(year, 1, 1))
    while date.datetime().year==year:
        date=ephem.next_full_moon(date)
        moons.append( (date,'full moon') )

    date=ephem.Date(datetime.date(year, 1, 1))
    while date.datetime().year==year:
        date=ephem.next_new_moon(date)
        moons.append( (date,'new moon') )

    date=ephem.Date(datetime.date(year, 1, 1))
    while date.datetime().year==year:
        date=ephem.next_first_quarter_moon(date)
        moons.append( (date,'first_quarter') )

    date=ephem.Date(datetime.date(year, 1, 1))
    while date.datetime().year==year:
        date=ephem.next_last_quarter_moon(date)
        moons.append( (date,'last_quarter') )

    moons.sort(key=lambda x: x[0])

    return moons


def get_lunation_(observer=None):

    # Convert input date to ephem date format
    date = ephem.Date(observer.get_utc)
    moon = ephem.Moon()
    moon.compute(date)
    phase = round(moon.moon_phase * 100, 2)
    print(phase)
    if phase < 100.0 / 8:
        return phase, "Новолуние"
    elif phase < 3 * 100.0 / 8:
        return phase, "Растущая Луна"
    elif phase < 5 * 100.0 / 8:
        return phase, "Первая Четверть"
    elif phase < 7 * 100.0 / 8:
        return phase, "Растущая Луна"
    else:
        return phase, "Полнолуние"


def get_lunation(observer=None):

    # Convert input curr_date to ephem curr_date format
    curr_date = ephem.Date(observer.get_utc)
    # moon = ephem.Moon()
    # moon.compute(curr_date)

    # calculate the curr_date and time of the last new moon
    last_new_moon = ephem.previous_new_moon(curr_date)
    # calculate the curr_date and time of the next new moon
    next_new_moon = ephem.next_new_moon(curr_date)

    # calculate the lunation by subtracting the dates
    cur_term = curr_date - last_new_moon
    lun_term = next_new_moon - last_new_moon
    lunation = cur_term / lun_term

    # print("Lunation:", lunation, observer.get_utc)

    return lunation


def get_moon_phase_moment(observer=None):
    '''
    :param observer:
    :return:
    '''
    #####################################################################
    # observer.unaware_update_utc()
    place_date_utc = observer.get_utc

    prev_NM = ephem.previous_new_moon(place_date_utc)
    prev_FQ = ephem.previous_first_quarter_moon(place_date_utc)
    prev_FM = ephem.previous_full_moon(place_date_utc)
    prev_LQ = ephem.previous_last_quarter_moon(place_date_utc)
    delta_prev_NM = place_date_utc - prev_NM
    delta_prev_FQ = place_date_utc - prev_FQ
    delta_prev_FM = place_date_utc - prev_FM
    delta_prev_LQ = place_date_utc - prev_LQ

    next_NM = ephem.next_new_moon(place_date_utc)
    next_FQ = ephem.next_first_quarter_moon(place_date_utc)
    next_FM = ephem.next_full_moon(place_date_utc)
    next_LQ = ephem.next_last_quarter_moon(place_date_utc)
    delta_next_NM = next_NM - place_date_utc
    delta_next_FQ = next_FQ - place_date_utc
    delta_next_FM = next_FM - place_date_utc
    delta_next_LQ = next_LQ - place_date_utc

    mph_dict = {}
    mph_dict["place_date_utc"] = place_date_utc
    # =======================================================================

    # Повний місяць
    # Молодик
    # Перша чверть
    # Остання чверть

    # New Moon
    # First Quarter
    # Full Moon
    # Last Quarter
    delta_prev = delta_prev_NM
    # mph_dict["prev"] = "New Moon"
    mph_dict["prev"] = "Молодик"
    mph_dict["prev_utc"] = prev_NM

    if delta_prev > delta_prev_FQ:
        delta_prev = delta_prev_FQ
        # mph_dict["prev"] = "First Quarter"
        mph_dict["prev"] = "Перша чверть"
        mph_dict["prev_utc"] = prev_FQ

    if delta_prev > delta_prev_FM:
        delta_prev = delta_prev_FM
        # mph_dict["prev"] = "Full Moon"
        mph_dict["prev"] = "Повний місяць"
        mph_dict["prev_utc"] = prev_FM

    if delta_prev > delta_prev_LQ:
        delta_prev = delta_prev_LQ
        # mph_dict["prev"] = "Last Quarter"
        mph_dict["prev"] = "Остання чверть"
        mph_dict["prev_utc"] = prev_LQ
    # ==========================================================================

    delta_next = delta_next_NM
    # mph_dict["next"] = "New Moon"
    mph_dict["next"] = "Молодик"
    mph_dict["next_utc"] = next_NM

    if delta_next > delta_next_FQ:
        delta_next = delta_next_FQ
        # mph_dict["next"] = "First Quarter"
        mph_dict["next"] = "Перша чверть"
        mph_dict["next_utc"] = next_FQ

    if delta_next > delta_next_FM:
        delta_next = delta_next_FM
        # mph_dict["next"] = "Full Moon"
        mph_dict["next"] = "Повний місяць"
        mph_dict["next_utc"] = next_FM

    if delta_next > delta_next_LQ:
        # delta_next = delta_next_LQ
        # mph_dict["next"] = "Last Quarter"
        mph_dict["next"] = "Остання чверть"
        mph_dict["next_utc"] = next_LQ
    # =========================================================================

    # mph_dict["moon_phase"] = moon.moon_phase

    return mph_dict


def main_moon_phase(observer=None):
    """
        {'calc_date_utc': 44892.471979341906,
         'next': 'First Quarter',
         'next_utc': 44894.10868446941,
         'prev': 'New Moon',
         'prev_utc': 44887.45639035291}
    """
    result_text = ""

    result_text += "\n"

    observer.unaware_update_utc()       # restore utc from previous calculation
    result_dict = get_moon_phase_moment(observer=observer)

    # calc_date_utc = observer.dt_utc_to_aware_by_tz((result_dict["calc_date_utc"].datetime()))
    prev_utc = observer.dt_utc_to_aware((result_dict["prev_utc"].datetime()))
    next_utc = observer.dt_utc_to_aware((result_dict["next_utc"].datetime()))
    result_text += "\n" + prev_utc.strftime(geo.dt_format) + " " + result_dict["prev"]
    # result_text += "\n" + calc_date_utc.strftime(geo.dt_format) + " calc_date_utc"
    result_text += "\n" + next_utc.strftime(geo.dt_format) + " " + result_dict["next"]

    return result_dict, result_text


# def main_moon_day(observer=None):
#     """
#        {'date_utc': 44916.03218687011,
#         'moon_rise': 44915.7511011787,
#         'moon_sett': 44916.03452341712,
#         'moon_day': 29,
#         'new_rise': 44916.81037278403}
#     """
#     result_text = ["", "", ""]
#
#     observer.unaware_update_utc()       # restore utc from previous calculation
#     date_utc = observer.get_utc
#     moon = ephem.Moon(observer.get_place)
#     #####################################################################
#
#     prev_NM = ephem.previous_new_moon(date_utc)
#     next_NM = ephem.next_new_moon(date_utc)
#
#     result_text[0] += "\n"
#     result_text[0] += "\nprev_NM : {:<18}".format(str(prev_NM))
#     result_text[0] += "\nnext_NM : {:<18}".format(str(next_NM))
#     # result_text[0] += "\n"
#
#     cur_mday = 1
#     observer.utc_update_utc(prev_NM)
#
#     moon_rise = observer.get_place.previous_rising(moon)
#     moon_sett = observer.get_place.previous_setting(moon)
#     new_rise = observer.get_place.next_rising(moon)
#
#     result_dict = {}
#     result_dict["date_utc"] = date_utc
#     result_dict["moon_day"] = cur_mday
#     result_dict["moon_rise"] = moon_rise
#     result_dict["moon_sett"] = moon_sett
#     result_dict["new_rise"] = new_rise
#
#     while date_utc > new_rise:
#         str_mark = ""
#
#         if cur_mday == 1:
#             moon_rise = observer.get_place.previous_rising(moon)
#             moon_sett = observer.get_place.previous_setting(moon)
#             if moon_rise > moon_sett:
#                 moon_sett = observer.get_place.next_setting(moon)
#             str_mark = " new moon >>>"
#         else:
#             moon_rise = observer.get_place.next_rising(moon)
#             observer.utc_update_utc(moon_rise)
#             moon_sett = observer.get_place.next_setting(moon)
#             observer.utc_update_utc(moon_sett)
#             new_rise = observer.get_place.next_rising(moon)
#
#             if next_NM < new_rise:
#                 str_mark = " >>> new moon"
#
#         # print "moon_rise=", moon_rise
#
#         str_out = ""
#         str_out += "{:2d} #".format(cur_mday)
#         str_out += " rise:{0:<18}".format(str(moon_rise))
#         str_out += " set:{0:<18}".format(str(moon_sett))
#         str_out += " to:{0:<18}".format(str(new_rise))
#         str_out += str_mark
#
#         result_dict["moon_day"] = cur_mday
#         result_dict["moon_rise"] = moon_rise
#         result_dict["moon_sett"] = moon_sett
#         result_dict["new_rise"] = new_rise
#
#         cur_mday += 1  # prepare for next moon day
#
#         result_text[1] += str_out + "\n"
#         # print result_text
#
#     result_text[1] += "<" * 76 + "\n"
#
#     moon_rise = observer.dt_utc_to_aware((result_dict["moon_rise"].datetime()))
#     moon_sett = observer.dt_utc_to_aware((result_dict["moon_sett"].datetime()))
#
#     result_text[2] += "\n"
#     result_text[2] += "\nMoon day: " + str(result_dict["moon_day"])
#     result_text[2] += "\n" + moon_rise.strftime(geo.dt_format) + " moon_rise"
#     result_text[2] += "\n" + moon_sett.strftime(geo.dt_format) + " moon_sett"
#
#     # observer.unaware_update_utc()   # restore utc for future calculation
#
#     return result_dict, result_text


def main_moon_day(observer=None):
    """
       {'date_utc': 44916.03218687011,
        'moon_rise': 44915.7511011787,
        'moon_sett': 44916.03452341712,
        'moon_day': 29,
        'new_rise': 44916.81037278403}
    """
    result_text = ["", "", ""]

    observer.unaware_update_utc()       # restore utc from previous calculation
    # date_utc = observer.get_utc
    date_utc = observer.get_place.date

    moon = ephem.Moon(observer.get_place)
    #####################################################################

    prev_NM = ephem.previous_new_moon(date_utc)
    next_NM = ephem.next_new_moon(date_utc)

    result_text[0] += "\n"
    result_text[0] += "\nprev_NM : {:<18}".format(str(prev_NM))
    result_text[0] += "\nnext_NM : {:<18}".format(str(next_NM))
    result_text[0] += "\n"

    cur_mday = 1

    observer.utc_update_utc(prev_NM)

    moon_rise = observer.get_place.previous_rising(moon)
    moon_sett = observer.get_place.previous_setting(moon)
    if moon_rise > moon_sett:
        moon_sett = observer.get_place.next_setting(moon)
    new_rise = observer.get_place.next_rising(moon)

    result_dict = {}
    result_dict["date_utc"] = date_utc
    result_dict["moon_day"] = cur_mday
    result_dict["moon_rise"] = moon_rise
    result_dict["moon_sett"] = moon_sett
    result_dict["new_rise"] = new_rise

    while date_utc > new_rise:
        str_mark = ""

        if cur_mday == 1:
            moon_rise = observer.get_place.previous_rising(moon)
            moon_sett = observer.get_place.previous_setting(moon)
            if moon_rise > moon_sett:
                moon_sett = observer.get_place.next_setting(moon)
            str_mark = " *new moon"
        else:
            moon_rise = observer.get_place.next_rising(moon)
            observer.utc_update_utc(moon_rise)
            moon_sett = observer.get_place.next_setting(moon)
            observer.utc_update_utc(moon_sett)
            new_rise = observer.get_place.next_rising(moon)

            if next_NM < new_rise:
                str_mark = " >>> new moon"

        # print "moon_rise=", moon_rise

        str_out = "\n"
        str_out += "{:2d} #".format(cur_mday)
        str_out += " rise:{0:<18}".format(str(moon_rise))
        str_out += " set:{0:<18}".format(str(moon_sett))
        str_out += " to:{0:<18}".format(str(new_rise))

        str_out += " == " + str(moon_sett - moon_rise)

        str_out += str_mark

        result_dict["moon_day"] = cur_mday
        result_dict["moon_rise"] = moon_rise
        result_dict["moon_sett"] = moon_sett
        result_dict["new_rise"] = new_rise

        cur_mday += 1  # prepare for next moon day

        result_text[1] += str_out
        # print result_text

    result_text[1] += "\n" + "<" * 74

    moon_rise = observer.dt_utc_to_aware((result_dict["moon_rise"].datetime()))
    moon_sett = observer.dt_utc_to_aware((result_dict["moon_sett"].datetime()))

    result_text[2] += "\n"
    result_text[2] += "\nMoon day: " + str(result_dict["moon_day"])
    result_text[2] += "\n" + moon_rise.strftime(geo.dt_format) + " moon_rise"
    result_text[2] += "\n" + moon_sett.strftime(geo.dt_format) + " moon_sett"

    return result_dict, result_text


if __name__ == '__main__':

    # geo_name = 'Mragowo'
    # geo_name = 'Boston'
    geo_name = 'Kharkiv'
    # geo_name = 'ASTANA'

    # local_unaware_datetime = datetime.strptime("2023-01-22 03:06:11", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    local_unaware_datetime = datetime.strptime("2023-02-20 11:40:24", geo.dt_format_rev)  # "%Y-%m-%d %H:%M:%S"
    # local_unaware_datetime = datetime.today()
    # local_unaware_datetime = datetime.now()

    observer_obj = geo.Observer(geo_name=geo_name, in_unaware_datetime=local_unaware_datetime)
    text = ""
    text += str(observer_obj)
    # ###########################################################################

    # mph_dict, mph_text = main_moon_phase(observer=observer_obj)
    # pprint.pprint(mph_dict)
    # text += mph_text

    md_dict, md_text = main_moon_day(observer=observer_obj)
    pprint.pprint(md_dict)
    text += md_text[0]
    text += md_text[1]
    text += md_text[2]

    print(text)



    # get_lunation(observer=observer_obj)

    # tp_md_ext = get_moon_day_local12place(loc_date, cur_place)
    # print "tp_md_ext=\n", pprint.pprint(tp_md_ext)

    # for ev in get_moons_in_year(2015):
    #     print ev

    # res_dict = get_moon_phase_local12place(loc_date, cur_place)
    # print("res_dict=", res_dict)
    # pprint.pprint(res_dict)





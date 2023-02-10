# http://stackoverflow.com/questions/16505501/get-timezone-from-city-in-python-django
# http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand


from datetime import datetime, timedelta
import pytz
import ephem


dt_format = "%d/%m/%Y %H:%M:%S %Z %z"
dt_format_rev = "%Y-%m-%d %H:%M:%S"     # fits for dynamoDB "main_record" table # SS[.ffffff]
dt_format_plot = "%d %b, %a"
# dt_format = "%Y-%m-%d %H:%M:%S %z"
# 28/11/2022 10:53:58 +0200


class Observer:
    """
        This is an observer class
    """
    _place = ephem.Observer()
    _place.pressure = 1010     # millibar
    _place.temp = 20           # deg. Celcius
    '''
    Civil twilight uses the value –6 degrees.
    Nautical twilight uses the value –12 degrees.
    Astronomical twilight uses the value –18 degrees.
    '''
    _place.horizon = '0'
    _place.elevation = 3       # meters

    location = None
    timezone_name = "UNDEF"

    _unaware = datetime.strptime("1976-01-13 02:37:21", dt_format_rev)  # dt_format_rev = "%Y-%m-%d %H:%M:%S"
    _unaware12 = datetime.strptime("1999-09-09 09:09:09", dt_format_rev)
    _aware = datetime.strptime("2000-06-21 02:37:21", dt_format_rev)
    _aware12 = datetime.strptime("1999-09-09 09:09:09", dt_format_rev)
    _utc = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    _utc12 = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    _set_noon = False
    _init_unaware = datetime.strptime("1974-01-13 02:37:21", dt_format_rev)  # dt_format_rev = "%Y-%m-%d %H:%M:%S"

    _span = (1., 1.)
    _begin_unaware = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    _end_unaware = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    _begin_aware = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    _end_aware = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    _begin_utc = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    _end_utc = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)

    def __init__(self,
                 latitude=1, longitude=2,
                 geo_name="Kharkiv",
                 input_unaware_datetime=None,   # datetime.strptime("1976-01-13 02:37:21", dt_format_rev),
                 input_utc_datetime=None,
                 span=(2., 2.),
                 ):

        self._latitude = latitude
        self._longitude = longitude
        self._geo_name = geo_name

        self.get_coords_by_name()
        self.get_tz_by_coord()

        self.timezone = pytz.timezone(self.timezone_name)

        # ********************************************************
        if input_utc_datetime is None:
            self._unaware = input_unaware_datetime
            self._init_unaware = self._unaware

            self._aware = self.timezone.localize(self._unaware)
            self._utc = self._aware.astimezone(pytz.timezone('UTC'))
            self._place.date = ephem.Date(self._utc)  # !!!!!!!!!!!!!!!!!!!!!!
            self._set_noon = False

        if input_unaware_datetime is None:
            self._utc = input_utc_datetime
            self._place.date = ephem.Date(self._utc)  # !!!!!!!!!!!!!!!!!!!!!!
            self._set_noon = False

            # ToDo save self._init_unaware
            self._aware = self._utc.replace(tzinfo=pytz.utc).astimezone(self.timezone)
            self._unaware = self._aware.astimezone(self.timezone).replace(tzinfo=None)
            self._init_unaware = self._unaware

        # ********************************************************
        self._span = span
        self._begin_unaware = self._unaware - timedelta(days=self._span[0])
        self._end_unaware = self._unaware + timedelta(days=self._span[1])
        self._begin_aware = self._aware - timedelta(days=self._span[0])
        self._end_aware = self._aware + timedelta(days=self._span[1])
        self._begin_utc = self._utc - timedelta(days=self._span[0])
        self._end_utc = self._utc + timedelta(days=self._span[1])

    def __str__(self):
        str_obj = ""

        # str_obj += "\n" + repr(self.timezone)
        str_obj += "\n" + self._geo_name
        if self.location is not None:
            str_obj += " [{:7.3f},".format(self.location.latitude) + " {:7.3f}]".format(self.location.longitude)
        str_obj += "\n" + self.timezone_name + " (" + str(self._aware.utcoffset()) + ")"
        str_obj += " [DST " + str(self._aware.dst()) + "]"

        str_obj += f'\n{self._unaware.strftime(dt_format)}'

        if not self._set_noon:
            str_obj += f'\n{self._aware.strftime(dt_format)}'
            # str_obj += f'\n{self._utc.strftime(dt_format)}'
        else:
            str_obj += f'\n{self._aware12.strftime(dt_format)}'
            # str_obj += f'\n{self._utc12.strftime(dt_format)}'

        return str_obj

    def __repr__(self):
        return f'Observer(name={self._geo_name}, unaware={self._unaware})'

    def set_coords(self):
        self._place.lat = self._latitude
        self._place.lon = self._longitude

    # def set_pressure(self):
    #     self.place.pressure = self.pressure
    #
    # def set_temp(self):
    #     self.place.temp = self.temp
    #
    # def set_horizon(self):
    #     self.place.horizon = self.horizon
    #
    # def set_elevation(self):
    #     self.place.elevation = self.elevation

    def get_coords_by_name(self):
        from geopy.geocoders import Nominatim               # pip install geopy
        geolocator = Nominatim(user_agent="user_agent")
        self.location = geolocator.geocode(self._geo_name)   # Kremenchuk Boston
        if self.location is not None:
            self._place.lat = str(self.location.latitude)
            self._place.lon = str(self.location.longitude)

            # ToDo for setting by coordinate. Now just for monitoring
            self._latitude = self._place.lat
            self._longitude = self._place.lon
        else:
            self._latitude = 50
            self._longitude = 30

        # print(self.geo_name, self.location.latitude, self.location.longitude)

    def get_tz_by_coord(self):
        from timezonefinder import TimezoneFinder
        timezone = TimezoneFinder()
        if self.location is not None:
            self.timezone_name = timezone.timezone_at(lng=self.location.longitude, lat=self.location.latitude)
        else:
            self.timezone_name = 'UTC'
        # print(self.timezone_name)

    def unaware_to_aware_by_tz(self):
        cur_timezone = pytz.timezone(self.timezone_name)  # 'Europe/Kiev'
        self._aware = cur_timezone.localize(self._unaware)
        # print("self.aware_datetime=", self.aware_datetime)

    def aware_to_utc(self):
        self._utc = self._aware.astimezone(pytz.timezone('UTC'))
        self._place.date = self._utc
        self._set_noon = False

        # print("self.utc_datetime=", self.utc_datetime)

    def utc_update_utc(self, in_utc_date):
        self._utc = in_utc_date
        self._place.date = ephem.Date(self._utc)  # !!!!!!!!!!!!!!!!!!!!!!
        self._set_noon = False

    @property
    def get_geo_name(self):                     # currently set place of observer
        return self._geo_name

    @property
    def get_place(self):                        # currently set place of observer
        return self._place

    @property
    def get_utc(self):                          # currently set place date of observer
        return self._place.date

    @property
    def get_unaware(self):                      # currently set unaware of observer
        return self._unaware

    @property
    def get_span(self):
        return self._span

    @property
    def get_span_unaware(self):
        return self._begin_unaware, self._end_unaware

    @property
    def get_span_aware(self):
        return self._begin_aware, self._end_aware

    @property
    def get_span_utc(self):
        return self._begin_utc, self._end_utc

    # @property
    def restore_unaware(self):                      # restore unaware of observer
        self._unaware = self._init_unaware
        return self._unaware

    def utc_to_aware_by_tz(self) -> None:       # restore internal aware from UTC
        self._aware = self._utc.replace(tzinfo=pytz.utc).astimezone(self.timezone)
        # print("self.aware_datetime=", self.aware_datetime)

    def dt_utc_to_aware(self, in_utc=None) -> datetime:
        if in_utc is not None:
            out_aware = in_utc.replace(tzinfo=pytz.utc).astimezone(self.timezone)
            return out_aware

    def dt_utc_to_unaware(self, in_utc=None) -> datetime:
        if in_utc is not None:
            out_aware = in_utc.replace(tzinfo=pytz.utc).astimezone(self.timezone)
            out_unaware = out_aware.astimezone(self.timezone).replace(tzinfo=None)
            return out_unaware

    def dt_unaware_to_utc(self, in_unaware=None) -> datetime:
        if in_unaware is not None:
            loc_aware = self.timezone.localize(in_unaware)
            out_utc = loc_aware.astimezone(pytz.timezone('UTC'))
            return out_utc

    def dt_aware_to_unaware(self, in_aware=None) -> datetime:
        if in_aware is not None:
            out_unaware = in_aware.astimezone(self.timezone).replace(tzinfo=None)
            return out_unaware

    def unaware_update_utc(self, in_unaware=None) -> None:
        if in_unaware is not None:
            self._unaware = in_unaware
        self._aware = self.timezone.localize(self._unaware)
        self._utc = self._aware.astimezone(pytz.timezone('UTC'))
        self._place.date = ephem.Date(self._utc)  # !!!!!!!!!!!!!!!!!!!!!!
        self._set_noon = False

    def unaware_update_utc12(self, in_unaware=None) -> None:
        if in_unaware is not None:
            self._unaware = in_unaware
        self._unaware12 = datetime(self._unaware.year, self._unaware.month, self._unaware.day, 12, 0, 0)
        self._aware12 = self.timezone.localize(self._unaware12)
        self._utc12 = self._aware12.astimezone(pytz.timezone('UTC'))
        self._place.date = ephem.Date(self._utc12)  # !!!!!!!!!!!!!!!!!!!!!!
        self._set_noon = True


# def get_place_coord(in_place_name):
#
#     from geopy.geocoders import Nominatim               # pip install geopy
#     geolocator = Nominatim(user_agent="user_agent")
#     location = geolocator.geocode(in_place_name)        # Kremenchuk Boston
#     # print((location.latitude, location.longitude))
#
#     return location.latitude, location.longitude
#
#
# def get_tz_name(in_coord):
#
#     from timezonefinder import TimezoneFinder
#     tf = TimezoneFinder()
#     tz_name = tf.timezone_at(lng=in_coord[1], lat=in_coord[0])
#     # print(tz_name)
#
#     return tz_name
#
#
# def set_tz_to_unaware_time(in_tz_name, in_unaware):
#
#     local_tz = pytz.timezone(in_tz_name)  # 'Europe/Kiev'
#     loc_aware = local_tz.localize(in_unaware)
#
#     # print "loc_aware=", loc_aware
#     return loc_aware
#
#     # I had use from dt_aware to dt_unware
#     #
#     # dt_unaware = dt_aware.replace(tzinfo=None)
#     #
#     # and dt_unware to dt_aware
#     #
#     # from pytz import timezone
#     # localtz = timezone('Europe/Lisbon')
#     # dt_aware = localtz.localize(dt_unware)
#
#
# def aware_time_to_utc(in_aware):
#     utc_aware = in_aware.astimezone(pytz.timezone('UTC'))
#     # print "utc_aware=", utc_aware
#     return utc_aware
#
#
# def utc_to_loc_time(in_tz_name, in_utc_time):
#     local_timezone = pytz.timezone(in_tz_name)  # 'Europe/Kiev'
#     loc_time = in_utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
#     # print "loc_time=", loc_time
#     return loc_time
#
#
# def loc_to_utc_time(in_tz_name, in_loc_time):
#     loc_timezone = pytz.timezone(in_tz_name)
#     loc_time = loc_timezone.localize(in_loc_time)
#     utc_time = loc_time.astimezone(pytz.timezone('UTC'))
#
#     # print "utc_time=", utc_time
#     return utc_time
#
#
# def aware_loc_unaware_utc_for_local12place(in_unaware_loc, place):  # rework!!!
#     """
#     Input: local unaware time and place
#     Returns tuple in utc for local time and place
#     """
#     # tz_nam, coord = geopr.set_tz(place)
#     # place = Observer.objects.get(pk=10)
#     # tz_nam = place.timezone_name
#     tz_nam = "Europe/Kiev"
#     # coord = (place.latitude, place.longitude)
#     coord = (22, 33)
#
#     print("place=", place.title, coord, tz_nam)
#
#     ###########################################################################
#     cur_date_loc = in_unaware_loc  # datetime.datetime.today()
#     # print "cur_date_loc=", cur_date_loc.strftime(format)
#
#     # Calculate utc date on local noon for selected place #####################
#     cur_noon_loc = datetime(cur_date_loc.year, cur_date_loc.month, cur_date_loc.day, 12, 0, 0)
#     # print "cur_noon_loc=", cur_noon_loc
#     # -------------------------------------------------------------------------
#
#     aware_loc = set_tz_to_unaware_time(tz_nam, cur_noon_loc)
#     # print "aware_loc=", aware_loc.strftime(format)
#     # -------------------------------------------------------------------------
#
#     unaware_utc = aware_time_to_utc(aware_loc)
#     # print "aware_utc=",    unaware_utc.strftime(format)
#     # print "unaware_utc=", unaware_utc.strftime(format), "utcoffset=", unaware_utc.utcoffset()
#
#     return aware_loc, unaware_utc


def main_observer(geo_name="Boston", unaware_datetime=datetime.today()):

    result_text = ["", "", ""]
    result_observer = Observer(geo_name=geo_name, input_unaware_datetime=unaware_datetime)

    # result_text[0] += "\n" + geo_name
    # result_text[0] += " [{:7.3f},".format(result_observer.location.latitude) + \
    #                " {:7.3f}]".format(result_observer.location.longitude)
    # result_text[0] += "\n" + result_observer.timezone_name + " (" + str(result_observer.aware.utcoffset()) + ")"
    # result_text[0] += " [DST " + str(result_observer.aware.dst()) + "]"
    #
    # result_text[1] += "\n" + result_observer.unaware.strftime(dt_format)
    # result_text[1] += "\n" + result_observer.aware.strftime(dt_format)
    # result_text[1] += "\n" + result_observer.utc.strftime(dt_format)
    #
    # result_text[2] += "\n" + result_observer.unaware12.strftime(dt_format)
    # result_text[2] += "\n" + result_observer.utc12.strftime(dt_format)

    return result_observer, result_text


if __name__ == '__main__':

    geo_name = 'Boston'
    # geo_name = 'London'
    # geo_name = 'Kharkiv'
    # geo_name = 'Warsaw'

    # ###########################################################################

    unaware_dt = datetime.today()
    observer_obj, observer_text = main_observer(geo_name=geo_name, unaware_datetime=unaware_dt)
    print(observer_obj)

    observer_obj.unaware_update_utc12()
    print(observer_obj)

    unaware_dt = datetime.strptime("2022-12-26 12:37:21", "%Y-%m-%d %H:%M:%S")
    observer_obj.unaware_update_utc12(unaware_dt)
    print(observer_obj)


    # dict = {}
    # dict["obj_name"] = observer_obj
    #
    # print(type(observer_obj))
    # print(type(dict["obj_name"]))


    # print("\n*** utc -> aware")
    # observer.utc = datetime.strptime("2011-06-21 02:37:21", "%Y-%m-%d %H:%M:%S")
    # observer.utc_to_aware_by_tz()                           # aware_datetime
    # print("utc=", observer.utc.strftime(dt_format), observer.aware.utcoffset())
    # print("awa=", observer.aware.strftime(dt_format))

# http://stackoverflow.com/questions/16505501/get-timezone-from-city-in-python-django
# http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand


from datetime import datetime
import pytz
import ephem

dt_format = "%d/%m/%Y %H:%M:%S %Z %z"
dt_format_rev = "%Y-%m-%d %H:%M:%S"     # fits for dynamoDB "main_record" table # SS[.ffffff]
# dt_format = "%Y-%m-%d %H:%M:%S %z"
# 28/11/2022 10:53:58 +0200


class Observer:

    """This is an observer class"""
    place = ephem.Observer()
    place.pressure = 1010     # millibar
    place.temp = 25           # deg. Celcius
    '''
    Civil twilight uses the value –6 degrees.
    Nautical twilight uses the value –12 degrees.
    Astronomical twilight uses the value –18 degrees.
    '''
    place.horizon = '0'
    place.elevation = 3       # meters

    location = None
    timezone_name = "UNDEF"

    unaware = datetime.strptime("1976-01-13 02:37:21", dt_format_rev)  # dt_format_rev = "%Y-%m-%d %H:%M:%S"
    unaware12 = datetime.strptime("1999-09-09 09:09:09", dt_format_rev)
    aware = datetime.strptime("2011-06-21 02:37:21", dt_format_rev)
    aware12 = datetime.strptime("1999-09-09 09:09:09", dt_format_rev)
    utc = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)
    utc12 = datetime.strptime("2000-01-01 00:00:01", dt_format_rev)

    def __init__(self, latitude=0, longitude=0, geo_name="Kharkiv"):
        self.latitude = latitude
        self.longitude = longitude
        self.geo_name = geo_name

    def set_coords(self):
        self.place.lat = self.latitude
        self.place.lon = self.longitude

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
        self.location = geolocator.geocode(self.geo_name)   # Kremenchuk Boston
        self.place.lat = str(self.location.latitude)
        self.place.lon = str(self.location.longitude)
        # print(self.geo_name, self.location.latitude, self.location.longitude)

    def get_tz_by_coord(self):
        from timezonefinder import TimezoneFinder
        timezone = TimezoneFinder()
        self.timezone_name = timezone.timezone_at(lng=self.location.longitude, lat=self.location.latitude)
        # print(self.timezone_name)

    def unaware_to_aware_by_tz(self):
        cur_timezone = pytz.timezone(self.timezone_name)  # 'Europe/Kiev'
        self.aware = cur_timezone.localize(self.unaware)
        # print("self.aware_datetime=", self.aware_datetime)

    def aware_to_utc(self):
        self.utc = self.aware.astimezone(pytz.timezone('UTC'))
        # print("self.utc_datetime=", self.utc_datetime)

    def utc_to_aware_by_tz(self):
        cur_timezone = pytz.timezone(self.timezone_name)
        self.aware = self.utc.replace(tzinfo=pytz.utc).astimezone(cur_timezone)
        # print("self.aware_datetime=", self.aware_datetime)

    def dt_utc_to_aware_by_tz(self, in_utc):
        cur_timezone = pytz.timezone(self.timezone_name)
        out_aware = in_utc.replace(tzinfo=pytz.utc).astimezone(cur_timezone)
        # print("self.aware_datetime=", self.aware_datetime)
        return out_aware

    def unaware12_to_utc(self):
        # Calculate utc date on local noon for selected place #####################
        self.unaware12 = datetime(self.unaware.year, self.unaware.month, self.unaware.day, 12, 0, 0)
        cur_timezone = pytz.timezone(self.timezone_name)
        self.aware12 = cur_timezone.localize(self.unaware12)
        self.utc12 = self.aware12.astimezone(pytz.timezone('UTC'))
        # -------------------------------------------------------------------------
        # print("self.aware_noon=", self.aware12.strftime(dt_format))
        # print("self.utc_datetime=", self.utc, "utcoffset=", self.utc.utcoffset())


# local_dt
# aware_dt
# unaware_dt
# utc_dt
# unaware_to_aware_by_tz
# aware_time_to_utc
# utc_to_loc_time
# loc_to_utc_time



def get_place_coord(in_place_name):

    from geopy.geocoders import Nominatim               # pip install geopy
    geolocator = Nominatim(user_agent="user_agent")
    location = geolocator.geocode(in_place_name)        # Kremenchuk Boston
    # print((location.latitude, location.longitude))

    return location.latitude, location.longitude


def get_tz_name(in_coord):

    from timezonefinder import TimezoneFinder
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=in_coord[1], lat=in_coord[0])
    # print(tz_name)

    return tz_name


def set_tz_to_unaware_time(in_tz_name, in_unaware):

    local_tz = pytz.timezone(in_tz_name)  # 'Europe/Kiev'
    loc_aware = local_tz.localize(in_unaware)

    # print "loc_aware=", loc_aware
    return loc_aware

    # I had use from dt_aware to dt_unware
    #
    # dt_unaware = dt_aware.replace(tzinfo=None)
    #
    # and dt_unware to dt_aware
    #
    # from pytz import timezone
    # localtz = timezone('Europe/Lisbon')
    # dt_aware = localtz.localize(dt_unware)


def aware_time_to_utc(in_aware):
    utc_aware = in_aware.astimezone(pytz.timezone('UTC'))
    # print "utc_aware=", utc_aware
    return utc_aware


def utc_to_loc_time(in_tz_name, in_utc_time):
    local_timezone = pytz.timezone(in_tz_name)  # 'Europe/Kiev'
    loc_time = in_utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    # print "loc_time=", loc_time
    return loc_time


def loc_to_utc_time(in_tz_name, in_loc_time):
    loc_timezone = pytz.timezone(in_tz_name)
    loc_time = loc_timezone.localize(in_loc_time)
    utc_time = loc_time.astimezone(pytz.timezone('UTC'))

    # print "utc_time=", utc_time
    return utc_time


def aware_loc_unaware_utc_for_local12place(in_unaware_loc, place):  # rework!!!
    """
    Input: local unaware time and place
    Returns tuple in utc for local time and place
    """
    # tz_nam, coord = geopr.set_tz(place)
    # place = Observer.objects.get(pk=10)
    # tz_nam = place.timezone_name
    tz_nam = "Europe/Kiev"
    # coord = (place.latitude, place.longitude)
    coord = (22, 33)

    print("place=", place.title, coord, tz_nam)

    ###########################################################################
    cur_date_loc = in_unaware_loc  # datetime.datetime.today()
    # print "cur_date_loc=", cur_date_loc.strftime(format)

    # Calculate utc date on local noon for selected place #####################
    cur_noon_loc = datetime(cur_date_loc.year, cur_date_loc.month, cur_date_loc.day, 12, 0, 0)
    # print "cur_noon_loc=", cur_noon_loc
    # -------------------------------------------------------------------------

    aware_loc = set_tz_to_unaware_time(tz_nam, cur_noon_loc)
    # print "aware_loc=", aware_loc.strftime(format)
    # -------------------------------------------------------------------------

    unaware_utc = aware_time_to_utc(aware_loc)
    # print "aware_utc=",    unaware_utc.strftime(format)
    # print "unaware_utc=", unaware_utc.strftime(format), "utcoffset=", unaware_utc.utcoffset()

    return aware_loc, unaware_utc


def main_observer(geo_name="Boston", unaware_datetime=datetime.today()):

    result_text = ["", "", ""]
    result_observer = Observer(geo_name=geo_name)
    result_observer.get_coords_by_name()
    result_observer.get_tz_by_coord()

    result_observer.unaware = unaware_datetime      # unaware_datetime
    result_observer.unaware_to_aware_by_tz()        # aware_datetime
    result_observer.aware_to_utc()                  # utc_datetime

    result_observer.unaware12_to_utc()              # utc_datetime


    result_text[0] += "\nName: " + geo_name
    result_text[0] += " [{:7.3f},".format(result_observer.location.latitude) + \
                   " {:7.3f}]".format(result_observer.location.longitude)
    result_text[0] += "\ntz: " + result_observer.timezone_name + " (" + str(result_observer.aware.utcoffset()) + ")"
    result_text[0] += "\ndst: " + str(result_observer.aware.dst())

    # result_text += "\n*** unaware -> aware -> utc"
    result_text[1] += "\n" + result_observer.unaware.strftime(dt_format)
    result_text[1] += "\n" + result_observer.aware.strftime(dt_format)
    result_text[1] += "\n" + result_observer.utc.strftime(dt_format)

    result_text[2] += "\n" + result_observer.unaware12.strftime(dt_format)
    result_text[2] += "\n" + result_observer.utc12.strftime(dt_format)

    return result_observer, result_text


if __name__ == '__main__':

    # geo_name = 'Boston'
    geo_name = 'London'
    # geo_name = 'Kharkiv'
    # ###########################################################################

    # observer = Observer(geo_name=geo_name)
    # observer.get_coords_by_name()
    # print("geo_name=", observer.geo_name, "[lat=", observer.location.latitude, "lon=", observer.location.longitude, "]")
    # observer.get_tz_by_coord()
    # print("timezone=", observer.timezone_name)
    # # print(observer.place, "\n")
    #
    # print("\n*** unaware -> aware -> utc")
    # # observer.unaware = datetime.strptime("2011-06-21 02:37:21", "%Y-%m-%d %H:%M:%S")
    # observer.unaware = datetime.now()                       # unaware_datetime
    # observer.unaware_to_aware_by_tz()                       # aware_datetime
    # observer.aware_to_utc()                                 # utc_datetime
    # print("una=", observer.unaware.strftime(dt_format), observer.aware.utcoffset())
    # print("awa=", observer.aware.strftime(dt_format), observer.aware.utcoffset())
    # print("utc=", observer.utc.strftime(dt_format), observer.aware.utcoffset())

    unaware_dt = datetime.strptime("2011-05-21 08:37:21", "%Y-%m-%d %H:%M:%S")
    # unaware_dt = datetime.today()
    observer_obj, observer_text = main_observer(geo_name=geo_name, unaware_datetime=unaware_dt)
    # print(observer_obj)
    print(observer_text[0])
    print(observer_text[1])
    print(observer_text[2])

    dict = {}
    dict["obj_name"] = observer_obj

    print(type(observer_obj))
    print(type(dict["obj_name"]))


    # print("\n*** utc -> aware")
    # observer.utc = datetime.strptime("2011-06-21 02:37:21", "%Y-%m-%d %H:%M:%S")
    # observer.utc_to_aware_by_tz()                           # aware_datetime
    # print("utc=", observer.utc.strftime(dt_format), observer.aware.utcoffset())
    # print("awa=", observer.aware.strftime(dt_format))
    #
    # print("\n*** unaware -> unaware12 -> aware12 -> utc")
    # observer.unaware = datetime.strptime("1976-01-13 04:22:01", "%Y-%m-%d %H:%M:%S")
    # observer.aware12_to_utc()                               # utc_datetime
    # print("una=", observer.unaware.strftime(dt_format))
    # print("u12=", observer.unaware12.strftime(dt_format))
    # print("a12=", observer.aware12.strftime(dt_format))
    # print("utc=", observer.utc.strftime(dt_format))

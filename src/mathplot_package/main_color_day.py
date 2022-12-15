import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd


observer = geo.Observer(geo_name="Mragowo")
observer.get_coords_by_name()
observer.get_tz_by_coord()

days = 100
# Using current time
ini_time_for_now = datetime.now()
begin_date = ini_time_for_now - timedelta(days=days)
end_day = ini_time_for_now + timedelta(days=days)

x = np.linspace(begin_date.timestamp(), end_day.timestamp(), 1000)
print(x)

sun_lon = []
sun_lat = []
moon_lon = []
moon_lat = []
sun_dist = []
moon_dist = []
for cur_dt in x:

    ecl_dict = zd.get_zodiac_Sun_Moon(observer, datetime.fromtimestamp(cur_dt))
    # print(ecl_dict)
    sun_lon.append(ecl_dict["sun_lon"])
    sun_lat.append(ecl_dict["sun_lat"])     # sun.alt
    moon_lon.append(ecl_dict["moon_lon"])
    moon_lat.append(ecl_dict["moon_lat"])

    sun_dist.append(ecl_dict["sun_dist"])
    moon_dist.append(ecl_dict["moon_dist"])

# print(sun_lon)
# print(sun_lat)
# print(moon_lon)
print(moon_lat)



# x = [1, 2, 3, 4]
y = moon_dist     # [1, 4, 9, 6]
labels = ['Frogs', 'Hogs', 'Bogs', 'Slogs']

plt.plot(x, y)
# You can specify a rotation for the tick labels in degrees or with keywords.
# plt.xticks(x, labels, rotation='vertical')
# Pad margins so that markers don't get clipped by the axes
# plt.margins(0.2)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)
plt.show()

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import matplotlib.cm as cm


import src.ephem_routines.ephem_package.geo_place as geo
import src.ephem_routines.ephem_package.sun_rise_sett as sr
import src.ephem_routines.ephem_package.zodiac_phase as zd


observer = geo.Observer(geo_name="Mragowo")
observer.get_coords_by_name()
observer.get_tz_by_coord()

days = 3
# Using current time
ini_time_for_now = datetime.now()
begin_date = ini_time_for_now - timedelta(days=days)
end_day = ini_time_for_now + timedelta(days=days)

dates = np.linspace(begin_date.timestamp(), end_day.timestamp(), 500)
# print(x)

sun_lon = []
sun_lat = []
moon_lon = []
moon_lat = []
# sun_dist = []
# moon_dist = []
sun_angle = []

for cur_dt in dates:
    observer.utc = datetime.fromtimestamp(cur_dt)
    ecl_dict, ecl_text = zd.main_zodiac_sun_moon(observer=observer)
    # print(ecl_dict)
    sun_lon.append(ecl_dict["sun_lon"])
    sun_lat.append(ecl_dict["sun_lat"])     # sun.alt
    moon_lon.append(ecl_dict["moon_lon"])
    moon_lat.append(ecl_dict["moon_lat"])

    # sun_dist.append(ecl_dict["sun_dist"])
    # moon_dist.append(ecl_dict["moon_dist"])

    sun_dict, sun_text = sr.main_sun_rise_sett(observer=observer)
    sun_angle.append(sun_dict["sun_angle"])


# print(sun_lon)
# print(sun_lat)
# print(moon_lon)
print(sun_angle.__len__())

# y = np.exp(sun_angle)
y = np.power(sun_angle, 2)

fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(4, 7))

arr_size = len(y)
Z = np.zeros(arr_size*3).reshape(arr_size, 3)

dates = np.ones(arr_size)
# Z[:, 0] = y
Z[:, 1] = y
# Z[:, 2] = y

# print(Z)
plt.grid(axis='y')
im = plt.imshow(Z, interpolation='bicubic',     # 'nearest', 'bilinear', 'bicubic'
                   cmap=cm.RdYlGn,  #gray
                   origin='lower',
                   extent=[-days/4, days/4, -days, days],
                   vmax=Z.max(), vmin=Z.min())

plt.show()

# coding: utf8
#!/usr/bin/python


import sys

# import ConfigParser
try:
    import configparser
except:
    from six.moves import configparser

import pprint
import datetime


# import astro.geo_place as geo
import geo_place as geo

# cur_path_to_file = 'geo_test.cfg'

GEO_PLACE_dict = \
    {
        'Kharkiv_test':
            {
                "latitude": 50.00,
                "longitude": 36.15,
                "timezone": "Europe/Zaporozhye",
                "dst": "True",
            },
        'Boston_test':
            {
                "latitude": 42.36,
                "longitude": 71.05,
                "timezone": "ewroi",
                "dst": "False",
            },
    }


def set_tz(in_place_name):

    '''
    :param in_place_name:
    :return: tz_name, coord
    '''

    tz_name = ""
    coord = (0, 0)

    if in_place_name in GEO_PLACE_dict:

        # From local dict GEO_PLACE
        lat = GEO_PLACE_dict[in_place_name]["latitude"]
        lon = GEO_PLACE_dict[in_place_name]["longitude"]

        coord = (lat, lon)
        tz_name = GEO_PLACE_dict[in_place_name]["timezone"]
    else:
        # Update from Google ######################################################
        try:
            coord = geo.get_place_coord(in_place_name)
        except:
            str_res = "Unexpected error:" + str(sys.exc_info()[0]) + str(sys.exc_info()[1])
            print(str_res)

        # print in_place_name, coord

        tz_name = geo.get_tz_name(coord)
        # print "tz_name=", tz_name

        # Save to
        if in_place_name in GEO_PLACE_dict:
            pass
        else:
            pass
            GEO_PLACE_dict.update({in_place_name:
                                            {
                                                "latitude": coord[0],
                                                "longitude": coord[1],
                                                "timezone": tz_name,
                                                "dst": "iutuyrdfkhjds"
                                             }
                                        })
            # write_geo_to_config(GEO_PLACE_dict)

    return tz_name, coord


# def write_geo_to_config(in_place_dict):
#
#     global cur_path_to_file
#
#     config = configparser.RawConfigParser()
#
#     for place in in_place_dict.keys():
#
#         lat = in_place_dict[place]["latitude"]
#         lon = in_place_dict[place]["longitude"]
#         tzn = in_place_dict[place]["timezone"]
#         dst = in_place_dict[place]["dst"]
#
#         upd = datetime.datetime.now()
#
#         print(place, lat, lon, dst, "-"*40)
#
#         # # When adding sections or items, add them in the reverse order of
#         # # how you want them to be displayed in the actual file.
#         # # In addition, please note that using RawConfigParser's and the raw
#         # # mode of ConfigParser's respective set functions, you can assign
#         # # non-string values to keys internally, but will receive an error
#         # # when attempting to write to a file or when you get it in non-raw
#         # # mode. SafeConfigParser does not allow such assignments to take place.
#         # config.add_section('Section')
#         # config.set('Section', 'an_int', '15')
#         # config.set('Section', 'a_bool', 'true')
#         # config.set('Section', 'a_float', '3.1415')
#         # config.set('Section', 'baz', 'fun')
#         # config.set('Section', 'bar', 'Python')
#         # config.set('Section', 'foo', '%(bar)s is %(baz)s!')
#
#         config.add_section(place)
#         config.set(place, 'latitude', lat)
#         config.set(place, 'longitude', lon)
#         config.set(place, 'timezone', tzn)
#         config.set(place, 'updated', upd)
#         config.set(place, 'dst', dst)
#
#     # Writing our configuration file to 'settings.cfg'
#     with open(cur_path_to_file, 'wb') as configfile:
#         config.write(configfile)
#         print("Configuration saved.")
#
#
# def as_dict(config):
#     """
#     Converts a ConfigParser object into a dictionary.
#
#     The resulting dictionary has sections as keys which point to a dict of the
#     sections options as key => value pairs.
#     """
#     the_dict = {}
#     for section in config.sections():
#         the_dict[section] = {}
#         for key, val in config.items(section):
#             the_dict[section][key] = val
#     return the_dict
#
#
# def read_config_to_geo(path_to_file):
#
#     global cur_path_to_file
#
#     cur_path_to_file = path_to_file
#
#     try:
#
#         with open(cur_path_to_file, 'r') as configfile:
#
#             config = configparser.RawConfigParser()
#
#             config.read_file(configfile)
#
#             # # print config._sections
#             # # getfloat() raises an exception if the value is not a float
#             # # getint() and getboolean() also do this for their respective types
#             # a_float = config.getfloat('Section', 'a_float')
#             # an_int = config.getint('Section', 'an_int')
#             # print a_float + an_int
#             #
#             # # Notice that the next output does not interpolate '%(bar)s' or '%(baz)s'.
#             # # This is because we are using a RawConfigParser().
#             # if config.getboolean('Section', 'a_bool'):
#             #     print config.get('Section', 'foo')
#
#             print("\n   Reading config file...")
#
#             res_dict = as_dict(config)
#             # print "res_dict=", res_dict
#
#             return res_dict
#
#     except IOError:
#
#         print("there is no config file!!!")
#         print("used defaults...")
#
#         return GEO_PLACE_dict
#
#





if __name__ == '__main__':

    path_to_file = 'geo_test.cfg'

    # res_d = read_config_to_geo(path_to_file)
    print("res_d=\n", pprint.pprint(res_d))

    write_geo_to_config(res_d)


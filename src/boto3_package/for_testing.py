
from pprint import pprint


my_dict = {'a': 1, 'b': 2}

default_dict = my_dict.setdefault('c', {})
default_dict['x'] = 3
print(my_dict)  # Output: {'a': 1, 'b': 2, 'c': {'x': 3}}

#
#
#
item_dict = {
    'activity': {"attempts": 8, "state": False, "last_error": "Overload2"},
    'payment': {"term": 11.009},
    'context_user_data': {
        'Geolocation': 'WARSHAW',
        'Interval': '4.560',
        'Reminder': '0011'
    },
    # 'context_user_data': {},
    # 'context_user_data': "",
    'pk_user_bot_id': '4774374724#122233333', 'last_time': '2023-01-31 11:04:43',
    'sk_user_bot_name': 'Serhii Surmylo @ Biblyka_bot'
}

# print("---------------------", item_dict['context_user_data'])
# default_context_user_data = item_dict.setdefault('context_user_data', {})
item_dict.setdefault('context_user_data', {})

# value = my_dict.setdefault('c', 3)
item_dict['context_user_data'].setdefault('Geolocation', "OLSZTYN")
item_dict['context_user_data'].setdefault('Interval', "4.567")
item_dict['context_user_data'].setdefault('Reminder', "0123")

# default_context_user_data['Geolocation'] = 'OLSZTYN'
# default_context_user_data['Interval'] = '4.567'
# default_context_user_data['Reminder'] = '0011'

pprint(item_dict)

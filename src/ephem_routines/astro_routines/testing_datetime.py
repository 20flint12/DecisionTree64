from datetime import datetime

# my_string = str(input('Enter date(yyyy-mm-dd): '))
in_time = "1451"
my_string = "2000-01-01 " + in_time

try:
    my_date = datetime.strptime("2000-01-01 " + in_time, "%Y-%m-%d %H%M")
    print(my_date.time().hour)
except ValueError:
    print("err")

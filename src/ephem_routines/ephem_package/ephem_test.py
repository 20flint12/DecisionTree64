
import ephem

def moon_phase(date):
    # Convert input date to ephem date format
    date = ephem.Date(date)
    moon = ephem.Moon()
    moon.compute(date)
    phase = round(moon.moon_phase * 100, 2)
    print(phase)
    if phase < 100.0/8:
        return "Новолуние"
    elif phase < 3*100.0/8:
        return "Растущая Луна"
    elif phase < 5*100.0/8:
        return "Первая Четверть"
    elif phase < 7*100.0/8:
        return "Растущая Луна"
    else:
        return "Полнолуние"

date = "2023/4/01"
print(moon_phase(date))

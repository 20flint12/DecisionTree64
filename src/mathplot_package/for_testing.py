import ephem
import datetime

date = datetime.datetime.now()
print("Date: " + str(date))

obs=ephem.Observer()
obs.lat='52:00'
obs.long='21:00'
obs.date = date
# print obs

sun = ephem.Sun(obs)
sun.compute(obs)
print(float(sun.alt))
print(str(sun.alt))
sun_angle = float(sun.alt) * 57.2957795 # Convert Radians to degrees
print("sun_angle: %f" % sun_angle)
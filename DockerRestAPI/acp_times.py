"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    #the speed that we divide by to get opening time
    speed = [34, 32, 30, 28, 26]
    buff = brevet_dist_km * 1.2
    if (control_dist_km > brevet_dist_km* 1.2):
        return "err1"

    if (control_dist_km > 1200 or control_dist_km < 0):
        return "err2"

    if (control_dist_km >= 0 and control_dist_km <= 200):
        opening_time = control_dist_km/speed[0]

    elif(control_dist_km > 200 and control_dist_km <= 400):
        previous = 200/speed[0]
        opening_time = previous + (control_dist_km-200)/speed[1]

    elif(control_dist_km > 400 and control_dist_km <= 600):
        previous = (200/speed[0]) + (200/speed[1])
        opening_time = previous + (control_dist_km-400)/speed[2]

    elif(control_dist_km > 600 and control_dist_km <= 1000):
        previous = (200/speed[0]) + (200/speed[1]) + (200/speed[2])
        opening_time = previous + (control_dist_km-600)/speed[3]

    elif(control_dist_km > 1000 and control_dist_km <= 1300):
        previous = (200/speed[0]) + (200/speed[1]) + (200/speed[2]) + (200/speed[3])
        opening_time = previous + (control_dist_km-1000)/speed[4]


    hours = opening_time // 1
    minutes = round((opening_time % 1) * 60)

    time = arrow.get(brevet_start_time)
    time = time.shift(hours=+hours, minutes=+minutes)
    print("opening time: " + str(time))
    
    return time.isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    speed = [15, 15, 15, 11.428, 13.333]
    buff = brevet_dist_km * 1.2
    if (control_dist_km > brevet_dist_km* 1.2):
        return "err1"

    if (control_dist_km > 1200 or control_dist_km < 0):
        return "err2"

    #less than 60km
    if (control_dist_km >=0 and control_dist_km < 60):
        closing_time = (control_dist_km/20) + 1
    
    #brevet dist of 200km
    elif (((brevet_dist_km==200) and (0 <= control_dist_km <= 240)) or (0 < control_dist_km <= 200)):
        if (200 <= control_dist_km <= buff and brevet_dist_km == 200):
            closing_time = 13.5
        else:
            closing_time = control_dist_km/speed[0]
    
    #brevet dist of 300km
    elif (((brevet_dist_km==300) and (200 < control_dist_km <= 360)) or (200 < control_dist_km <= 300)):
        if(300 <= control_dist_km <= buff and brevet_dist_km == 300):
            closing_time = 20
        else:
            closing_time = (control_dist_km)/speed[1]

    #brevet dist of 400km
    elif (((brevet_dist_km==400) and (200 < control_dist_km <= 480)) or (200 < control_dist_km <= 400)):
        if (400 <= control_dist_km <= buff and brevet_dist_km == 400):
            closing_time = 27
        else:
            closing_time = (control_dist_km)/speed[1]

    #brevet dist of 600km
    elif (((brevet_dist_km==600) and (400 < control_dist_km <= 720)) or (400 < control_dist_km <= 600)):
        if(600 <= control_dist_km <= buff and brevet_dist_km == 600):
            closing_time = 40
        else:
            closing_time = (control_dist_km)/speed[2]

    #brevet dist of 1000km
    elif (((brevet_dist_km==1000) and (600 < control_dist_km <= 1200)) or (600 < control_dist_km <= 1000)):
        if(1000 <= control_dist_km <= buff and brevet_dist_km == 1000):
            closing_time = 75
        else:
            previous = (600/speed[2])
            closing_time = previous + (control_dist_km-600)/speed[3]

    #brevet dist of >1000km
    elif(control_dist_km > 1000 and control_dist_km <= 1300):
        previous = (600/speed[2]) + (1000/speed[3])
        closing_time = previous + (control_dist_km-1000)/speed[4]

    hours = closing_time // 1
    minutes = round((closing_time % 1) * 60)
    #print(closing_time)

    time = arrow.get(brevet_start_time)
    time = time.shift(hours=+hours, minutes=+minutes)
    #time.shift(minutes=+minutes)
    print("closing time: " + str(time))
    return time.isoformat()
"""
print(open_time(350, 400, "2017-01-01T00:00:00+00:00"))
open_time(120, 200, "2017-01-01T00:00:00+00:00")
open_time(175, 200, "2017-01-01T00:00:00+00:00")
open_time(200, 200, "2017-01-01T00:00:00+00:00")
print(close_time(60, 200, "2017-01-01T00:00:00+00:00"))
close_time(120, 200, "2017-01-01T00:00:00+00:00")
close_time(175, 200, "2017-01-01T00:00:00+00:00")
"""
close_time(480, 400, "2017-01-01T00:00:00+00:00")


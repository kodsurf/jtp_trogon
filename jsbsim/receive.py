import socket
from scanf import scanf
import matplotlib.pyplot as plt
import numpy as np
from funcinclude import *
import time as t

UDP_IP = "127.0.0.1"
UDP_PORT = 5138

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


v_kts = np.array([])
altitude = np.array([])
time = np.array([])
pose_latlon = np.array([[],[],[]])



def parse(strMsg): # parse fix
    #pattern = "GGA,%s,%f,%s,%f,%s,%d,%d,%f,%f,%s"
    #pattern = "$GPGGA,%s,%f,%s,%f,%s,%d,%d,%f,%f,%s"
    #pattern = "$:          %f,    %f"
    #$:         10.8,    47.83197,    16.25626,    8614.223,    117.8657,   -3.140063,   -1.100116,    3.140674
    #pattern = "$:          %f,    %f,    %f,    %f,    %f,  %f,    %f,     %f"
    pattern = "$:         %f,    %f,    %f,    %f,    %f,   %f,   %f,    %f"
    time = None
    lat = None
    lon = None
    alt = None
    vel = None
    roll_rad = None
    pitch_rad = None
    heading_rad = None

    try:
        result = scanf(pattern,strMsg)
        print result
        time = result[0]
        lat = result[1]
        lon = result[2]
        alt = result[3]
        vel = result[4]
        roll_rad = result[5]
        pitch_rad = result[6]
        heading_rad = result[7]
    except:
        #print "Wrong NMEA GPGGA format"
        pass
          

    return time,lat,lon,alt,vel,roll_rad,pitch_rad,heading_rad


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    msg = "$: "+data+"#END"
    print msg
    time,lat,lon,alt,vel,roll_rad,pitch_rad,heading_rad = parse(msg)
    #t.sleep(1)
    try:
    	roll = roll_rad*360/(2*math.pi)
    	pitch = pitch_rad*360/(2*math.pi)
    	yaw = heading_rad*360/(2*math.pi)
    	print "time ="+str(time)+" lat="+str(lat)+" lon="+str(lon)+" alt="+str(alt)+" vel="+str(vel)
    	print "roll="+str(roll_rad)+" pitch="+str(pitch_rad)+" heading="+str(heading_rad)
    	plt.figure(1)
    	plt.scatter(time,vel)
    	plt.xlabel('time (s)')
    	plt.ylabel('velocity (knots)')
    	plt.pause(0.001)# plot every 0.5
    except:
    	print "None error"
plt.show()
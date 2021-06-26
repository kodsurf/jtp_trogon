import socket
from scanf import scanf
import matplotlib.pyplot as plt
import numpy as np
from funcinclude import *
import time as t
import math
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5138

# ECEF reference point
lat0 = 47.8303295
lon0 = 16.2562515
alt0 = 0

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)

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


def extract_nums(text):
    for item in text.split(','):
        try:
            yield float(item)
        except ValueError:
            pass


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #msg = "$: "+data+"#END"
    msg = data
    print msg
    try:
    	#time,lat,lon,alt,vel,roll_rad,pitch_rad,heading_rad = parse(msg)
    	#t.sleep(1)
    	result= list(extract_nums(msg))
    	time = result[0]
    	lat = result[1]
    	lon = result[2]
    	alt = result[3]
    	vel = result[4]
    	roll_rad = result[5]
    	pitch_rad = result[6]
    	heading_rad = result[7]
    	left_aileron = result[8]
    	right_aileron = result[9]
    	elevator = result[10]
    	rudder = result[11]
    	alpha = result[12]

    	x,y,z = geodetic_to_enu(lat,lon,alt,lat0,lon0,alt0)
    	print "time ="+str(time)+" lat="+str(lat)+" lon="+str(lon)+" alt="+str(alt)+" vel="+str(vel)
    	print "roll="+str(roll_rad)+" pitch="+str(pitch_rad)+" heading="+str(heading_rad)

    	print "CONTROLLS ------"
    	print "aileron LEFT "+str(left_aileron)+ " RIGHT "+str(right_aileron)
    	print "elevator "+str(elevator)
    	print "rudder "+str(rudder)
    	print "angle of attack "+str(alpha)


    	plt.figure(1)
    	plt.scatter(time,vel)
    	plt.xlabel('time (s)')
    	plt.ylabel('velocity (knots)')
    	#plt.pause(0.001)# plot every 0.5
    	if time > 60:
    		plt.savefig('vel_time.png')

    	plt.figure(2)
    	plt.scatter(time,alt)
    	plt.xlabel('time (s)')
    	plt.ylabel('alt (m)')
    	#plt.pause(0.001)# plot every 0.5
    	if time > 60:
    		plt.savefig('alt_time.png')

    	plt.figure(3)
    	plt.scatter(time,alpha)
    	plt.xlabel('Time [S]')
    	plt.ylabel('Angle of attack [DEG]')
    	if time > 60:
    		plt.savefig('alpha_time.png')


    	plt.figure(4)
    	plt.scatter(x,y)
    	plt.xlabel('X (m)')
    	plt.ylabel('Y (m)')
    	if time > 60:
    		plt.savefig('xy.png')

    	plt.figure(5)
    	plt.scatter(time,pitch_rad)
    	plt.xlabel('Time [S]')
    	plt.ylabel('Pitch [DEG]')
    	if time > 60:
    		plt.savefig('pitch_time.png')

    	plt.figure(6)
    	plt.scatter(time,elevator)
    	plt.xlabel('time [S]')
    	plt.ylabel('Elevator Position [DEG]')
    	if time > 60:
    		plt.savefig('elevator_time.png')
    		break


    	plt.pause(0.001)# plot every 0.5
    except:
    	print "ERROR"

    '''
    time = result[1]
    lat = result[1]
    lon = result[2]
    alt = result[3]
    vel = result[4]
    roll_rad = result[5]
    pitch_rad = result[6]
    heading_rad = result[7]
    roll = roll_rad*360/(2*math.pi)
    pitch = pitch_rad*360/(2*math.pi)
    yaw = heading_rad*360/(2*math.pi)
    roll = math.normalize(-180,180,roll)
    pitch = math.normalize(-180,180,pitch)
    yaw = math.normalize(0,360,yaw)
    print "time ="+str(time)+" lat="+str(lat)+" lon="+str(lon)+" alt="+str(alt)+" vel="+str(vel)
    print "roll="+str(roll_rad)+" pitch="+str(pitch_rad)+" heading="+str(heading_rad)
    plt.figure(1)
    plt.scatter(time,vel)
    plt.xlabel('time (s)')
    plt.ylabel('velocity (knots)')
    plt.pause(0.001)# plot every 0.5
    '''



    '''
    try:
    	time = result[0]
        lat = result[1]
        lon = result[2]
        alt = result[3]
        vel = result[4]
        roll_rad = result[5]
        pitch_rad = result[6]
        heading_rad = result[7]

    	roll = roll_rad*360/(2*math.pi)
    	pitch = pitch_rad*360/(2*math.pi)
    	yaw = heading_rad*360/(2*math.pi)

    	roll = math.normalize(-180,180,roll)
    	pitch = math.normalize(-180,180,pitch)
    	yaw = math.normalize(0,360,yaw)
    	print "time ="+str(time)+" lat="+str(lat)+" lon="+str(lon)+" alt="+str(alt)+" vel="+str(vel)
    	print "roll="+str(roll_rad)+" pitch="+str(pitch_rad)+" heading="+str(heading_rad)
    	plt.figure(1)
    	plt.scatter(time,vel)
    	plt.xlabel('time (s)')
    	plt.ylabel('velocity (knots)')
    	plt.pause(0.001)# plot every 0.5
    except:
    	print "None error"
    '''
plt.show()
import jsbsim
import numpy as np
import matplotlib.pyplot as plt
import keyboard  # using module keyboard
from funcinclude import *


# ECEF reference point
lat0 = 47.8303295
lon0 = 16.2562515
alt0 = 0
plot_delta = 0.5 # PLOT EVERY seconds

fdm = jsbsim.FGFDMExec('.', None)
#fdm.load_script('scripts/737_cruise.xml', delta_t=0.1,initfile='cruise_init.xml')
#fdm.load_script('scripts/737_custom.xml', delta_t=0.1,initfile='custom.xml')
#fdm.load_script('scripts/c172_cruise_8K.xml', delta_t=0.1,initfile='reset00.xml')

fdm.load_model("ogel")
#fdm.load_model("c172p")
#fdm.load_model("trogon")
#fdm.load_model("c172x")



frame_duration = fdm.get_delta_t() 
fdm.set_dt(0.1) # set dt  # CALCULATE NEW FRAME EVER dt


fdm.print_property_catalog() # list avaliable properties


v_kts = np.array([])
altitude = np.array([])
time = np.array([])

pose_latlon = np.array([[],[],[]])
pose_cartesian = np.array([[],[],[]])

# INITIAL CONDITIONS

fdm.set_property_value("ic/vc-kts",130) #Calibrated airspeed initial condition in knots

#fdm.set_property_value("ic/v-fps",130) 
#fdm.set_property_value("ic/v-fps",0) 
#fdm.set_property_value("ic/w-fps",0) 


#fdm.set_property_value("ic/gamma-rad",0) 
#fdm.set_property_value("ic/phi-deg",0) 
#fdm.set_property_value("ic/theta-deg",6.47) 
#fdm.set_property_value("ic/psi-true-deg",200)
fdm.set_property_value("ic/h-sl-ft",10000.0) 

#fdm.set_property_value("ic/lat-geod-deg",47.8303295)
#fdm.set_property_value("ic/long-gc-deg",16.2562515)
#fdm.set_property_value("PIZDA",777.0)


fdm.run_ic()




#SET STARTING POINT
'''
fdm.set_property_value("position/h-sl-meters",6000) # set altitude to 5000m
fdm.set_property_value("position/lat-gc-deg",47.8303295) # set altitude to 5000m
fdm.set_property_value("position/lon-gc-deg",16.2562515) # set altitude to 5000m
'''

# TURN ON  engines
fdm.set_property_value("propulsion/engine/set-running",1) 
#fdm.set_property_value("propulsion/engine[1]/set-running",1)
#fdm.set_property_value("propulsion/engine/set-running",0) 

#TRIM
#fdm.set_property_value("simulation/do_simple_trim",1)


#fdm.set_property_value("simulation/write-state-file",0)
#fdm.set_property_value("thrust",50) # external force DIRECTION 0 0 1

flag = True
elevator_cmd=0 # initialize elevator in neutral position
throttle_cmd = 0
aileron_cmd = 0
rudder_cmd = 0
while fdm.run() and fdm.get_sim_time()<5000:


	current_time = fdm.get_sim_time()
	#time = np.append(time,current_time)

	if current_time > 5 and flag:

		fdm.set_property_value("fcs/roll-trim-cmd-norm",0)# roll trim
		fdm.set_property_value("fcs/pitch-trim-cmd-norm",0)# roll trim
		fdm.set_property_value("fcs/yaw-trim-cmd-norm",0)# roll trim

		fdm.set_property_value("simulation/do_simple_trim",1)
		flag = False
	
	print "current time="+str(current_time)

	v = fdm.get_property_value("velocities/ve-kts")
	print "Velocity (kts) = "+str(v)

	pitch = fdm.get_property_value("attitude/pitch-rad")
	print "Pitch RAD = "+str(pitch)
	
	alt = fdm.get_property_value("position/h-sl-meters")
	print "Sea level alt = "+str(alt)

	test = fdm.get_property_value("ic/vt-fps")
	print "test = "+str(test)

	lat = fdm.get_property_value("position/lat-gc-deg")
	lon = fdm.get_property_value("position/lon-gc-deg")
	alt = fdm.get_property_value("position/h-sl-meters")

	x,y,z = geodetic_to_enu(lat,lon,alt,lat0,lon0,alt0)
	current_pose_cartesian= np.array([[x],[y],[z]])
	#pose_cartesian = np.append(pose_cartesian,current_pose_cartesian)
	print "X Y Z "+ str(current_pose_cartesian)



	curr_lat_lon_alt= np.array([[lat],[lon],[alt]])
	#pose_latlon = np.append(pose_latlon,curr_lat_lon_alt)

	print "LAT LON ALT = "+str(curr_lat_lon_alt)

	#fdm.set_property_value("propulsion/engine/power-hp",1000)
	engine_power = fdm.get_property_value("propulsion/engine/power-hp")
	print "ENGINE POWER = "+str(engine_power)

	#fdm.set_property_value("thrust",77777)
	thrust = fdm.get_property_value("thrust")
	print "thrust = "+str(thrust)

	elevator_deg = fdm.get_property_value("fcs/elevator-pos-deg")
	print "ELEVATOR POSITION "+ str(elevator_deg)+" DEG"

	elevator_pose_norm = fdm.get_property_value("fcs/elevator-pos-norm")
	print "ELEVATOR NORMALIZED "+ str(elevator_pose_norm)

	left_aileron = fdm.get_property_value("fcs/left-aileron-pos-deg")
	right_aileron = fdm.get_property_value("fcs/right-aileron-pos-deg")
	print "AILERON LEFT "+ str(left_aileron) + " RIGHT "+str(right_aileron)


	rudder = fdm.get_property_value("fcs/rudder-pos-deg")
	print "RUDDER "+str(rudder)




	engine_thrust = fdm.get_property_value("propulsion/engine/thrust-lbs")
	print "Engine thrust "+ str(engine_power)+ " lbs"



	# ELEVATOR   --------------------------------
	if keyboard.is_pressed('w'):
		#print "W PRESSED"
		#fdm.set_property_value("fcs/elevator-pos-deg",elevator_deg+10.0) #add altitude if  button is pressed
		elevator_cmd = elevator_cmd +0.05
		fdm.set_property_value("fcs/elevator-cmd-norm",elevator_cmd) #add altitude if  button is pressed

		#elevator_deg = fdm.get_property_value("fcs/elevator-pos-deg")
		#print "ELEVATOR INCREASES "+ str(elevator_deg)+" DEG"



	if keyboard.is_pressed('s'):
		#fdm.set_property_value("fcs/elevator-pos-deg",elevator_deg-10) Absolute position of elevator
		elevator_cmd = elevator_cmd -0.05
		fdm.set_property_value("fcs/elevator-cmd-norm",elevator_cmd) #NORMALIZED COMMAND
		#elevator_deg = fdm.get_property_value("fcs/elevator-pos-deg")

		#print "ELEVATOR DECREASE "+ str(elevator_deg)+" DEG"

	# AILERONS -----------------------

	if keyboard.is_pressed('d'):
		aileron_cmd = aileron_cmd +0.05
		fdm.set_property_value("fcs/aileron-cmd-norm",aileron_cmd) #NORMALIZED COMMAND
		print "AILERON INCREASE"

	if keyboard.is_pressed('a'):
		aileron_cmd = aileron_cmd -0.05
		fdm.set_property_value("fcs/aileron-cmd-norm",aileron_cmd) #NORMALIZED COMMAND
		print "AILERON INCREASE"

	# RUDDER -------------------------------


	if keyboard.is_pressed('z'):
		rudder_cmd = rudder_cmd+0.05
		fdm.set_property_value("fcs/rudder-cmd-norm",rudder_cmd) #NORMALIZED COMMAND
		print "RUDDER INCREASE"

	if keyboard.is_pressed('c'):
		rudder_cmd = rudder_cmd-0.05
		fdm.set_property_value("fcs/rudder-cmd-norm",rudder_cmd) #NORMALIZED COMMAND
		print "RUDDER DECREASE"










	



	### THROTLE
	if keyboard.is_pressed('t'):
		throttle_cmd = throttle_cmd +0.05
		fdm.set_property_value("fcs/throttle-cmd-norm",throttle_cmd)
		print "THROTTLE INCREASE "

	if keyboard.is_pressed('g'):
		throttle_cmd = throttle_cmd +0.05
		fdm.set_property_value("fcs/throttle-cmd-norm",throttle_cmd)
		print "THROTTLE DECREASE "


	if keyboard.is_pressed('space'):
		print "SET ALL CONTROLLS FLIGHT CONTROLS TO NEUTRAL"
		fdm.set_property_value("fcs/elevator-cmd-norm",0)
		fdm.set_property_value("fcs/aileron-cmd-norm",0)
		fdm.set_property_value("fcs/rudder-cmd-norm",0)








	#print "possition = "
	#print aircraft.get_xyz_rp()
	#print "forces = "
	#print aerodynamics.get_forces()

	#v_kts = np.append(v_kts,v)
	#altitude = np.append(altitude,alt)

	#plt.clf()
	plt.figure(1)
	if (current_time%plot_delta)<0.1:
		plt.scatter(current_time,v)

	#plt.scatter(current_time,v)
	plt.xlabel('time (s)')
	plt.ylabel('velocity (knots)')

	plt.figure(2)
	if (current_time%plot_delta)<0.1:
		plt.scatter(current_time,alt)
	plt.xlabel('time (s)')
	plt.ylabel('altitude (m)')
	#plt.pause(0.05)

	plt.figure(3)
	if (current_time%plot_delta)<0.1:
		plt.scatter(x,y)
	plt.xlabel('x')
	plt.ylabel('y')
	#plt.pause(0.05)

	#fdm.set_property_value("simulation/write-state-file",0)
	STATUS_PLOTS = plt.figure(4).clf()
	x = [1, 2, 4]
	#plt.plot(x)
	plt.text(1, 1, '*',)
	elevator_text = "ELEVATOR DEG -----   "+str(round(elevator_deg,2))
	plt.text(0.1, 0.5, elevator_text)

	aileron_text = "AILERON------  LEFT "+ str(round(left_aileron,2)) + " RIGHT "+str(round(right_aileron,2))
	plt.text(0.1, 0.55, aileron_text)

	rudder_text = "RUDDER------  LEFT "+ str(round(rudder,2))
	plt.text(0.1, 0.60, rudder_text)



	plt.pause(0.05)








print v_kts.size
print altitude.size


#plt.plot(v_kts,altitude)
plt.show()

















#fdm.print_simulation_configuration()

# -----------------------------------------------
'''
fdm.run_ic()

while fdm.run():
	pass

# -----------------------------------

#print dir(fdm.set_logging_rate)
path = fdm.get_aircraft_path()
print path



#output_filename = fdm.get_output_filename(0)
#print output_filename



output_filename = fdm.get_output_filename(0)
print output_filename

property_value = fdm.get_property_value("Q")
print property_value
'''
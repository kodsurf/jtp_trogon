import jsbsim
import numpy as np
import matplotlib.pyplot as plt
import keyboard  # using module keyboard
from funcinclude import *


# ECEF reference point
lat0 = 47.8303295
lon0 = 16.2562515
alt0 = 0

fdm = jsbsim.FGFDMExec('.', None)
#fdm.load_script('scripts/737_cruise.xml', delta_t=0.1,initfile='cruise_init.xml')
#fdm.load_script('scripts/737_custom.xml', delta_t=0.1,initfile='custom.xml')

fdm.load_model("ogel")
#fdm.load_model("c172p")
#fdm.load_model("trogon")



frame_duration = fdm.get_delta_t() 
fdm.set_dt(0.1) # set dt
fdm.set_logging_rate(0.5)


fdm.set_output_filename(0,"testOutTT.csv")
fdm.enable_output()


#fdm.run_ic()
fdm.print_property_catalog() # list avaliable properties


#atm = fdm.get_atmosphere()
#aircraft = fdm.get_aircraft()
#aerodynamics = fdm.get_aerodynamics()



#print aircraft.get_xyz_rp()
#print aerodynamics.get_forces()


v_kts = np.array([])
altitude = np.array([])
time = np.array([])

pose_latlon = np.array([[],[],[]])
pose_cartesian = np.array([[],[],[]])

# INITIAL CONDITIONS



fdm.set_property_value("ic/u-fps",0) 
fdm.set_property_value("ic/v-fps",0) 
fdm.set_property_value("ic/w-fps",0) 


#fdm.set_property_value("ic/gamma-rad",0) 
#fdm.set_property_value("ic/phi-deg",0) 
#fdm.set_property_value("ic/theta-deg",6.47) 
#fdm.set_property_value("ic/psi-true-deg",200)
fdm.set_property_value("ic/h-sl-ft",10000.0) 

fdm.set_property_value("ic/lat-geod-deg",47.8303295)
fdm.set_property_value("ic/long-gc-deg",16.2562515)
fdm.set_property_value("PIZDA",777.0)


fdm.run_ic()




#SET STARTING POINT
'''
fdm.set_property_value("position/h-sl-meters",6000) # set altitude to 5000m
fdm.set_property_value("position/lat-gc-deg",47.8303295) # set altitude to 5000m
fdm.set_property_value("position/lon-gc-deg",16.2562515) # set altitude to 5000m
'''

# TURN ON 737 engines
#fdm.set_property_value("propulsion/engine[0]/set-running",1) 
#fdm.set_property_value("propulsion/engine[1]/set-running",1)
#fdm.set_property_value("propulsion/engine/set-running",0) 

#TRIM
#fdm.set_property_value("simulation/do_simple_trim",1)


fdm.set_property_value("simulation/write-state-file",0)
fdm.set_property_value("thrust",50) # external force DIRECTION 0 0 1

flag = True
while fdm.run() and fdm.get_sim_time()<20:


	current_time = fdm.get_sim_time()
	#time = np.append(time,current_time)

	if current_time > 5 and flag:
		#fdm.set_property_value("simulation/do_simple_trim",1)
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



	if keyboard.is_pressed('q'):
		fdm.set_property_value("position/h-sl-meters",alt+10) #add altitude if button is pressed



	#print "possition = "
	#print aircraft.get_xyz_rp()
	#print "forces = "
	#print aerodynamics.get_forces()

	#v_kts = np.append(v_kts,v)
	#altitude = np.append(altitude,alt)

	#plt.clf()
	plt.figure(1)
	plt.scatter(current_time,v)
	plt.xlabel('time (s)')
	plt.ylabel('velocity (knots)')
	#plt.pause(0.05)

	plt.figure(2)
	plt.scatter(current_time,alt)
	plt.xlabel('time (s)')
	plt.ylabel('altitude (m)')
	#plt.pause(0.05)

	plt.figure(3)
	plt.scatter(x,y)
	plt.xlabel('x')
	plt.ylabel('y')
	plt.pause(0.05)

	fdm.set_property_value("simulation/write-state-file",0)






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
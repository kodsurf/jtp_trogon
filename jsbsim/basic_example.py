import jsbsim
import numpy as np



fdm = jsbsim.FGFDMExec('.', None)
fdm.load_model("trogon")
fdm.set_dt(0.1) # set dt
fdm.set_logging_rate(0.5)


fdm.print_property_catalog() # list avaliable properties


fdm.set_property_value("ic/u-fps",0) 
fdm.set_property_value("ic/v-fps",0) 
fdm.set_property_value("ic/w-fps",0) 
fdm.set_property_value("ic/gamma-rad",0) 
fdm.set_property_value("ic/phi-deg",0) 
fdm.set_property_value("ic/theta-deg",6.47) 
fdm.set_property_value("ic/psi-true-deg",200)
fdm.set_property_value("ic/h-sl-ft",10000.0) 
fdm.set_property_value("ic/lat-geod-deg",47.8303295)
fdm.set_property_value("ic/long-gc-deg",16.2562515)

fdm.run_ic()



while fdm.run() and fdm.get_sim_time()<20:


	current_time = fdm.get_sim_time()
	
	
	print "current time="+str(current_time)

	v = fdm.get_property_value("velocities/ve-kts")
	print "Velocity (kts) = "+str(v)

	pitch = fdm.get_property_value("attitude/pitch-rad")
	print "Pitch RAD = "+str(pitch)
	
	alt = fdm.get_property_value("position/h-sl-meters")
	print "Sea level alt = "+str(alt)

	lat = fdm.get_property_value("position/lat-gc-deg")
	lon = fdm.get_property_value("position/lon-gc-deg")
	alt = fdm.get_property_value("position/h-sl-meters")

	print "lat ="+str(lat)+ " lon="+str(lon)+"alt= "+str(alt)






















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
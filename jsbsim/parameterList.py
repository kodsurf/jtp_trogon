import jsbsim
import numpy as np
import matplotlib.pyplot as plt

import keyboard  # using module keyboard

if keyboard.is_pressed('q'):
	print "ffff"
else:
	print "huj"

fdm = jsbsim.FGFDMExec('.', None)
atmosphere = jsbsim.FGAtmosphere()



#fdm.load_script('scripts/737_custom.xml', delta_t=0.1,initfile='reset00.xml')
#fdm.load_script('scripts/737_custom.xml', delta_t=0.1,initfile='cruise_init.xml')

#fdm.load_model("trogon")
#fdm.load_model("c172p")
fdm.load_model("ogel")

fdm.set_output_filename(0,"testOut.csv")
fdm.enable_output()

frame_duration = fdm.get_delta_t() 



fdm.run_ic()
fdm.print_property_catalog() # list avaliable properties




alt = fdm.get_property_value("propulsion/engine/set-running")

fdm.set_property_value("propulsion/engine/set-running",1)
alt = fdm.get_property_value("propulsion/engine/set-running")
print "Sea level alt = "+str(alt)


atm = fdm.get_atmosphere()
aircraft = fdm.get_aircraft()
aerodynamics = fdm.get_aerodynamics()


print atm.get_temperature(10)
print aircraft.get_xyz_rp()
print aerodynamics.get_forces()
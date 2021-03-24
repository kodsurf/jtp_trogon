import jsbsim

fdm = jsbsim.FGFDMExec('.', None)
fdm.load_script('scripts/c1721.xml')
fdm.run_ic()

while fdm.run():
  pass
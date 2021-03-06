from startup._common_imports import *  # @UnusedWildImport

if not GDA:    
    import startup._demo
else:
#     import __main__  # @UnresolvedImport
    from __main__ import tth,th,chi,pgm_energy, simtth,simth,simchi,simalpha # @UnresolvedImport

LOCAL_MANUAL = ""

SIM_MODE=False

### Create dummy scannables ###
if GDA:  
    ###map GDA scannable to diffcalc axis name###
    phi = Dummy('phi')
    _fourc = ScannableGroup('_fourc', (tth, th, chi, phi))
    en=pgm_energy
    if float(en.getPosition()) == 0: # no energy value - dummy mode
        en(800)
else:
    #Create dummy axes to run outside GDA in IPython#   
    delta = Dummy('delta')
    eta = Dummy('eta')
    chi = Dummy('chi')
    phi = Dummy('phi')
    _fourc = ScannableGroup('_fourc', (delta, eta, chi, phi))
    en = Dummy('en')
    en(800)

en.level = 3

### Configure and import diffcalc objects ###
ESMTGKeV = 0.001
settings.hardware = ScannableHardwareAdapter(_fourc, en, ESMTGKeV)
settings.geometry = diffcalc.hkl.you.geometry.FourCircle()  # @UndefinedVariable
settings.energy_scannable = en
settings.axes_scannable_group= _fourc
settings.energy_scannable_multiplier_to_get_KeV = ESMTGKeV
 
from diffcalc.gdasupport.you import *  # @UnusedWildImport

if GDA:
    print "Running in GDA --- aliasing commands"
    alias_commands(globals())
 
### Load the last ub calculation used
lastub()
 
### Set i10 specific limits
def setLimitsAndCuts(delta,eta,chi,phi):
    ''' set motor limits for diffcalc, these are within the actual motor limits
    '''
    setmin(delta, -60.0)
    setmax(delta, 165.0) 
    setmin(eta, -94.408)
    setmax(eta, 190.591)
    setmin(chi, 85.5)
    setmax(chi, 94.5)
    setmin(phi, 0)
    setmax(phi, 360.0)
    print "Current hardware limits set to:"
    hardware()

if GDA:
    setLimitsAndCuts(tth,th,chi,phi)
else:
    setLimitsAndCuts(delta,eta,chi,phi)

if GDA:
    def swithMotors(delta, mu, eta, chi, phi):
        import __main__
        from diffcalc.dc import dcyou as _dc
        
        ### update Wrap i21 names to get diffcalc names
        _fourc = ScannableGroup('_fourc', (delta, mu, eta, chi, phi))
        #update diffcalc objects
        __main__.settings.hardware = ScannableHardwareAdapter(_fourc, __main__.en, ESMTGKeV)  # @UndefinedVariable
        __main__.settings.geometry = diffcalc.hkl.you.geometry.FourCircle()  # @UndefinedVariable
        __main__.settings.energy_scannable = __main__.en  # @UndefinedVariable
        __main__.settings.axes_scannable_group= _fourc
        __main__.settings.energy_scannable_multiplier_to_get_KeV = ESMTGKeV
        
        __main__.fourc=DiffractometerScannableGroup('fourc', _dc, _fourc)
        __main__.hkl = Hkl('hkl', _fourc, _dc)
        __main__.h, __main__.k, __main__.l = hkl.h, hkl.k, hkl.l

        from diffcalc.gdasupport.you import _virtual_angles
        from diffcalc.gdasupport.scannable.simulation import SimulatedCrystalCounter
        from diffcalc.gdasupport.scannable.wavelength import Wavelength
        __main__.hklverbose = Hkl('hklverbose', _fourc, _dc, _virtual_angles)
        __main__.wl = Wavelength('wl',__main__.en,ESMTGKeV)  # @UndefinedVariable
        __main__.ct = SimulatedCrystalCounter('ct', _fourc, __main__.settings.geometry,__main__.wl)  # @UndefinedVariable
        
    def stopMotors(delta, eta, chi, phi):
        delta.stop()
        eta.stop()
        chi.stop()
        phi.stop()
        
    def simdc():
        ''' switch to use dummy motors in diffcalc
        '''
        print "Stop real motors"
        stopMotors(tth,th,chi,phi)
        
        global SIM_MODE
        SIM_MODE=True
        import __main__
        __main__.en=Dummy("en")
        print "Set energy to 12398.425 eV in simulation mode!"
        __main__.en(12398.425) #1 Angstrom wavelength @UndefinedVariable
        print "Switch to simulation motors"
        swithMotors(simtth,simalpha,simth,simchi,phi)
        setLimitsAndCuts(simtth,simalpha,simth,simchi,phi)
        
    def realdc():
        ''' switch to use real motors in diffcalc
        '''
        print "Stop simulation motors"
        stopMotors(simtth,simalpha,simth,simchi,phi)
        
        global SIM_MODE
        SIM_MODE=False
        import __main__
        print "Set energy to current beamline energy in real mode!"
        __main__.en=pgm_energy
        print "Switch to real motors"
        swithMotors(tth,th,chi,phi)
        setLimitsAndCuts(tth,th,chi,phi)
     
    from gda.jython.commands.GeneralCommands import alias  # @UnresolvedImport
    print "Created commands: 'simdc' and 'realdc' to switch between real and simulated motors."
    alias("simdc")
    alias("realdc")

### Demo ###
if not GDA:
    demo = demo = startup._demo.Demo(globals(), 'fourc')

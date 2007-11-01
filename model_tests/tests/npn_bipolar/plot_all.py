#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import pylab
import os



def plot_dc_current_gain():
    mm=[]

    mm.append(("0 C", pylab.load("dc_current_gain_t0.data")))
    mm.append(("25 C",pylab.load("dc_current_gain_t25.data")))
    mm.append(("50 C",pylab.load("dc_current_gain_t50.data")))
    mm.append(("75 C",pylab.load("dc_current_gain_t75.data")))
    mm.append(("100 C",pylab.load("dc_current_gain_t100.data")))

    for t,m in mm:
        pylab.semilogx(-m[:,1]*1000,m[:,1]/m[:,2],label=t)
    pylab.xlabel("Ic [mA]")
    pylab.ylabel("hfe")
    pylab.grid()
    pylab.legend(loc="best")
    pylab.savefig("dc_current_gain.png",dpi=80)
    pylab.close()

    for t,m in mm:
        pylab.semilogx(-m[:,1]*1000,m[:,3]*1000,label=t)
    pylab.xlabel("Ic [mA]")
    pylab.ylabel("V BE [mV]")
    pylab.grid()
    pylab.legend(loc='best')
    pylab.savefig("base_emitter_voltage.png",dpi=80)
    pylab.close()

def plot_saturation_voltages():
    mm=[]

    mm.append(("0 C", pylab.load("saturation_voltages_t0.data")))
    mm.append(("25 C",pylab.load("saturation_voltages_t25.data")))
    mm.append(("50 C",pylab.load("saturation_voltages_t50.data")))
    mm.append(("75 C",pylab.load("saturation_voltages_t75.data")))
    mm.append(("100 C",pylab.load("saturation_voltages_t100.data")))

    for t,m in mm:
        pylab.semilogx(-m[:,1]*1000,m[:,3]*1000,label=t)
    pylab.xlabel("Ic [mA]")
    pylab.ylabel("VCE sat [mV]")
    pylab.grid()
    pylab.legend(loc='best')
    pylab.savefig("vce_saturation_voltage.png",dpi=80)
    pylab.close()

    for t,m in mm:
        pylab.semilogx(-m[:,1]*1000,m[:,2]*1000,label=t)
    pylab.xlabel("Ic [mA]")
    pylab.ylabel("V BE [mV]")
    pylab.grid()
    pylab.legend(loc='best')
    pylab.savefig("vbe_saturation_voltage.png",dpi=80)
    pylab.close()


#################### MAIN

os.system("gnetlist -g spice-sdb -o dc_current_gain.net dc_current_gain.sch")
os.system("gnetlist -g spice-sdb -o saturation_voltages.net saturation_voltages.sch")
os.system("gnucap -b simulate.gnucap")
plot_dc_current_gain()
plot_saturation_voltages()


#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Gnuplot
import pylab  #TODO: replace pylab.load function
import os



def plot_dc_current_gain():
    mm=[]

    mm.append(("0 C", pylab.load("dc_current_gain_t0.data")))
    mm.append(("25 C",pylab.load("dc_current_gain_t25.data")))
    mm.append(("50 C",pylab.load("dc_current_gain_t50.data")))
    mm.append(("75 C",pylab.load("dc_current_gain_t75.data")))
    mm.append(("100 C",pylab.load("dc_current_gain_t100.data")))

    g = Gnuplot.Gnuplot()
    g('set data style lines')
    g('set logscale x')
    g('set terminal png')
    g('set output "dc_current_gain.png"')
    g.xlabel("Ic [mA]")
    g.ylabel("hfe")
    g('set grid')
    datasets = []
    for t,m in mm:
        datasets.append(Gnuplot.Data(-m[:,1]*1000, m[:,1]/m[:,2], title = t))
    g.plot(*datasets)

    g('set output "base_emitter_voltage.png"')
    g.ylabel("V BE [mV]")
    g('set key left top')
    datasets = []
    for t,m in mm:
        datasets.append(Gnuplot.Data(-m[:,1]*1000, m[:,3]*1000, title = t))
    g.plot(*datasets)

def plot_saturation_voltages():
    mm=[]

    mm.append(("0 C", pylab.load("saturation_voltages_t0.data")))
    mm.append(("25 C",pylab.load("saturation_voltages_t25.data")))
    mm.append(("50 C",pylab.load("saturation_voltages_t50.data")))
    mm.append(("75 C",pylab.load("saturation_voltages_t75.data")))
    mm.append(("100 C",pylab.load("saturation_voltages_t100.data")))

    g = Gnuplot.Gnuplot()
    g('set data style lines')
    g('set logscale xy')
    g('set terminal png')
    g('set output "vce_saturation_voltage.png"')
    g.xlabel("Ic [mA]")
    g.ylabel("VCE sat [mV]")
    g('set grid')
    g('set key right bottom')
    datasets = []
    for t,m in mm:
        ## only plot the values where Vce sat is smaller 2.00
        firstind = pylab.find(m[:,3] < 2.0)[0]
        datasets.append(Gnuplot.Data(-m[firstind:,1]*1000, m[firstind:,3]*1000, title = t))
    g.plot(*datasets)

    g('set logscale x')
    g('set output "vbe_saturation_voltage.png"')
    g('set key left top')
    g.ylabel("V BE sat [mV]")
    datasets = []
    for t,m in mm:
        datasets.append(Gnuplot.Data(-m[:,1]*1000, m[:,2]*1000, title = t))
    g.plot(*datasets)


#################### MAIN

os.system("gnetlist -g spice-sdb -l ../../../../scripts/geda-parts.scm -o dc_current_gain.net dc_current_gain.sch")
os.system("gnetlist -g spice-sdb -l ../../../../scripts/geda-parts.scm -o saturation_voltages.net saturation_voltages.sch")
os.system("gnucap -b simulate.gnucap")
plot_dc_current_gain()
plot_saturation_voltages()


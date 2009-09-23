#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Gnuplot
import pylab  #TODO: replace pylab.load function
import popen2
import sys
import numpy


def plot_dc_current():
    mm=[]
    ret = 0

    mm.append(("0 C", pylab.load("dc_current_t0.data")))
    mm.append(("25 C",pylab.load("dc_current_t25.data")))
    mm.append(("50 C",pylab.load("dc_current_t50.data")))
    mm.append(("75 C",pylab.load("dc_current_t75.data")))
    mm.append(("100 C",pylab.load("dc_current_t100.data")))

    g = Gnuplot.Gnuplot()
    g('set data style lines')
    g('set terminal png')
    g('set output "dc_IB.png"')
    g.xlabel("Uin [V]")
    g.ylabel("Iin [mA]")
    g('set grid')
    g('set key left top')
    datasets = []
    for t,m in mm:
        if numpy.any(-m[:,1]< -0.001) or numpy.any(-m[:,1]>1.0):
            print "input current out of expected range [-0.001, 1.0]"
            ret = 1
        datasets.append(Gnuplot.Data(m[:,0], -m[:,1]*1000, title = t))
    g.plot(*datasets)

    g('set output "dc_IC.png"')
    g.ylabel("IC [mA]")
    datasets = []
    for t,m in mm:
        if numpy.any(-m[:,2]< -0.001) or numpy.any(-m[:,2]>100.0):
            print "collector current out of expected range [-0.001, 100.0]"
            ret = 1
        datasets.append(Gnuplot.Data(m[:,0], -m[:,2]*1000, title = t))
    g.plot(*datasets)

    return ret

#################### MAIN



ME = sys.argv[0] + ": "

command = "gnetlist -g spice-sdb -l ../../../../scripts/geda-parts.scm -o dc_current.net dc_current.sch"

print ME, "creating netlist: ", command
pop = popen2.Popen4(command)
print pop.fromchild.read()
ret_gnetlist = pop.wait()
if ret_gnetlist != 0:
    print ME, "netlist creation failed with errorcode:", ret_gnetlist
else:
    print ME, "netlist creation was successful"

command = "gnucap -b simulate.gnucap"
print ME, "running simulation: ", command
pop = popen2.Popen4(command)
print pop.fromchild.read()
ret_simulation = pop.wait()
if ret_simulation != 0:
    print ME, "simulation failed with errorcode:", ret_simulation
else:
    print ME, "simulation run was successful"

print ME, "testing and plotting"
try:
    ret_plot = plot_dc_current()
except Exception, data:
    print ME, "plotting function died:"
    print data
    sys.exit(1)
    
if ret_plot == 0:
    print ME, "finished testing and plotting successfully"
    sys.exit(0)
else:
    print ME, "testing or plotting failed"
    sys.exit(2)

#!/usr/bin/env python
# modified slightly by R. Hlozek - 9/17

# This code will make plots for any output regardless of whether or not it is fit
import sys
import configparser
import numpy as np
import pylab as pl
from PIL import Image
from PyPDF2 import PdfFileMerger
import os
import glob
merger=PdfFileMerger()

settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()

try:

    inifile=sys.argv[1]
    root = sys.argv[2]
    print 'Reading inifile: %s '%inifile
except:
    print 'you need to specify an ini file'


settings.read(inifile)


curdir=settings.get('Filenames', 'curdir')
simdir=settings.get('Filenames', 'simdir')
savedir=settings.get('Filenames', 'savedir')

varindices=settings.get('PlotParams', 'varindiceshist')
varnames=settings.get('PlotParams', 'varshist')

varindices2d=settings.get('PlotParams', 'varindices2d')
varnames2d=settings.get('PlotParams', 'vars2d')

varnames = eval(varnames) # turn unicode into string
varindices = eval(varindices) # turn unicode into string

varnames2d = eval(varnames2d) # turn unicode into string
varindices2d = eval(varindices2d) # turn unicode into string


dumpfile=simdir+'/'+root+'/'+root+'.DUMP'

tmpdir = savedir+ '/tmpdir'

print 'Saving plots with root: %s to %s'%(root, savedir)

file = open(dumpfile, "rw+")
lines=file.readlines()[9:]
lendat = len(lines)
print 'there are %i lines in the data'%lendat
dat = np.zeros((lendat,28))

weirdcount=0

for count, line in enumerate(lines):
    spl=line.split()
    try:
        dat[count,:] = spl[1:]
    except:
        dat[count,:] = 0

#print np.shape(dat), 'before'
# Clipping to remove any blank lines in the simulation
ids=np.where(dat.any(axis=1))
dat = dat[ids]
#print np.shape(dat), 'after'

# removing weird z values
indsok = np.where(dat[:,4] < 2.)[0]
dat = dat[indsok,:]

print np.shape(dat), 'this is new shape'

for pcount, var in enumerate(varnames):
    pl.clf()
    print pcount, var, np.shape(dat[:,varindices[pcount]])
    pl.hist(dat[:,varindices[pcount]])
    pl.xlabel(var)
    pl.savefig(tmpdir+'/'+root+'hist_'+var+'.pdf')
    

for pcount, var in enumerate(varnames2d):
    pl.clf()
    pl.plot(dat[:,varindices2d[pcount][0]],dat[:,varindices2d[pcount][1]] , '.')
    pl.xlabel(varnames2d[pcount][0])
    pl.ylabel(varnames2d[pcount][1])
    pl.savefig(tmpdir+'/'+root+'hist_'+varnames2d[pcount][0]+varnames2d[pcount][1]+'.pdf')


for file in glob.glob(tmpdir+'/'+ root+ '*.pdf'):
    merger.append(file)

merger.write(savedir+'/'+root+'_summary.pdf')
merger.close()

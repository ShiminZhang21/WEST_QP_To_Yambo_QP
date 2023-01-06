#!/usr/bin/python
import numpy as np
import sys
import os
import argparse

dir_default='.'
parser = argparse.ArgumentParser()
parser.add_argument('-d',action='store',dest='dir',default=dir_default,
  help="directory of west output")
parser.add_argument('-k',type=int,action='store',dest='nk',default=1,
  help="number of k points")
parser.add_argument('-s',type=int,action='store',dest='ns',default=1,
  help="number of spins")
args = parser.parse_args()
ns= args.ns
print("dir=%s" % (args.dir))
print("nk=%d" % (args.nk))
print("ns=%d" % (ns))

cz = str(0.0)+"|"
fout = open("ypp.in","w")
fout.write("QPDBs # [R] Quasi-particle databases\n")
fout.write("QPDB_edit # [R] Generation/editing\n")
fout.write("%QPkrange # [QPDB] QP correctionQPDB energy correction( kp1| kp2| bnd1| bnd2| E-Eo[eV]| Img(E)[eV]| Re[Z] |)\n")

for ik in range(args.nk):
	# read west qp corrections
  ck = str(ik+1)+"|"
  cifil = str(ik*ns+1).zfill(5)
  filw = args.dir+"/o-eqp_K"+cifil+".tab"
  b = np.loadtxt(filw,usecols=(0),dtype=np.int16)
  eqp = np.loadtxt(filw,usecols=(4))
  if ns == 2:
    cifil = str(ik*ns+2).zfill(5)
    filw = args.dir+"/o-eqp_K"+cifil+".tab"
    b2 = np.loadtxt(filw,usecols=(0),dtype=np.int16)
    eqp2 = np.loadtxt(filw,usecols=(4))
  nb = b.shape[0]
  
  # write ypp.in
  for ib in range(nb):
    cb = str(b[ib])+"|"
    ceqp = str(eqp[ib])+"|"
    fout.write(" %s %s %s %s %10s %s %s\n" % 
      (ck,ck,cb,cb,ceqp,cz,cz))
    if ns == 2:
      cb2 = str(b2[ib])+"|"
      ceqp2 = str(eqp2[ib])+"|"
      fout.write(" %s %s %s %s %10s %s %s\n" %  
      (ck,ck,cb2,cb2,ceqp2,cz,cz))
fout.write("%")

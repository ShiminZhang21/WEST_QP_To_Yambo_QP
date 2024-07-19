#!/usr/bin/env python3
from netCDF4 import Dataset
import numpy as np


"""
This script print read and print the quasiparticle database ndb.QP
The output: 
	E0: DFT energy
	QP_E: energy of GW, have real and imaginary part
	E-E0: the usually printied quasiparticle correction, get from Re[QP_E]-E0
	QP_table: include |bn1 | bn2 | k | spin|, where spin=1 for up, spin=2 for dn
"""
ha2ev  = 27.2113834



f_qp="NewQP_60bands/ndb.QP_merged_1"

#database = Dataset(f_qp,"r")
#print(database)

#print(database.variables['QP_Eo'][:])



#f_qp="NewQP_60bands_p1/ndb.QP"
#f_qp="/data/groups/ping/kli103/defects_in_diamond/nv_center_in_diamond/clean/3x3x3/qe-6.6/pbe/new_gwbse_nk222_nbnd3600/5.0redo_triplet/data_60_bsebands/all_Bz/ndb.QP"
database = Dataset(f_qp,"r")
#print(database)
print(database.variables)

print("------------")
print(database.variables['QP_Eo'])
print(database.variables['QP_E'])
print(database.variables['QP_Z'])
print(database.variables['QP_kpts'])
print(database.variables["QP_table"])
print("------------")

#print("E0, QP_E, QP_Z, Re[QP_E-E0]")

#for i in np.arange(62):
#	print(database.variables['QP_Eo'][i], database.variables['QP_E'][i], database.variables['QP_E'][i][0]-database.variables['QP_Eo'][i])

print("E0, QP_E, E-E0, QP_table")
for i in np.arange(138):
	E0=database.variables['QP_Eo'][i]*ha2ev
	QP_E=database.variables['QP_E'][i]*ha2ev
	delE=QP_E[0]-E0
	QP_kpts=database.variables['QP_table'][:,i]
	print(E0, QP_E,delE, QP_kpts)

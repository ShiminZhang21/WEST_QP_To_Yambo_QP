# Example of YamboQPDB Class 
#
from qepy import *
from yambopy import *
import matplotlib.pyplot as plt

# Read Lattice information from SAVE
lat  = YamboSaveDB.from_db_file(folder='SAVE',filename='ns.db1')
# Read QP database
ydb  = YamboQPDB.from_db(filename='ndb.QP_merged_1',folder='NewQP_60bands')
E=ydb.e
E0=ydb.e0
print("{:<20}, {:<20}, {:<20}".format("e","e0","e-e0"))

for e, e0 in zip(E,E0):
	print("{:<20}, {:<20}, {:<20}".format(e, e0, e-e0))

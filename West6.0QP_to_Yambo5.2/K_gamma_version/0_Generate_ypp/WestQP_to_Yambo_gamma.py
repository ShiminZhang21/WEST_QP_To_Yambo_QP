#!/usr/bin/env python3

#This script read the west wfreq.json and write into the ndb.QP database generation input
#This is the gamma version, only have two k point, K000001 for spin up,  K000002 for spin dn. for K version the west don't have inverstion symmetry, so the k point index need to be compatible with yambo kp1 kp2. 

# to use the generated input:
    #yambo/ypp -F ypp.in
# this will generate a ndb.QP database in your SAVE folder.

#_______________INPUT________________________

import json

#read in data:  #spinpol and gamma
f_json="./wfreq.json" #west database
f_ypp = "./ypp.in" #Output file name
Bandlist = "All" #All for using all the bands, if not specify the list of bands to use
    


#_________________Functions___________________
def find_json(directory):
    """
    find the last json file in directory;
    useage: find_json("../west.wfreq.save")
    """
    import glob
    import os
    # Directory containing the files
    #directory = "L_0.16/west.wfreq.save"

    # Pattern to match the files of interest
    pattern = os.path.join(directory, "wfreq_*.json")

    # Find all files matching the pattern
    files = glob.glob(pattern)

    # If no files are found, default to "wfreq.json"
    if not files:
        f_name = os.path.join(directory, "wfreq.json")
    else:
        # Sort the files by the number in their name, assuming the format is "wfreq_NUMBER.json"
        files_sorted = sorted(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
        # The last file in the sorted list is the one with the largest number
        f_name = files_sorted[-1]
#    print("found json file:",f_name)
    return f_name

def Readqp_gamma(f_name, Bands="All", Verbose=False):
    """
    INPUT
    ________________________
    f_name: string
        name of the json file
    Bands: list 
        A list of bands. 
        if Bands="All", then return all bands 
    ________________________
    OUTPUT:
        Edft, Eqp
    Edft: numpy list 
        list of dft energy level.
        when nspin=2, Edft[0], Edft[1] for spin up and dn
    Eqp: numpy list
        list of qp correction
        when nspin=2, same as Edft
    Occ: numpy list
        list of occupation
    """
    import numpy as np
    # read data from JSON file
    with open(f_name, 'r') as file:
        data = json.load(file)
    # pretty print the data
    #print(json.dumps(data, indent=2))
    nspin = data["system"]["electron"]["nspin"]
    if nspin == 1:
        #find band index
        bandmap = data['input']['wfreq_control']["qp_bands"][0]
        # extracting energy levels from the data
        y = {}
        y['dft'] = data['output']['Q']['K000001']['eks']
        y['gw']  = data['output']['Q']['K000001']['eqpSec']
        y['qp'] = np.array(y['gw']) - np.array(y['dft'])
        y['occ'] = data['output']['Q']['K000001']['occupation']
        # output the list of data:
        if Bands=="All":
            Bands = bandmap
        Eqp = np.zeros(len(Bands))
        Edft = np.zeros(len(Bands))
        Occ = np.zeros(len(Bands))
        for i, band in enumerate(Bands):
            i_band = bandmap.index(band) #list index of band
            if Verbose==True:
                print("band : {} ; Index: {}".format(band, i_band))
            Eqp[i] = y['qp'][i_band]
            Edft[i] = y['dft'][i_band]
            Occ[i] = y['occ'][i_band]
        return Bands, Edft, Eqp, Occ
    elif nspin == 2:
        #find band index
        bandmap = data['input']['wfreq_control']["qp_bands"][0]
        # extracting energy levels from the data
        y = {}
        y['dft_up'] = data['output']['Q']['K000001']['eks']
        y['dft_dn'] = data['output']['Q']['K000002']['eks']
        y['gw_up']  = data['output']['Q']['K000001']['eqpSec']
        y['gw_dn']  = data['output']['Q']['K000002']['eqpSec']
        y['qp_up'] = np.array(y['gw_up']) - np.array(y['dft_up'])
        y['qp_dn'] = np.array(y['gw_dn']) - np.array(y['dft_dn'])
        y['occ_up'] = data['output']['Q']['K000001']['occupation']
        y['occ_dn'] = data['output']['Q']['K000002']['occupation']
        if Bands=="All":
            Bands = bandmap
        # output the list of data:
        Eqp = np.zeros((2,len(Bands))) # 2 for spin index
        Edft = np.zeros((2,len(Bands)))
        Occ = np.zeros((2,len(Bands)))
        for i, band in enumerate(Bands):
            i_band = bandmap.index(band) #list index of band
            if Verbose==True:
                print("band : {} ; Index: {}".format(band, i_band))
            Eqp[0,i] = y['qp_up'][i_band]
            Eqp[1,i] = y['qp_dn'][i_band]
            Edft[0,i] = y['dft_up'][i_band]
            Edft[1,i] = y['dft_dn'][i_band]
            Occ[0,i] = y['occ_up'][i_band]
            Occ[1,i] = y['occ_dn'][i_band]
        return Bands, Edft, Eqp, Occ

#_____________________Write___________________
Bands, Edft, Eqp, Occ = Readqp_gamma(f_json,Bands=Bandlist)
       
#_________Output contents___________
QP_input_contents = \
"""#                                                                     
#                                                                     
# Y88b    /   e           e    e      888~~\    ,88~-_                
#  Y88b  /   d8b         d8b  d8b     888   |  d888   \               
#   Y88b/   /Y88b       d888bdY88b    888 _/  88888    |              
#    Y8Y   /  Y88b     / Y88Y Y888b   888  \  88888    |              
#     Y   /____Y88b   /   YY   Y888b  888   |  Y888   /               
#    /   /      Y88b /          Y888b 888__/    `88_-~                
#                                                                     
#                                                                     
# Version 5.1.0 Revision 22561 Hash (prev commit) 785b4fd6f           
#                     Branch is 5.2                                   
#                 MPI+HDF5_MPI_IO Build                               
#               http://www.yambo-code.org                             
#

PDBs                            # [R] Quasiparticle Databases 
QPDB_edit                        # [R] Generation/editing 
%QP_user_corrections             # [QPDB] Correction( spin | kp1| kp2| bnd1| bnd2| #E-Eo[eV]| Img(E)[eV]| Re[Z] |)
"""

for b, eqpup, eqpdn in zip(Bands,Eqp[0],Eqp[1]):
    QP_input_contents+= "1|1|1|{}|{}| {}| 0.000000| 0.000000|\n".format(int(b),int(b),eqpup)
    QP_input_contents+= "2|1|1|{}|{}| {}| 0.000000| 0.000000|\n".format(int(b),int(b),eqpdn)
QP_input_contents+="%"
with open(f_ypp, 'w') as file:
    file.write(QP_input_contents)

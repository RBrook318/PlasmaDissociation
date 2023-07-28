#########################################################################################
#
#   Main python script for the submission of dissociation after electron impact
#   Written by R Brook                                                 28.07.23
#  
# 
#   Designed to be called from the .sh run file in order to manage the whole process.
#     
#   Steps taken:
#   1. Recieves arguements from the .sh run file
#   2. Read in geometries from the geom input file
#   3. Submit the qchem job (and the second if the first one fails)
#   4. Stores the output of the qchem file 
#   5. Moves the information from the qchem output to a file ready to be propagated  
#   6. Begin propagation by taking the preliminary timestep 
#   7. Submit the qchem job (and the second one if it fails)
#   8. Run the correlation script to calculate new momenta
#   9. Repeat 6-8 until propagation is done 
#######################################ß##################################################
#!/usr/bin/env python
import sys
import socket
import os
import subprocess
import getpass
import random
import shutil
import glob
import csv
import Conversion

# !!!! Defining functions !!!!

def process_geometry_file(file_path):
    with open(file_path, "r") as geometry_file:
        lines = geometry_file.readlines()
        last_19_lines = lines[-19:]

    with open("t.0", "w") as t0_file:
        t0_file.writelines(last_19_lines)
        t0_file.writelines(" ")
        t0_file.writelines("1.0")
        t0_file.writelines("0.0")
    
    with open("t.ini", "w") as tini_file:
            tini_file.writelines(last_19_lines)        
            tini_file.writelines(" ")
            tini_file.writelines("1.0")
            tini_file.writelines("0.0")

# Helper function to write content to a file
def write_content_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

# Helper function to check if a file contains a specific string
def file_contains_string(file_path, search_string):
    with open(file_path, "r") as file:
        return search_string in file.read()

def run_qchem(ncpu):

    def submit_qchem_job():
        subprocess.run(["qchem", "-save", "-nt", str(ncpu), "f.inp", "f.out", "wf"], wait= True)


    # Prepare f.inp file
    write_content_to_file("f.inp", f"$molecule\n{open('geom.in').read()}$end\n{open('sf_diis').read()}CIS_N_ROOTS 1\nCIS_STATE_DERIV 1\n$end\n")

    # Submit the initial QChem job
    submit_qchem_job()

    if not file_contains_string("f.out", "Calculating analytic gradient of the CIS energy"):
        # Retry with a different setup if the job fails
        write_content_to_file("f.inp", f"$molecule\n{open('geom.in').read()}$end\n{open('sf_gmd').read()}CIS_N_ROOTS 1\nCIS_STATE_DERIV 1\n$end\n")
        submit_qchem_job()

        if not file_contains_string("f.out", "Calculating analytic gradient of the CIS energy"):
            # Job failed both times, print error and exit
            write_content_to_file("ERROR", "Error occurred during QChem job.\n" + os.getcwd())
            exit(1)

    # Append f.out content to f.all
    with open("f.out", "r") as f_out, open("f.all", "a") as f_all:
        f_all.write(f_out.read())



# !!!! ACTUAL CODE PORTION !!!!

#  And if we start coding here. 
#  Step 1. Recieves arguements from the .sh run file
#  Arguements recieved ncpu: number of cpus available, reps: number of the repition in order to access the right files. 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <number_of_cpus> <reps_number")
        sys.exit(1)

    try:
        ncpu = int(sys.argv[1])
        reps = int(sys.arg[2])
        # run_qchem(ncpu)
    except ValueError:
        print("Invalid number of CPUs. Please provide a valid integer.")
        sys.exit(1)

#  Step 2. Read in geometries from the geom input file
#  Needs to take in a geometry.reps file and makes the output t.ini and t.0 file.

process_geometry_file("geometry."+str(reps)) 

#  Step 3. Submit the qchem job (and the second if the first one fails)
# subprocess.run(["../Code/get_geom.x", "t.0"],Wait =True)
Conversion.make_geometry_input('t.0')
run_qchem(ncpu)
# subprocess.run(["../Code/q_to_prop.x"], Wait = True)
Conversion.q_to_prop('t.0')

#   Step 9. Repeat steps 6-10 until complete

for i in range(1, 2501):
    # os.rename("t.1", "t.0") NEEDS TO BE AT THE END OF THE LOOP?

    #   Step 6. Begin propagation by taking the preliminary timestep 

    subprocess.run(["../Code/prop_prelim.x", "t"], Wait= True)
   
    # subprocess.run(["../Code/get_geom.x", "t.p"], Wait = True)
    Conversion.make_geometry_input('t.p')
    
    #  Step 7. Submit the qchem job (and the second one if it fails)
    run_qchem(ncpu)

    # Step 8. Translate from angstroms to bohr
    # subprocess.run(["../Code/q_to_prop.x"], Wait = True)
    Conversion.q_to_prop('t.p')
    subprocess.run(["../Code/prop_corr.x", "t"], Wait = True)

    # Append t.1 content to t1.all
    with open("t.1", "r") as t1_file, open("t1.all", "a") as t1_all:
        t1_all.write(t1_file.read())
        t1_all.write("---------------------------------------------------\n")

    # Append t.te content to te.all
    with open("t.te", "r") as t_te_file, open("te.all", "a") as te_all:
        te_all.write(t_te_file.read())

    # Check for removed molecules
    if open("t.1").readline() != open("t.p").readline():
        # os.rmdir("wf")
        with open("t.diss1", "a") as t_diss1:
            t_diss1.write(str(i) + "\n")



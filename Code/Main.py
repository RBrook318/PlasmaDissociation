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

def process_geometry_file(file_path,spin_flip):
    with open(file_path, "r") as geometry_file:
        lines = geometry_file.readlines()
        

    with open("t.0", "w") as t0_file:
        t0_file.writelines(str(natoms)+" "+str(nstates)+"\n")
        t0_file.writelines(str(nbranch)+"\n")
        t0_file.writelines("0 "+str(timestep)+"\n")
        if spin_flip == 0: 
            t0_file.writelines("0 3 \n")
        elif spin_flip == 1:
            t0_file.writelines("0 5 \n")
        t0_file.writelines(lines)
        t0_file.writelines(" \n")
        t0_file.writelines("1.0 \n")
        t0_file.writelines("0.0 \n")
        t0_file.writelines(" \n")

    with open("t.ini", "w") as tini_file:
            tini_file.writelines(str(natoms)+" "+str(nstates)+"\n")
            tini_file.writelines(str(nbranch)+"\n")
            tini_file.writelines("0 "+str(timestep)+"\n")
            tini_file.writelines("0 5 \n")
            tini_file.writelines(lines)        
            tini_file.writelines(" \n")
            tini_file.writelines("1.0 \n")
            tini_file.writelines("0.0 \n")
            tini_file.writelines(" \n")


# Helper function to write content to a file
def write_content_to_file(file_path, content):
    with open(file_path, "w") as file:
        file.write(content)

# Helper function to check if a file contains a specific string
def file_contains_string(file_path, search_string):
    with open(file_path, "r") as file:
        return search_string in file.read()

def create_qchem_input(output_file, geom_file_path, spin_flip,theory, scf_algorithm="DIIS",Guess=True):
    # Read the geometry data from geom.in
    with open(geom_file_path, "r") as geom_file:
        geom_lines = geom_file.readlines()

    # Q-Chem input file content
    qchem_input = (
        "$molecule\n"
        + "".join(geom_lines)
        + "$end\n"
        "$rem\n"
        "    JOBTYPE             Force\n"
        "    EXCHANGE            BHHLYP\n"
        "    BASIS               6-31+G*\n"
        "    UNRESTRICTED        True\n"
        "    MAX_SCF_CYCLES      500\n"
        "    SYM_IGNORE          True\n"
        f"    SCF_Algorithm       {scf_algorithm}\n"  # Use the specified SCF algorithm
        "\n"
    )
    # Use spin flip if method chosen 
    if spin_flip==1:
        qchem_input += "    SPIN_FLIP           True\n"

    qchem_input += (
        "    SET_Iter            500\n"
        "\n"
        "    MAX_CIS_CYCLES      500\n"
        )
    # Add SCF_GUESS line if Guess is True
    if Guess:
        qchem_input += "    SCF_GUESS           Read\n"

    if theory ==1:
        qchem_input += (
            "\n"
            "CIS_N_ROOTS 1\n"
            "CIS_STATE_DERIV 1\n"
        )
    qchem_input += "$end\n"
    # Write the Q-Chem input content to the output file
    with open(output_file, "w") as qchem_file:
        qchem_file.write(qchem_input)




def run_qchem(ncpu,spin_flip,theory,Guess=True):

    def submit_qchem_job():
        subprocess.run(["qchem", "-save", "-nt", str(ncpu), "f.inp", "f.out", "wf"])


    # Prepare f.inp file
    create_qchem_input("f.inp", "geom.in",spin_flip,theory, scf_algorithm="DIIS",Guess=Guess)

    # Submit the initial QChem job
    submit_qchem_job()

    if not file_contains_string("f.out", " Total job time:"):
        # Retry with a different setup if the job fails
        create_qchem_input("f.inp", "geom.in", spin_flip,theory,scf_algorithm="DIIS_GDM",Guess =False)
        submit_qchem_job()

        if not file_contains_string("f.out", " Total job time:"):
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
    if len(sys.argv) != 12:
        print("Usage: python script_name.py <reps> <noofcpus> <natoms> <nstates>")
        print(len(sys.argv))
        sys.exit(1)

    try:
        reps= int(sys.argv[1])
        ncpu = int(sys.argv[2])
        natoms = int(sys.argv[3])
        nstates = int(sys.argv[4])
        nbranch = int(sys.argv[5])
        timestep = int(sys.argv[6])
        endstep = int(sys.argv[7])
        restart = str(sys.argv[8])
        geom_start = int(sys.argv[9])
        spin_flip = int(sys.argv[10])
        theory = int(sys.argv[11])
    except ValueError:
        print("Invalid number of CPUs. Please provide a valid integer.")
        sys.exit(1)

#  Step 2. Read in geometries from the geom input file
#  Needs to take in a geometry.reps file and makes the output t.ini and t.0 file.
if(restart == 'NO'):
    process_geometry_file("Geometry."+str(reps+geom_start-1),spin_flip) 

    #  Step 3. Submit the qchem job (and the second if the first one fails)

    Conversion.make_geometry_input('t.0')
    run_qchem(ncpu,spin_flip,theory,Guess=False)
    # Conversion.q_to_prop('t.0')
    if theory==1:
        command = ["./q_to_prop.x"]
        with open("t.0", "a") as output_file:
            try:
                # Execute the command as a subprocess
                subprocess.run(command, stdout=output_file, check=True)
                print("Command executed successfully.")
            except subprocess.CalledProcessError as e:
                print("Command execution failed with error:", e)
        with open("t.0", "r") as t0_file, open("t1.all", "a") as t1_all:
            t1_all.write(t0_file.read())
            t1_all.write("---------------------------------------------------\n")
    elif theory==0:
        command = ["./q_to_propSCF.x"]
        with open("t.0", "a") as output_file:
            try:
                # Execute the command as a subprocess
                subprocess.run(command, stdout=output_file, check=True)
                print("Command executed successfully.")
            except subprocess.CalledProcessError as e:
                print("Command execution failed with error:", e)
        with open("t.0", "r") as t0_file, open("t1.all", "a") as t1_all:
            t1_all.write(t0_file.read())
            t1_all.write("---------------------------------------------------\n")
    startstep = 1


elif (restart == 'YES'):
    file_path = 't.0'

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 3:
                third_row = lines[2].strip().split()
                startstep = float(third_row[0]) / timestep
            else:
                # Handle the case where the file doesn't have at least 3 lines
                startstep = 1.0
    else:
        # Handle the case where the file doesn't exist
        process_geometry_file("Geometry."+str(reps+geom_start-1),spin_flip) 

        #  Step 3. Submit the qchem job (and the second if the first one fails)

        Conversion.make_geometry_input('t.0')
        run_qchem(ncpu,spin_flip,theory,Guess=False)
        # Conversion.q_to_prop('t.0')

        startstep = 1


if theory==0:
    correct_mult = 3
    old_mult = 3

#   Step 9. Repeat steps 6-10 until complete

for i in range(int(startstep), endstep+1):


    #   Step 6. Begin propagation by taking the preliminary timestep 

    subprocess.run(["./prop_prelim.x", "t"])
    Conversion.make_geometry_input('t.p')
    
    #  Step 7. Submit the qchem job (and the second one if it fails)
    run_qchem(ncpu,spin_flip,theory,Guess=True)

    # Step 8. Translate from angstroms to bohr

    # Conversion.q_to_prop('t.p')
    if theory==1:
        command = ["./q_to_prop.x"]
        with open("t.p", "a") as output_file:
            try:
                # Execute the command as a subprocess
                subprocess.run(command, stdout=output_file, check=True)
                print("Command executed successfully.")
            except subprocess.CalledProcessError as e:
                print("Command execution failed with error:", e)
        # with open("t.0", "r") as t0_file, open("t1.all", "a") as t1_all:
        #     t1_all.write(t0_file.read())
        #     t1_all.write("---------------------------------------------------\n")
    elif theory==0:
        command = ["./q_to_propSCF.x"]
        with open("t.p", "a") as output_file:
            try:
                # Execute the command as a subprocess
                subprocess.run(command, stdout=output_file, check=True)
                print("Command executed successfully.")
            except subprocess.CalledProcessError as e:
                print("Command execution failed with error:", e)
        # with open("t.0", "r") as t0_file, open("t1.all", "a") as t1_all:
        #     t1_all.write(t0_file.read())
        #     t1_all.write("---------------------------------------------------\n")
    
    subprocess.run(["./prop_corr.x", "t"])
    
    if theory==0:
        with open("t.1","r") as file:
            lines = file.readlines()
            fourth_line = lines[3]  
            print(fourth_line)
            numbers = fourth_line.split()
            mult = int(numbers[1])
            print(mult)
            print(old_mult)
            if mult != old_mult:
                mult = correct_mult -1 
                correct_mult = correct_mult -1 
                if mult ==0:
                    mult == 1
                lines[3] = f"{numbers[0]} {mult}\n"
                print(lines[3])

                with open("t.1", "w") as file:
                    file.writelines(lines)
            print(mult)
            old_mult = mult
            
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

    # Transfer the contents of t.1 to t.0 to continue the propagation
    with open("t.1", "r") as t1_file, open("t.0", "w") as t0_file:
        t0_file.write(t1_file.read())



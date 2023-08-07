#########################################################################################
#
#   Python Run script for the submission of dissociation after electron impact
#   Written by R Brook                                                 26.07.23
#   Inspired heavily by Oliver Bramley's run script for MCE/CCS
# 
#   Written to make submission of jobs to the HPC easier and quicker
#     
#
#########################################################################################
import sys
import socket
import os
import subprocess
import getpass
import random
import shutil
import glob
import csv
import inputs

#########################################################################################
#                              VARIABLES TO SET FOR SIMULATION                          #
#########################################################################################

# Number of repeats 
repeats=2
# #Number of parallel cores per folder/node (max 8)
cores=8
# Name of running folder 
# Default : <method>-<system>-<random number> ie CCS-HP-31254
# Otherwise:  <method>-<system>-<runfolder string>
Runfolder='Propylene-test'
# Restart Flag 
restart = 'NO'

#########################################################################################
#                                   END OF INPUTS                                       #
#########################################################################################
#                * NO NEED TO SCROLL FURTHER IF USING AS BLACKBOX *                     #
#########################################################################################


if __name__=="__main__":
    #Check basic arguements
    if(isinstance(repeats,int)==False):
        sys.exit("Number of repeats must be an integer")
    elif(isinstance(cores,int)==False):
        sys.exit("Number of parallel cores must be an integer")
    elif(repeats<1):
        sys.exit("Not enough runs selected. Must be 1 or greater")
    elif(cores>8):
        sys.exit("Too many cores selected. Maximum of 8 available")
    elif(cores<1):
        sys.exit("Not enough cores selected. Must be 1 or greater")

    if(restart=="NO"):
        if(inputs.Geom not in{0,1}):
            sys.exit("Geometry flag must be zero or 1")
        else:
            print("Arguments checked")
            Hostname=socket.gethostname()
            if(Hostname==("login1.arc4.leeds.ac.uk")or(Hostname==("login2.arc4.leeds.ac.uk"))):
                HPCFLG=1
            elif(Hostname==("login1.arc3.leeds.ac.uk")or(Hostname==("login2.arc3.leeds.ac.uk"))):
                HPCFLG=1 
            else:
                HPCFLG=1

        #Makes execution folder and run folder
        if(HPCFLG==1): #change this to 0 before uploading.
            if not os.path.exists("../EXEC"):
                os.mkdir("../EXEC")
            EXDIR="../EXEC"
        else:
            # subprocess.run(['module','load','mkl'])
            os.environ['LOGNAME']
            EXDIR="/nobackup/"+getpass.getuser()

        
        if os.path.exists(EXDIR+"/"+Runfolder):
            value=input("File already exists do you want to delete it? y/n\n")
            if(value=='y'):
                shutil.rmtree(EXDIR+"/"+Runfolder)
            else:
                sys.exit("Runfolder already exists. Change the Runfolder name or delte/move it")
        
        os.mkdir(EXDIR+"/"+Runfolder)
        
        EXDIR1=EXDIR+"/"+Runfolder  

        mcerunf=os.getcwd()
        # result=open(EXDIR1+"/result.sh","w")
        # result.write("python "+mcerunf+"/collate.py $PWD "+(str(repeats))+" "+str(nodes)+" '"+Runfolder+"' "+(str(HPCFLG))+" '"+prop+"'")
        # result.close()
        # subprocess.run(['chmod', 'u+x', EXDIR1+'/result.sh'])
            
        #Copies input files
        shutil.copy2("run.py",EXDIR1)

        for i in range(repeats):
            path=os.path.join(EXDIR1,"run-"+str(i+1))
            os.mkdir(EXDIR1+"/run-"+str(i+1))
            shutil.copy2("../"+inputs.Molecule+"/Geom/Geometry."+str(i+1),EXDIR1+"/run-"+str(i+1))
            shutil.copy2("../Code/Main.py",EXDIR1+"/run-"+str(i+1))
            shutil.copy2("../Code/Conversion.py",EXDIR1+"/run-"+str(i+1))
            shutil.copy2("../Code/prop_prelim.x",EXDIR1+"/run-"+str(i+1))
            shutil.copy2("../Code/prop_corr.x",EXDIR1+"/run-"+str(i+1))
            subprocess.run(['chmod', 'u+x', EXDIR1+"/run-"+str(i+1)+'/prop_prelim.x'])
            subprocess.run(['chmod', 'u+x', EXDIR1+"/run-"+str(i+1)+'/prop_corr.x'])

                

        os.chdir(EXDIR1)
        EXDIR1=os.getcwd()




       


        # for i in range (nodes):
        #     shutil.copy2("MCE.exe","run-"+str(i+1))
        #     shutil.copy2("rundata.csv","run-"+str(i+1))
        #     if(Geom==1):
        #         for k in range(repeats/nodes):
        #             shutil.copy2("freq.dat","/run-"+str(i+1)+"/freq"+str(k+1)+".dat")
        
    #If on a SGE machine make job submission file
    if(HPCFLG==1):
        number=random.randint(99999,1000000)
        file1="Plasma"+str(number)+".sh"
        f=open(file1,"w")
        f.write("#$ -cwd -V \n")
        f.write("#$ -l h_vmem=1G,h_rt=48:00:00 \n")
        f.write("#$ -pe smp "+str(cores)+" \n") #Use shared memory parallel environemnt 
        f.write("#$ -t 1-"+str(repeats)+" \n")
        f.write("module load mkl \n")
        f.write("module load test qchem \n")
        f.write("module load anaconda \n")
        f.write("source actviate base \n")
        f.write("cd "+EXDIR1+"/run-$SGE_TASK_ID/ \n")
        f.write(" python Main.py "+str(cores)+" "+str(repeats)+" "+str(inputs.Atoms)+" "+str(inputs.States)+" "+str(inputs.Branch)+" "+str(inputs.Timestep)+" "+str(inputs.Tot_timesteps))
        f.close()
        # if(cores!=1):
        #     os.environ["OMP_NUM_THREADS"]=str(cores)
        # subprocess.call(['qsub',file1])

    else:
        print('Probably dont run this here')
        

    
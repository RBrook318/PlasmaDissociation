# PlasmaDissociation


Interface developed in order to perform Ab Initio Molecular Dynamics. The electronic structure information is calculated via QChem using the method TDDF spin flip. 

The code is broken into 3 main parts, the setup & run, the propagation, and the results processing. 

Chapter 1: Setup and Run files 

The code is designed to work on a high powered computing environment with a Sun Grid Engine (SGE) scheduling system. The run folder contains the files capable of changing most factors of the propagation. 

Inside inputs.py, there are the options for: 
  - Geometry Flag: Kept as 1, signals that the code should look for the geometry files in a given folder specified later. If a way to generate random geometries was implemented,       then this flag could be changed.
    
  - Molecule: If 'Geometry Flag' is 1, this is then taken as the name of the file containing the pre-generated geometries.

  - Number of atoms: Number of atoms in the starting molecule.

  - Number of states: Number of states considered by QChem, normally set to be 2 for small molecules, and even then only the first state is populated. This coincides with the fact     that the first triplet state is involved in dissociation after electron impact.

  - Branching number: Determines whether or not branching (cloning) is allowed within propagation.

  - Timestep: How many atomic time units should make up a single timestep

  - Tot_timestep: How many timesteps in total should make a total propagation.

  - Geom_start: The first geometry file taken from the file, e.g. in order to run geom.101-geom.200

Inside Run.py, there are options for: 
  - Repeats: The number of different trajectories that should be propagated in this run

  - Cores: The number of CPUS to be requested

  - Runfolder: The name of the file to be created where the outputs are made

  - Restart Flag: Whether this run is being started for the first time or whether to restart a failed or timed-out run.

If restart flag is 0, then this the first run for a given run-folder, and the run-folder is created within nobackup and the approiate geometry file is copied into each repeat folder. The bash run file is then created and submitted. The geometry file should be of the form: 

               9
    C    -0.0151530299    -1.7245140076     0.0902602226
    H     1.6599788666    -3.0194928646     1.4945089817
    H     1.1987202168    -2.1157917976    -2.2039279938
    H    -2.1853125095    -2.7259137630    -0.0852743164
    C    -0.0296703614     1.0355875492     1.0148756504
    H    -0.0190874841     0.9638609290     2.7984864712
    C     0.0215299744     3.0698873997    -0.5709819794
    H     0.2935736775     3.2048637867    -2.3483188152
    H    -0.0668819323     5.6954283714     0.5106948614
     momenta
      -1.340299      -1.839603       11.11354    
       3.765748       18.21791      -9.453912    
     -0.3961563       14.19139      -5.992531    
      -3.157275      -9.615326       4.598836    
      0.7770783      0.4139509      -14.58165    
      -9.946272      -15.44369       6.820938    
      -3.426562      -4.431175       3.883945    
       8.392735       1.632011       3.478122    
       15.20431       11.46569     -0.5870720   

This file is geom.1 for the propylene molecule. 

Chapter 2: Propagation 

The main.py file has a step by step process 
Step 1. Recieves arguements from the run.sh file and sets variables 

Step 2. Read in geometries from the geom input file

Step 3. Submit the initial qchem job (and the second if the first one fails) to generate forces before propagation 

Step 4. Begin propagation by taking the preliminary timestep (uses homemade nuclear propagation code prop_prelim.x)
 
Step 5. Submit the qchem job (and the second one if it fails) to find the forces of the new geometry 

Step 6. Use the forces from both the begining of the timestep and the prelimary timestep to recalculate momentum 

Step 7. Repeat step 4-6 until the end timestep is reached. 

The file conversion.py is used to move and transform data between the output from the molecular dynamic code and the output of QChem. 

Chapter 3: Results processing 

At the end of propagation, for each repeat there will be a run-x folder, which contains all information calculated throughout the propagation. Running Result.py transfers analysis.x into each run-x folder, and creates t.xyz and output.xyz, which are condensed forms of the geometry of each timestep. The program then makes dissociation.out in each run-x folder, which states if and when each bond exceeeds a given distance, where each bond is specified in a provided bond array. 

The program collate.py then goes through each dissociation.out within each run-x folder and creates a collateddissociation.out that contains all instances of bonds breaking across all repeats. Collate.py is also used to separate the collated file into files based on both bond type and each individual bond, which can then be plotted to display results.

Animation.py can be used with an input of output.xyz in order to generate a gif of the trajectory. 






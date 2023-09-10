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

If restart flag is 0, then this the first run for a given run-folder, and the run-folder is created within nobackup and the approiate geometry file is copied into each repeat folder. The bash run file is then created and submitted.

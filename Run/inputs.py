# Input file to serve along side run.py containing 
# information not concerning the input to hpc 
# R.Brook 7/08/2023

# Geometry flag
Geom = 1
# Name of molecule if Geom flag (where the Geometry files are stored: Molecule>Geom>Geometry.num)
Molecule = 'i-C4H3F7O'
# Number of atoms
Atoms = 15
# Number of states
States = 2
# Branching number
Branch = 0
# Timestep size 
Timestep = 10
# No of timesteps
Tot_timesteps = 1
# Starting geometry index
Geom_start = 1
# Use spin flip TDDFT
Spin_flip = 0
# Level of theory (SCF = 0 or CIS = 1) ! If you want spin-flip, use CIS
Theory = 0
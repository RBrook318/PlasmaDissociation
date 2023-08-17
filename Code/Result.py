import os
import shutil
import subprocess
import sys 

runfolder = str(sys.argv[1])
reps = int(sys.argv[2])


def detect_dissociation(input_file, output_file):
    # Define the array denoting bonded molecules
    bonded_array = [
        [1, 2],
        [1, 3],
        [1, 4],
        [1, 5],
        [5, 6],
        [5, 7],
        [7, 8],
        [7, 9]
        # Add more bonded pairs as needed
    ]

    # Read the input data from a file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Initialize variables to store the current timestep, atom data, and dissociation flag
    timestep = None
    atoms = {}
    previous_broken_bonds = []

    # Open the output file for writing
    with open(output_file, 'w') as output:
        # Iterate through the lines and process the data
        for line in lines:
            parts = line.split()
            if len(parts) == 1 and parts[0].replace('.', '', 1).isdigit():
                if atoms:
                    broken_bonds = []
                    for bonded_pair in bonded_array:
                        i, j = bonded_pair
                        atom1 = atoms[i]
                        atom2 = atoms[j]
                        distance = ((atom1[1] - atom2[1])**2 + (atom1[2] - atom2[2])**2 + (atom1[3] - atom2[3])**2)**0.5
                        if distance > 3.0:  # Adjust this threshold as needed
                            broken_bonds.append((i, j))
                    if broken_bonds and broken_bonds != previous_broken_bonds:
                        output.write(f"Dissociation detected at timestep {timestep}, Broken bonds: {broken_bonds}\n")
                        previous_broken_bonds = broken_bonds
                    atoms = {}
                timestep = float(parts[0])
            elif len(parts) == 5 and parts[0].isdigit():
                atom_num = int(parts[0])
                atom_info = [parts[1]] + [float(x) for x in parts[2:]]
                atoms[atom_num] = atom_info

# Call the function with the input file
# detect_dissociation('output.xyz')

def process_molecular_coordinates(input_file_path, output_file_path):
    current_atoms = []
    atom_number = 1  # Initialize atom number

    with open(input_file_path, 'r') as input_file:
        lines = input_file.readlines()

    with open(output_file_path, 'w') as output_file:
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue  # Skip empty lines and comments

            if line.startswith('C') or line.startswith('H'):
                parts = line.split()
                if len(parts) == 4:  # Assuming "Symbol x y z" format
                    symbol, x, y, z = parts
                    current_atoms.append((atom_number, symbol, float(x), float(y), float(z)))
                    atom_number += 1
            
            elif line.replace('.', '', 1).isdigit():
                # This line indicates a new time step, write time step to output file
                if current_atoms:
                    output_file.write(f"{time_step}\n")
                    for atom in current_atoms:
                        atom_number, symbol, x, y, z = atom
                        output_file.write(f"{atom_number} {symbol} {x} {y} {z}\n")
                    output_file.write("\n")  # Add a space between sets

                # Update time step and reset for a new set of atoms
                time_step = line
                current_atoms = []
                atom_number = 1  # Reset atom number for the next set

        # Write the last set of atoms (if any)
        if current_atoms:
            output_file.write(f"{time_step}\n")
            for atom in current_atoms:
                atom_number, symbol, x, y, z = atom
                output_file.write(f"{atom_number} {symbol} {x} {y} {z}\n")

# Call the function with input and output file paths
# process_molecular_coordinates('t.xyz', 'output.xyz')

# for i in (1,100):

EXDIR= os.getcwd()


for i in range(reps):
        EXDIR1 = '../t'+str(i+1)
        print(EXDIR1)
        shutil.copy2("analysis/analysis.x",EXDIR1)
        subprocess.run(['chmod', 'u+x', "../t"+str(i+1)+'/analysis.x'])
        os.chdir(EXDIR1)
        subprocess.run(["./analysis.x", "t"])
        process_molecular_coordinates('t.xyz', 'output.xyz')
        detect_dissociation('output.xyz','dissociation.out')
        os.chdir(EXDIR)




        
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
with open('output.xyz', 'r') as f:
    lines = f.readlines()

# Initialize variables to store the current timestep, atom data, and dissociation flag
timestep = None
atoms = {}
previous_broken_bonds = []

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
                print(f"Dissociation detected at timestep {timestep}, Broken bonds: {broken_bonds}")
                previous_broken_bonds = broken_bonds
            atoms = {}
        timestep = float(parts[0])
    elif len(parts) == 5 and parts[0].isdigit():
        atom_num = int(parts[0])
        atom_info = [parts[1]] + [float(x) for x in parts[2:]]
        atoms[atom_num] = atom_info

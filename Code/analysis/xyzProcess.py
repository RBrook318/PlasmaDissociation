# Read the molecular coordinates data
input_file_path = 't.xyz'  # Replace with your input file path
output_file_path = 'output.xyz'  # Replace with your desired output file path

with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

current_atoms = []
atom_number = 1  # Initialize atom number

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

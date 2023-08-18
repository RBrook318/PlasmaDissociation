import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Read the molecular coordinates data
with open('t.xyz', 'r') as file:
    lines = file.readlines()

time_steps = []
current_time_step = None
current_atoms = []

# Process the lines and parse the data
for line in lines:
    line = line.strip()
    if line.isdigit() and current_time_step is None:
        current_time_step = float(line)
        current_atoms = []
    elif re.match(r'\d+\.\d+', line):
        if current_time_step is not None:
            time_steps.append((current_time_step, current_atoms))
        current_time_step = float(line)
        current_atoms = []
    else:
        match = re.match(r'([A-Za-z]+)\s+([-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+)', line)
        if match:
            atom_symbol, coords = match.group(1), match.group(2)
            x, y, z = map(float, coords.split())
            current_atoms.append((atom_symbol, x, y, z))

bond_distance_threshold = 3  # Adjust this threshold based on your molecule
bonded_atoms = []

for step in time_steps:
    step_bonds = []
    carbon_atoms = [(i, atom) for i, atom in enumerate(step[1]) if atom[0] == 'C']
    hydrogen_atoms = [(i, atom) for i, atom in enumerate(step[1]) if atom[0] == 'H']

    # Bond hydrogen atoms to the closest carbon atom
    for hydrogen_idx, hydrogen_atom in hydrogen_atoms:
        h_coords = hydrogen_atom[1:]

        # Find the closest carbon atom to the hydrogen atom
        closest_carbon_idx = None
        min_distance = float('inf')
        for carbon_idx, carbon_atom in carbon_atoms:
            c_coords = carbon_atom[1:]
            distance = ((h_coords[0] - c_coords[0])**2 +
                        (h_coords[1] - c_coords[1])**2 +
                        (h_coords[2] - c_coords[2])**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_carbon_idx = carbon_idx
        
        # Check if the closest carbon is within the bond distance threshold
        if min_distance < bond_distance_threshold:
            step_bonds.append((closest_carbon_idx, hydrogen_idx))

    # Bond carbon atoms to each other if within the bond distance threshold
        # Bond carbon atoms to each other if within the bond distance threshold
        for i, carbon1 in carbon_atoms:
            for j, carbon2 in carbon_atoms:
                if i < j and not ((i == 0 and j == 6)):

                    c1_coords = carbon1[1:]
                    c2_coords = carbon2[1:]
                    distance = ((c1_coords[0] - c2_coords[0])**2 +
                                (c1_coords[1] - c2_coords[1])**2 +
                                (c1_coords[2] - c2_coords[2])**2)**0.5
                    if distance < bond_distance_threshold:
                        step_bonds.append((i, j))
                        # print('after threshold', i,j)
 
    
    bonded_atoms.append(step_bonds)



if current_time_step is not None:
    time_steps.append((current_time_step, current_atoms))

# Create the animation
# Create the animation
def update_plot(frame):
    ax.clear()
    ax.set_title(f"Time: {time_steps[frame][0]}")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    atom_colors = {'C': 'grey', 'H': 'red'}  # You can define colors for different atom types
    
    # Draw atoms as spheres
    for atom in time_steps[frame][1]:
        atom_symbol, x, y, z = atom
        color = atom_colors.get(atom_symbol, 'blue')  # Default color for unknown atoms
        ax.scatter(x, y, z, color=color, s=200)  # Adjust 's' for the size of the spheres

    # Draw bonds if available
    if frame < len(bonded_atoms):
        for bond in bonded_atoms[frame]:
            atom1 = time_steps[frame][1][bond[0]]
            atom2 = time_steps[frame][1][bond[1]]
            ax.plot([atom1[1], atom2[1]], [atom1[2], atom2[2]], [atom1[3], atom2[3]], color='black')
    
    # Set a fixed range of X units for each axis
    axis_range = 5.0
    
    ax.set_xlim(-axis_range, axis_range)
    ax.set_ylim(-axis_range, axis_range)
    ax.set_zlim(-axis_range, axis_range)
    ax.view_init(elev=30, azim=1)  # Adjust the angles as needed



fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Specify the range of frames (0 to 599 for the first 600 time steps)
start_frame = 0
end_frame = 3000

animation = FuncAnimation(fig, update_plot, frames=range(start_frame, end_frame), interval=100)

# Save the animation as an MP4 video
animation.save('Trajectory50.gif', writer='pillow', fps=2000)  # Adjust fps as needed

# plt.show()


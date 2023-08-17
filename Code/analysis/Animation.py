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
    for i, atom1 in enumerate(step[1]):
        for j, atom2 in enumerate(step[1]):
            if i != j:
                distance = ((atom1[1] - atom2[1])**2 + (atom1[2] - atom2[2])**2 + (atom1[3] - atom2[3])**2)**0.5
                if distance < bond_distance_threshold:
                    step_bonds.append((i, j))
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




fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Specify the range of frames (0 to 599 for the first 600 time steps)
start_frame = 0
end_frame = 599

animation = FuncAnimation(fig, update_plot, frames=range(start_frame, end_frame+1), interval=100)

# Save the animation as an MP4 video
animation.save('Trajectory1.gif', writer='pillow', fps=100)  # Adjust fps as needed

# plt.show()


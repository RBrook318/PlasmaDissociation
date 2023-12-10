# Masses of carbon and fluorine in amu
mass_C = 12.0
mass_F = 19.0

# Initialize kinetic energy
kinetic_energy = 0.0

# Open the file containing momentum data
with open('test.txt', 'r') as file:
    # Skip the lines until "momenta" is reached
    for line in file:
        if "momenta" in line:
            break
    
    # Read and process the momentum data
    for line in file:
        if line.strip():
            momenta = list(map(float, line.split()))
            
            # Calculate the velocity for each atom
            velocities = [momentum / mass_C if i < 4 else momentum / mass_F for i, momentum in enumerate(momenta)]
            
            # Calculate the square of the velocity components and sum them
            kinetic_energy += 0.5 * sum(vi ** 2 for vi in velocities)

print(f"Kinetic energy in Hartree: {kinetic_energy:.6f}")

import numpy as np

# Load the text file as a NumPy array
A = np.loadtxt('a.txt')
m = np.loadtxt('m.txt')
# geom = np.loadtxt('opt_geom.txt')
m = m * 1822.887  # Multiply m by 1836
geometry = """C      -3.2882930731     0.5560421350     0.0280274967
F      -4.5998455044     0.3078221324    -2.1051049787
F      -2.8218650371     2.9956614543     0.3892853324
F      -4.7607547604    -0.2547979579     1.8994098491
C      -0.9010983702    -0.9572933675    -0.0921917448
F      -1.3005152227    -3.4078116786    -0.4772640894
C       1.4354388883    -0.1272885785     0.1319523176
F       2.0982288430     2.2132205487     0.5141951239
F       3.3929789571    -1.6260182976    -0.0126311230
"""
T = 0.015834
n = 9
nmod = 3 * n - 6
Ax = A[:, 0]
Ay = A[:,1]
Az = A[:,2]

Ax = Ax.reshape(n, nmod, order = 'F')
Ay = Ay.reshape(n, nmod, order = 'F')
Az = Az.reshape(n, nmod, order = 'F')

rn = np.random.randn(nmod, 500)  # Use np.random.randn for standard normal distribution


# Initialize arrays for random
Meff = np.zeros(nmod)
rv = np.zeros((nmod, 500))


for i in range(nmod):
    for j in range(n):
        Meff[i] = Meff[i]+np.sum(((Ax[j, i]**2) + (Ay[j, i]**2) + (Az[j, i]**2)) * m[j])
    rv[i, :] = rn[i, :] * np.sqrt(2 * T / Meff[i])

# Saves effective masses for checking. 
# np.savetxt('Meff.txt', Meff, fmt='%f', delimiter='\t')

# Calculate the velocity by applying it through the tranformation matrix of normal modes.
Vx = np.dot(Ax, rv)
Vy = np.dot(Ay, rv)
Vz = np.dot(Az, rv)


Px = np.zeros((n,500))
Py = np.zeros((n,500))
Pz = np.zeros((n,500))
for i in range(n):
    Px[i,:] = Vx[i,:]*m[i]
    Py[i,:] = Vy[i,:]*m[i]
    Pz[i,:] = Vz[i,:]*m[i]
print(Px.shape)

# Save each momentum to separate files
for j in range(500):
    with open(f'Geometry.{j + 1}', 'w') as file:
        # Write the "momentum" line
        file.write(geometry)
        file.write("momentum\n")
        # Write Px, Py, and Pz for each atom on the same line
        for atom in range(n):
            # Access the Px, Py, and Pz values using the corresponding indices
            px_value = Px[atom, j]
            py_value = Py[atom, j]
            pz_value = Pz[atom, j]
            file.write(f'{px_value}  {py_value}  {pz_value}\n')
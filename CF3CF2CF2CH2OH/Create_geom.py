import numpy as np

# Load the text file as a NumPy array
A = np.loadtxt('a.txt')
m = np.loadtxt('m.txt')
# geom = np.loadtxt('opt_geom.txt')
m = m * 1822.887  # Multiply m by 1836
geometry = """C   4.1992585114  -1.2492114839  -0.0080420459
C   1.8834855674  0.4373184564  0.0002071925
C   -0.5951137825  -1.0878246895  0.0008027033
C   -3.0813296608  0.4314274526  -0.0005176058
F   -5.0010101418  -1.1781768703  0.0051820629
F   -3.2484480901  1.8752478184  2.0305819741
F   -3.2524240128  1.8648995363  -2.0385827343
F   -0.6251228065  -2.5784983163  -2.0538061868
F   -0.6231369275  -2.5750781880  2.0579408347
F   1.8830385440  1.9308553023  2.0569933002
F   1.8771926539  1.9405459716  -2.0498516026
O   6.2994642475  0.3496423013  -0.0010599610
H   7.8171023278  -0.6327070064  0.0053196088
H   4.1282120963  -2.4281041285  -1.6911160083
H   4.1303648101  -2.4447429760  1.6634557902
"""
T = 0.015834
n = 15
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
        
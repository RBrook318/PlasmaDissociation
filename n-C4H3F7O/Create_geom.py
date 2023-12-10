import numpy as np

# Load the text file as a NumPy array
A = np.loadtxt('a.txt')
m = np.loadtxt('m.txt')
# geom = np.loadtxt('opt_geom.txt')
m = m * 1822.887  # Multiply m by 1836
geometry = """C   6.3092958158  0.1278909773  0.0052366548
O   3.8276337154  1.1937151324  -0.0206583357
C   1.9010774949  -0.4130380901  -0.0045198773
C   -0.5770147077  1.1201851466  -0.0023186525
C   -3.0488393917  -0.4248754997  0.0015821978
F   -4.9815917780  1.1652346725  0.0117263959
F   -3.2140404970  -1.8652547424  -2.0347664789
F   -3.1991286541  -1.8733816247  2.0334970928
F   -0.6081393486  2.5872155230  2.0553676363
F   -0.6136615960  2.5880018735  -2.0587731980
F   1.9168153829  -1.9646900525  -2.0293104999
F   1.9330455118  -1.9413794466  2.0372916251
H   7.5762728350  1.7274619766  -0.0689346695
H   6.6084978867  -0.9310884237  1.7329707421
H   6.5873531008  -1.0687856420  -1.6339444857
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

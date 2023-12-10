import numpy as np

# Load the text file as a NumPy array
A = np.loadtxt('a.txt')
m = np.loadtxt('m.txt')
# geom = np.loadtxt('opt_geom.txt')
m = m * 1822.887  # Multiply m by 1836
geometry = """C       2.4680780671    -0.4420969519    -0.0004659616
C      -0.0001729096     1.1033546370    -0.0015047200
C      -2.4710227900    -0.4417431664     0.0001016348
F      -4.4071177658     1.1360534953     0.0017568645
F      -2.6065921738    -1.8870191459    -2.0334165869
F      -2.6012857033    -1.8852935120     2.0384893477
F       0.0012083946     2.5714722830     2.0562951904
F      -0.0000257235     2.5693766511    -2.0569273409
F       4.4015409303     1.1367847897     0.0010022774
F       2.6111086711    -1.8893003477    -2.0325322229
F       2.6046732558    -1.8834263146     2.0372427258
"""
T = 0.015834
n = 11
nmod = 3 * n - 6
Ax = A[:, 0]
Ay = A[:,1]
Az = A[:,2]

Ax = Ax.reshape(n, nmod, order = 'F')
Ay = Ay.reshape(n, nmod, order = 'F')
Az = Az.reshape(n, nmod, order = 'F')

rn = np.random.randn(nmod, 500)  # Use np.random.randn for standard normal distribution


# Initialize arrays for results
Meff = np.zeros(nmod)
rv = np.zeros((nmod, 500))


for i in range(nmod):
    for j in range(n):
        Meff[i] = Meff[i]+np.sum((Ax[j, i] ** 2 + Ay[j, i] ** 2 + Az[j, i] ** 2) * m[j])
    rv[i, :] = rn[i, :] * np.sqrt(2 * T / Meff[i])

# You can continue with the remaining calculations
# np.savetxt('Meff.txt', Meff, fmt='%f', delimiter='\t')

Vx = np.dot(Ax, rv)
Vy = np.dot(Ay, rv)
Vz = np.dot(Az, rv)

M = np.diag(m)
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
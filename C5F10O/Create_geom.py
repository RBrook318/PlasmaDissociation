import numpy as np

# Load the text file as a NumPy array
A = np.loadtxt('a.txt')
m = np.loadtxt('m.txt')
# geom = np.loadtxt('opt_geom.txt')
m = m * 1822.887  # Multiply m by 1836
geometry = """C   0.0312761894  0.3325787020  0.3921268865
C   2.5142844942  0.0353324016  -1.1018386595
C   4.9252439858  -0.2835608636  0.5070413448
F   6.8883627397  -0.4438221189  -1.0296201641
F   5.2462201872  1.6753003640  2.0249457599
F   4.8064974814  -2.3659705248  1.8823453710
F   2.3117514665  -1.9952204678  -2.5857606942
F   2.8193626358  2.0865350996  -2.5388803036
O   -1.8742344892  0.5212469788  -1.3312789038
C   -4.2282007527  0.9583221242  -0.4466698579
C   -5.9000882724  -0.8370204200  -0.0609353490
F   -8.2214424924  -0.3996087286  0.6493289954
F   -5.4264304378  -3.2397925390  -0.3563925299
F   -4.8175121090  3.3663577508  -0.1548723274
F   0.1446395410  2.3743489791  1.8640478488
F   -0.3138065626  -1.6585597583  1.9017341595
"""
T = 0.015834
n = 16
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
    with open(f'Geom/Geometry.{j + 1}', 'w') as file:
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

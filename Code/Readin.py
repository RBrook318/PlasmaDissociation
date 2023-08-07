import numpy as np

def read_input_file(input_file):
    with open(input_file, 'r') as f:
        # Read the input file and extract the data
        natom, nst = map(int, f.readline().split())
        branch = int(f.readline())
        time, TimeStep = map(float, f.readline().split())
        ndim = natom * 3

        # Read geometry
        nc, mult = map(int, f.readline().split())
        atom = []
        r0 = []
        for i in range(natom):
            line = f.readline().split()
            atom.append(line[0])
            r0.extend(map(float, line[1:]))

        # Read momenta
        p0 = []
        for i in range(natom):
            p0.extend(map(float, f.readline().split()))

        # Read amplitudes
        A0 = np.zeros(nst, dtype=np.complex128)
        for i in range(nst):
            A0[i] = complex(float(f.readline()))

        # Read potential energies
        Es0 = np.zeros(nst)
        for i in range(nst):
            val, _ = map(float, f.readline().split())
            Es0[i] = val

        # Read forces
        Fs0 = np.zeros((ndim, nst))
        for i in range(ndim):
            val, j, k = map(float, f.readline().split())
            Fs0[int(j) - 1, int(k) - 1] = val

        # Read couplings
        Cs0 = np.zeros((ndim, nst, nst))
        for i in range(ndim):
            val, j, k, l = map(float, f.readline().split())
            Cs0[int(j) - 1, int(k) - 1, int(l) - 1] = val
            Cs0[int(j) - 1, int(l) - 1, int(k) - 1] = -val

    return natom, nst, branch, time, TimeStep, nc, mult, atom, r0, p0, Es0, Fs0, Cs0
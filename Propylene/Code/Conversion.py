def convert_to_bohr_units(r0_angstrom):
    # Convert coordinates from Angstrom to Bohr units
    bohr_conversion_factor = 0.529177
    return r0_angstrom * bohr_conversion_factor

def make_geometry_input(f_inp):
    with open(f_inp, "r") as file:
        lines = file.readlines()

    natom, nst = map(int, lines[0].split())

    # Write the geometry data to geom.in
    with open("geom.in", "w") as geom_file:
        geom_file.write(f"{natom:2d} {nst:2d}\n")

        for line in lines[4:]:
            data = line.split()
            atom = data[0]
            r0_angstrom = [float(val) for val in data[1:4]]
            r0_bohr = convert_to_bohr_units(r0_angstrom)
            geom_file.write(f"{atom:1s} {r0_bohr[0]:15.8f} {r0_bohr[1]:15.8f} {r0_bohr[2]:15.8f}\n")

def q_to_prop(output_file):
    with open("t.0", "r") as file:
        lines = file.readlines()

    natom, nst = map(int, lines[0].split())

    if nst > 9:
        print("ERROR: Number of states > 9")
        return

    ndim = 3 * natom
    c = [[[0.0 for _ in range(ndim)] for _ in range(nst)] for _ in range(nst)]
    f = [[0.0 for _ in range(ndim)] for _ in range(nst)]
    e = [0.0 for _ in range(nst)]

    l1t = " Excited state   1: excitation energy (eV) ="
    l2t = " Gradient of the state energy (including CIS Excitation Energy)"

    with open("f.out", "r") as f_out_file:
        f_lines = f_out_file.readlines()

        for line in f_lines:
            if line.strip() == l1t:
                e[0] = float(f_lines[f_lines.index(line) + 1].strip())
                break

        for line in f_lines:
            if line.strip() == l2t:
                j = 0
                for j in range(natom // 6 + 1):
                    iend = min((j + 1) * 6, natom)
                    _, fx, _, fy, _, fz = map(float, f_lines[f_lines.index(line) + 1 + j * 4].split())
                    f[j * 18][0] = -fx
                    f[j * 18 + 1][0] = -fy
                    f[j * 18 + 2][0] = -fz
                break

    # Write electronic structure data to the output file
    with open(output_file, "a") as out_file:
        for i in range(nst):
            out_file.write(f"{e[i]:25.16f} {i + 1:8d}\n")

        out_file.write("\n")
        for i in range(nst):
            for j in range(ndim):
                out_file.write(f"{f[i][j]:25.16f} {i + 1:8d} {j + 1:8d}\n")

        out_file.write("\n")
        for i in range(nst - 1):
            for k in range(i + 1, nst):
                for j in range(ndim):
                    out_file.write(f"{c[i][k][j]:25.16f} {i + 1:8d} {k + 1:8d} {j + 1:8d}\n")




# Conversion factor: 1 Bohr = 0.529177 angstroms
angstrom_to_bohr = 0.529177

# Function to convert coordinates from angstroms to Bohr
def convert_to_bohr(coordinates):
    bohr_coordinates = []
    for line in coordinates:
        elements = line.split()
        element = elements[0]
        x = float(elements[1]) / angstrom_to_bohr
        y = float(elements[2]) / angstrom_to_bohr
        z = float(elements[3]) / angstrom_to_bohr
        bohr_coordinates.append(f"{element:2s}  {x:.10f}  {y:.10f}  {z:.10f}")

    return bohr_coordinates

# Provided coordinates
# Conversion factor: 1 Bohr = 0.529177 angstroms
angstrom_to_bohr = 0.529177

# Function to convert coordinates from angstroms to Bohr
def convert_to_bohr(coordinates):
    bohr_coordinates = []
    for line in coordinates:
        elements = line.split()
        element = elements[0]
        x = float(elements[1]) / angstrom_to_bohr
        y = float(elements[2]) / angstrom_to_bohr
        z = float(elements[3]) / angstrom_to_bohr
        bohr_coordinates.append(f"{element:2s}  {x:.10f}  {y:.10f}  {z:.10f}")

    return bohr_coordinates

# Provided coordinates
coordinates = [
    "C       0.0165506401     0.1759929998     0.2075045294",
    "C       1.3305015258     0.0186970943    -0.5830676763",
    "C       2.6063258367    -0.1500538871     0.2683146177",
    "F       3.6451631295    -0.2348604574    -0.5448513096",
    "F       2.7761790600     0.8865304207     1.0715547224",
    "F       2.5434879177    -1.2520171844     0.9960938764",
    "F       1.2233257058    -1.0558247815    -1.3683250869",
    "F       1.4919418615     1.1041463844    -1.3435170624",
    "O      -0.9918017843     0.2758319125    -0.7044821765",
    "C      -2.2374665897     0.5071220267    -0.2363674154",
    "C      -3.1221910117    -0.4429319548    -0.0322455852",
    "F      -4.3505982738    -0.2114637482     0.3436099698",
    "F      -2.8715421798    -1.7144236964    -0.1885947298",
    "F      -2.5493166053     1.7813990955    -0.0819548736",
    "F       0.0765399184     1.2564508697     0.9864112485",
    "F      -0.1660592154    -0.8776716772     1.0063539773",
]

bohr_coordinates = convert_to_bohr(coordinates)

# Print the result
for line in bohr_coordinates:
    print(line)




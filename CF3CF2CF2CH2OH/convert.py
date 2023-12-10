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
angstrom_coordinates = [
    "C  2.2221510213  -0.6610539854  -0.0042556657",
    "C  0.9966972421   0.2314188688   0.0001096415",
    "C -0.3149205261  -0.5756518057   0.0004247721",
    "C -1.6305687859   0.2283014851  -0.0002739051",
    "F -2.6464195438  -0.6234641017   0.0027422285",
    "F -1.7190040150   0.9923380148   1.0745372773",
    "F -1.7211079818   0.9868619419  -1.0787710956",
    "F -0.3308006114  -1.3644820035  -1.0868269965",
    "F -0.3297497299  -1.3626721503   1.0890149571",
    "F  0.9964606876   1.0217642163   1.0885135436",
    "F  0.9933671770   1.0268922956  -1.0847343215",
    "O  3.3335315921   0.1850226641  -0.0005609070",
    "H  4.1366307585  -0.3348139955   0.0028150146",
    "H  2.1845548925  -1.2848968584  -0.8948996959",
    "H  2.1856940591  -1.2937017538   0.8802625447",
]

bohr_coordinates = convert_to_bohr(angstrom_coordinates)

# Print the result
for line in bohr_coordinates:
    print(line)

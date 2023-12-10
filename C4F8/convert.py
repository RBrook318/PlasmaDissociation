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
    "C  0.8622448202   0.6782219824  -0.0635265251",
    "C -0.6782273354   0.8621743403   0.0632055696",
    "C -0.8622070647  -0.6781614688  -0.0627331576",
    "C  0.6782157412  -0.8622466479   0.0631667520",
    "F  1.2448579800  -1.5834281093  -0.8913779254",
    "F  1.0374525302  -1.3176599347   1.2592050001",
    "F -1.5833333649  -1.2455605895   0.8914057455",
    "F -1.3178451124  -1.0366215828  -1.2590015288",
    "F -1.0363915857   1.3184778568   1.2592386259",
    "F -1.2458755184   1.5825621389  -0.8913451896",
    "F  1.3182152871   1.0370605334  -1.2594350356",
    "F  1.5829023433   1.2451775497   0.8912352153",
]

bohr_coordinates = convert_to_bohr(angstrom_coordinates)

# Print the result
for line in bohr_coordinates:
    print(line)

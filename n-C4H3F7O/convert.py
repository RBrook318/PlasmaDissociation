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
    "C  3.3387342319   0.0676769637   0.0027711173",
    "O  2.0254957266   0.6316865926  -0.0109319161",
    "C  1.0060064855  -0.2185702574  -0.0023918151",
    "C -0.3053429120   0.5927762153  -0.0012269776",
    "C -1.6133756828  -0.2248343423   0.0008372627",
    "F -2.6361437923   0.6166153883   0.0062053390",
    "F -1.7007963081  -0.9870499088  -1.0767516210",
    "F -1.6929053038  -0.9913504680   1.0760798911",
    "F -0.3218133561   1.3690949488   1.0876532797",
    "F -0.3247356024   1.3695110674  -1.0894554246",
    "F  1.0143346139  -1.0396687879  -1.0738644424",
    "F  1.0229232248  -1.0273333514   1.0780878703",
    "H  4.0091893300   0.9141331464  -0.0364786416",
    "H  3.4970650862  -0.4927105788   0.9170482584",
    "H  3.4858757518  -0.5655767797  -0.8646458411",
]

bohr_coordinates = convert_to_bohr(angstrom_coordinates)

# Print the result
for line in bohr_coordinates:
    print(line)

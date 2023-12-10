import os



# Specify the range of file numbers
start_file = 3
end_file = 500

# Iterate over the range of file numbers
for file_number in range(start_file, end_file + 1):
    file_path = f"geometry.{file_number}"

    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove the last two lines
    lines = lines[:-2]

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

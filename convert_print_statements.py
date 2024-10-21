import os
import re

def convert_print_statements(file_path):
    """Converts print statements from Python 2 to Python 3 format in the given file."""
    with open(file_path, 'r') as file:
        content = file.readlines()

    modified_content = []
    for line in content:
        # Use regex to find print statements in various forms
        modified_line = re.sub(
            r'(?<!\w)print\s+(.*?)(\s*#.*)?$',  # Matches print statements
            r'print(\1)\2',  # Replaces with print() format
            line
        )
        print(modified_line)
        modified_content.append(modified_line)

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_content)

if __name__ == "__main__":
    # Specify the path of the Python file to be converted
    input_file = r"/home/lachmansinghet/data1/RLMD/RL/prepare_receptor4.py"
    
    # Check if the file exists
    if os.path.isfile(input_file):
        convert_print_statements(input_file)
    else:
        print("The specified file does not exist.")

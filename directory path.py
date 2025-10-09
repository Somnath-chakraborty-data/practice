import os

# Use forward slashes or escaped backslashes
path = 'C:/'

try:
    contents = os.listdir(path)
    print(f"Contents of directory '{os.path.abspath(path)}':")
    for item in contents:
        print(item)
except FileNotFoundError:
    print("The specified directory does not exist.")
except PermissionError:
    print("You do not have permission to access this directory.")

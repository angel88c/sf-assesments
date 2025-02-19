import os

if __name__ == '__main__':
    # Define the path where you want to create the file
    #path = r"C:\Users\c_ang\Innovative Board Test SAPI de CV\admin - iBtest Assesment\test.txt"
    #path = r"C:\Users\c_ang\OneDrive - Innovative Board Test SAPI de CV\01. Projects\SF\test1.txt"
    path = r"C:\Users\c_ang\Innovative Board Test SAPI de CV\admin - iBtest Assesment\test1.txt"
    # Ensure the directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Create and write to the file
    with open(path, 'w') as file:
        file.write('Hello, this is a test file!')

    print(f'File created at: {path}')
    
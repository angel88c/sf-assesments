import os
import shutil
from pages.lib.constants import * 

if __name__ == '__main__':
    # Define the path where you want to create the file
    #path = r"C:\Users\c_ang\Innovative Board Test SAPI de CV\admin - iBtest Assesment\test.txt"
    #path = r"C:\Users\c_ang\OneDrive - Innovative Board Test SAPI de CV\01. Projects\SF\test1.txt"
    #path = r"C:\Users\c_ang\Innovative Board Test SAPI de CV\admin - iBtest Assesment\test1.txt"
        
    # Ensure the directory exists
    #path = "/Users/c_angel/OneDrive - Innovative Board Test SAPI de CV/01_2025"
    path = PATH_FILE_Q
    #os.makedirs(os.path.dirname(path), exist_ok=True)

    SOURCE = "/Users/c_angel/Downloads/TEMPLATE_ICT"
    DEST = "/Users/c_angel/Documents/Ford_2U_2025"
    
    shutil.copytree(SOURCE, DEST, dirs_exist_ok=True)
    assesment = "ICT"
    country = "MX"
    customer = "SMTC"
    if assesment == "ICT":
        path = os.path.join(path, ICT_PROJECTS_FOLDER, country, customer)
        directories = os.listdir(path)
        for dir in directories:
            print(dir)

    # Create and write to the file
    # with open(path, 'w') as file:
    #     file.write('Hello, this is a test file!')

    # print(f'File created at: {path}')
    
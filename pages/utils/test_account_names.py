import os

DIR = os.path.join(os.path.dirname(__file__), "..", "..", "accounts.txt")
def get_account_names_from_local_file():
    data = []
    try:
        with open(DIR, mode='r') as file:
            data = [s.rstrip('\n') for s in file.readlines()]
        
        if not "Other" in data:
            data.append("Other")
            
        return data
    except Exception as e:
        return data

if __name__ == "__main__":
    
   print(get_account_names_from_local_file())
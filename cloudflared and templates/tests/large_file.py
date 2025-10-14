import os

if __name__ == "__main__":
    
    FILE = r"C:\Users\Administrator\OneDrive - Innovative Board Test SAPI de CV\Documentos - Public_Quotes_2025\01_2025\1_In_Circuit Test (ICT)\MX\HARMAN TIJ\Titan Edge -IOAudioBoards\1_Customer_Info\7_ALL_Info_Shared"
    
    file_to_create = "512940401_PCBASYBSSTITANEDGEIOAUDIN_HPD_D7_Design1.txt"
    
    save_path = os.path.join(FILE, file_to_create)
    print(save_path)
    with open(save_path, "wb") as f:
        f.write(b"123")
    



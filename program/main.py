# main_script.py

import easygui as eg
from load_data_utils import generate_load_data, get_channels_from_files, get_names_of_channels_from_user 

def main():
    print("\n ### Load_Data takes a folder with images acquired on Cytation 5 and creates 3 CSV files on a folder called load_data. ### \n")
    print("\n **INSTRUCTION**: Choose a folder containing images \n")
    
    input_folder = eg.diropenbox('Choose folder with images', 'Choose folder')
    print(f"\n INPUT FOLDER: {input_folder} \n")

    ch_unique = get_channels_from_files(input_folder)
    ch_dic = get_names_of_channels_from_user(ch_unique)

    generate_load_data(input_folder, ch_dic)

    print("\n ## Finished successfully. ## \n ## Check your image/load_data folder! ##")

if __name__ == "__main__":
    main()

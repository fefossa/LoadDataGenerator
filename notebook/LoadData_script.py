# test load_data only on the command line

import easygui as eg
import sys
import pandas as pd
import numpy as np
import re
import os
from PIL import Image
from os import walk

def get_image_width(image_path):
    try:
        with Image.open(image_path) as img:
            width, _ = img.size
            return width
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def remove_path_cols(df, prefix="PathName_"):
    # Specify the prefix you want to remove
    prefix_to_remove = prefix

    # Use the filter function to select columns with the specified prefix
    filtered_columns = df.filter(like=prefix_to_remove, axis=1)

    # Use the drop method to remove the selected columns
    df = df.drop(columns=filtered_columns)
    return df

def generate_load_data(input_folder, ch_dic):

    illum_list = [True, False]

    for illum_bool in illum_list:
        df = pd.DataFrame()
        #plate name
        regex_plate = r".*[\\/](?P<Assay>.*)[\\/](?P<Plate>.*)$"
        plate_search = re.search(regex_plate, input_folder)
        platefind = plate_search.group('Plate')
        plate = platefind.replace(" ", "_")
        images_dir = input_folder
        illum_dir = input_folder + r"/illum"
        #filesname and channel
        files = []
        for (dirpath, dirnames, filenames) in walk(input_folder):
            files.extend(sorted(filenames))
            break
        #find channels
        channels = []
        regex = r"^(?P<Well>.*)_.*_.*_(?P<Site>.*)_(?P<Channel>.*)_001.tif"
        for f in files:
            matches = re.search(regex, f)
            if matches:
                channels.append(matches.group('Channel'))
        channels = np.array(channels)
        ch_unique = np.unique(channels)
        #create columns with files and pathnames
        temp_list = []
        illum_list = []
        for ch in ch_unique:
            temp_list = []
            for file in files:
                if ch in file and 'tif' in file:
                    temp_list.append(file)
            if ' ' in ch:
                ch = ch.replace(' ', '')
            for key,value in ch_dic.items():
                if key in ch:
                    df["FileName_"+value] = temp_list
                    # print(temp_list)
                    df["PathName_"+value] = images_dir
                    file_width = temp_list[0]
                    path_width = images_dir
                    if illum_bool:
                        illum_temp = plate + "_Illum" + value + ".npy"
                        df["FileName_Illum"+value] = illum_temp
                        df["PathName_Illum"+value] = illum_dir
        #get wells and sites names
        wells = []
        sites = []
        for files in df.iloc[:, 0]:
            matches = re.search(regex, files)
            wells.append(matches.group('Well'))
            sites.append(matches.group('Site'))
        df['Metadata_Well'] = wells
        df['Metadata_Site'] = sites
        df['Metadata_Plate'] = plate
        #save df
        directory = "load_data_csv"
        path = os.path.join(input_folder, directory)
        os.makedirs(path, exist_ok=True)
        if illum_bool:
            df.to_csv(path + r'\load_data_with_illum.csv', index=False)
        else:
            df.to_csv(path + r'\load_data.csv', index=False)
            width = get_image_width(os.path.join(path_width, file_width))
            df['Metadata_Width'] = width
            df = remove_path_cols(df, prefix="PathName_")
            df.to_csv(path + r'\metadata_representative_cells.csv', index=False)


# path_scripts = eg.diropenbox('Choose folder where "load_data_utils.py" is located', 'Choose folder')

# sys.path.append(path_scripts)

# from LoadDataGenerator.notebook import load_data_utils

input_folder = eg.diropenbox('Choose folder with images', 'Choose folder')
print(input_folder)

dirlist = eg.enterbox("Enter the NUMBER of channels in your assay:")
number_inputs = [x+1 for x in range(int(dirlist))] 
channel_inputs = eg.multenterbox("Write the name of each channel like on the filename (DAPI, GFP, etc):", "Channels", number_inputs)
names_inputs = eg.multenterbox("Write a name to represent each channel:", "Names", channel_inputs)
ch_dic = dict(zip(channel_inputs, names_inputs))
print(ch_dic)

generate_load_data(input_folder, ch_dic)

print("Finished successfully. Check your image folder!")
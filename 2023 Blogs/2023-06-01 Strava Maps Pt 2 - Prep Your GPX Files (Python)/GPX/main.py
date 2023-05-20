from gpx_converter import Converter

Converter(input_file='Paris-Files/8663587823.gpx').gpx_to_csv(output_file='Paris-Files/8663587823.csv')

# import required module
import os
# assign directory
directory = 'Tom_2021_Gpx'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        df = Converter(input_file=f).gpx_to_dataframe()
        df['filename'] = filename
        df.to_csv(f'OutputFiles/{filename}.csv')

import glob
import pandas as pd
os.chdir("/Users/christophermayes/PycharmProjects/GPX/OutputFiles")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv("All_Data.csv", index=False, encoding='utf-8-sig')
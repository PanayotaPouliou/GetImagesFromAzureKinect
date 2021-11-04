from os import path
from capture_data_functions import get_data, create_folder,timestamp


#in_path= 'C:\\Users\\ppou\\Downloads\\gitclone\\sg_benchmark\\DataAcquisition\\filesaving' 
in_path='C:\\Users\\ppou\\source\\repos\\pyKinectAzure\\DataAcquisition\\filesaving'

#New Folder Creation
path = create_folder(in_path, 'CITA')

#Save files in the created folder
get_data(path, 'no', 10)

#renames files in the path with their timestamp
timestamp(path)